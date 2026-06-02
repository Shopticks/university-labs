import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .effects import EffectsStack
from .entities import Ghost, GhostMode, Pacman, PacmanState
from .geometry import DOWN, LEFT, RIGHT, UP, ZERO, Vec2, dir_name, opposite
from .maze import Maze


class GamePhase(Enum):
    READY = "ready"
    PLAYING = "playing"
    DYING = "dying"
    LEVEL_CLEAR = "level_clear"
    GAME_OVER = "game_over"


@dataclass
class GameEvent:
    kind: str
    data: dict = field(default_factory=dict)


@dataclass
class Snapshot:
    """Plain-data view of game state for the renderer."""
    maze_name: str
    grid: list[list[str]]
    pellets: set[tuple[int, int]]
    powers: set[tuple[int, int]]
    pacman_pos: tuple[float, float]
    pacman_dir: str
    pacman_state: str
    pacman_death_progress: float
    ghosts: list[dict]
    score: int
    high_score: int
    lives: int
    level: int
    phase: str
    ready_text: str
    fruit: dict | None
    effect_remaining: dict[str, float]


class Game:
    """Top-level orchestrator. Pure-domain (no pygame)."""

    def __init__(self, maze: Maze, cfg: dict, high_score: int = 0) -> None:
        self.maze = maze
        self.cfg = cfg
        self.high_score = high_score
        self.score = 0
        self.lives = int(cfg["pacman"]["lives"])
        self.level = 1
        self.phase = GamePhase.READY
        self.ready_timer = float(cfg["pacman"]["ready_seconds"])
        self.death_timer = 0.0
        self.death_duration = float(cfg["pacman"]["death_animation_seconds"])
        self.events: list[GameEvent] = []
        self.effects = EffectsStack()
        self._ghost_chain = 0
        self._extra_life_given = False
        # Scatter/Chase global timer.
        self._mode_pattern = list(cfg["ghosts"]["scatter_chase_pattern_seconds"])
        self._mode_index = 0
        self._mode_timer = self._mode_pattern[0]
        self._global_mode = GhostMode.SCATTER
        # Fruit state.
        self._fruit_thresholds = list(cfg["fruits"]["spawn_pellet_thresholds"])
        self._fruit_active: dict | None = None
        self._fruit_lifetime = float(cfg["fruits"]["lifetime_seconds"])
        # Entities.
        self.pacman = Pacman(pos=Vec2(0, 0))
        self.ghosts: list[Ghost] = []
        self._build_entities()

    # ——— setup ———
    def _build_entities(self) -> None:
        # ——— Pacman ———
        px, py = self.maze.pacman_start
        self.pacman = Pacman(
            pos=Vec2(px + 0.5, py+ 0.5),
            speed=float(self.cfg["pacman"]["speed_tiles_per_sec"]),
        )
        self.pacman.state = PacmanState.READY

        # ——— Ghosts ———
        thresholds = self.cfg["ghosts"]["release_pellet_thresholds"]
        self.ghosts = []
        for name in ("blinky", "pinky", "inky", "clyde"):
            home = self.maze.ghost_spawn[name]
            corner = self.maze.scatter_corners[name]
            g = Ghost(
                name=name,
                pos=Vec2(home[0] + 0.5, home[1] + 0.5),
                direction=LEFT if name == "blinky" else UP,
                home_tile=home,
                scatter_corner=corner,
                release_at_pellets=int(thresholds.get(name, 0)),
            )
            if name == "blinky":
                g.mode = GhostMode.SCATTER
            else:
                g.mode = GhostMode.HOUSE
            self.ghosts.append(g)

    def reset_round(self, *, keep_score: bool = True) -> None:
        self.maze.reset_pellets()
        self._build_entities()
        self.phase = GamePhase.READY
        self.ready_timer = float(self.cfg["pacman"]["ready_seconds"])
        self.effects.clear()
        self._ghost_chain = 0
        self._mode_index = 0
        self._mode_timer = self._mode_pattern[0]
        self._global_mode = GhostMode.SCATTER
        self._fruit_active = None
        self._fruit_thresholds = list(self.cfg["fruits"]["spawn_pellet_thresholds"])
        if not keep_score:
            self.score = 0
            self.lives = int(self.cfg["pacman"]["lives"])
            self.level = 1
            self._extra_life_given = False

    def next_level(self) -> None:
        self.level += 1
        self.maze.reset_pellets()
        self._build_entities()
        self.phase = GamePhase.READY
        self.ready_timer = float(self.cfg["pacman"]["ready_seconds"])
        self.effects.clear()
        self._ghost_chain = 0
        self._mode_index = 0
        self._mode_timer = self._mode_pattern[0]
        self._global_mode = GhostMode.SCATTER
        self._fruit_active = None
        self._fruit_thresholds = list(self.cfg["fruits"]["spawn_pellet_thresholds"])

    # ---- input ----
    def request_direction(self, d: Vec2) -> None:
        if self.phase in (GamePhase.PLAYING, GamePhase.READY):
            self.pacman.request(d)

    # ---- main step ----
    def step(self, dt: float) -> list[GameEvent]:
        self.events = []

        if self.phase is GamePhase.READY:
            self.ready_timer -= dt
            if self.ready_timer <= 0:
                self.pacman.state = PacmanState.ALIVE
                self.phase = GamePhase.PLAYING
            return self.events

        if self.phase is GamePhase.DYING:
            self.death_timer += dt
            self.pacman.death_timer = self.death_timer
            if self.death_timer >= self.death_duration:
                self.death_timer = 0.0
                self.pacman.death_timer = 0.0
                self.lives -= 1
                if self.lives <= 0:
                    self.phase = GamePhase.GAME_OVER
                    self.events.append(GameEvent("game_over"))
                else:
                    self.reset_round(keep_score=True)
                    self.events.append(GameEvent("life_lost"))
            return self.events

        if self.phase is GamePhase.LEVEL_CLEAR:
            self.ready_timer -= dt
            if self.ready_timer <= 0:
                self.next_level()
                self.events.append(GameEvent("level_start", {"level": self.level}))
            return self.events

        if self.phase is GamePhase.GAME_OVER:
            return self.events

        # --- PLAYING ---
        self._tick_modes(dt)
        # Tick effects.
        expired = self.effects.step(dt)
        for e in expired:
            if e.kind == "frightened":
                # Anyone still frightened becomes scatter/chase per global mode.
                for g in self.ghosts:
                    if g.mode is GhostMode.FRIGHTENED:
                        g.mode = self._global_mode
                self._ghost_chain = 0

        # Pacman speed.
        speed_mul = 1.0
        if self.effects.has("speed_up"):
            speed_mul = float(self.cfg["effects"]["fruit_speed_multiplier"])
        # Pacman step.
        self.pacman.step(dt, self.maze, speed_mul=speed_mul)

        # Pellet pickup.
        eaten = self.maze.consume_pellet(self.pacman.tile)
        if eaten == "pellet":
            self._add_score(int(self.cfg["scoring"]["pellet"]))
            self.events.append(GameEvent("pellet"))
        elif eaten == "power":
            self._add_score(int(self.cfg["scoring"]["power_pellet"]))
            self._activate_power_pellet()
            self.events.append(GameEvent("power"))

        # Ghost release based on pellets eaten.
        pellets_eaten = self.maze.pellets_eaten()
        for g in self.ghosts:
            if g.mode is GhostMode.HOUSE and pellets_eaten >= g.release_at_pellets:
                g.mode = GhostMode.LEAVING

        # Ghost stepping.
        speeds = {
            "normal": float(self.cfg["ghosts"]["speed_normal_tiles_per_sec"]),
            "frightened": float(self.cfg["ghosts"]["speed_frightened_tiles_per_sec"]),
            "eaten": float(self.cfg["ghosts"]["speed_eaten_tiles_per_sec"]),
            "tunnel": float(self.cfg["ghosts"]["speed_tunnel_tiles_per_sec"]),
        }
        blinky = next((g for g in self.ghosts if g.name == "blinky"), None)
        # Door exit tile = first walkable cell above door (door coords are at row 12; row 11 is exit).
        door_exit = (self.maze.ghost_door[0][0], self.maze.ghost_door[0][1] - 1)
        # Apply freeze effect.
        frozen = self.effects.has("freeze")
        for g in self.ghosts:
            g.frozen = frozen
            g.step(dt, self.maze, self.pacman, blinky, self._global_mode, speeds, door_exit)

        # Fruit lifecycle.
        self._update_fruit(dt, pellets_eaten)

        # Collisions.
        self._check_collisions()

        # Level clear?
        if self.maze.pellets_left() == 0:
            self.phase = GamePhase.LEVEL_CLEAR
            self.ready_timer = 1.5
            self.events.append(GameEvent("level_clear"))

        return self.events

    # ---- helpers ----
    def _tick_modes(self, dt: float) -> None:
        if self.effects.has("frightened"):
            return
        self._mode_timer -= dt
        if self._mode_timer <= 0 and self._mode_index < len(self._mode_pattern) - 1:
            self._mode_index += 1
            self._mode_timer = self._mode_pattern[self._mode_index]
            # Alternate scatter <-> chase by index parity.
            self._global_mode = GhostMode.SCATTER if self._mode_index % 2 == 0 else GhostMode.CHASE
            # Reverse non-frightened ghosts.
            for g in self.ghosts:
                if g.mode in (GhostMode.SCATTER, GhostMode.CHASE):
                    g.direction = opposite(g.direction) if g.direction != ZERO else g.direction
                    g.mode = self._global_mode

    def _activate_power_pellet(self) -> None:
        seconds = float(self.cfg["ghosts"]["frightened_seconds"])
        self.effects.add("frightened", seconds)
        self._ghost_chain = 0
        for g in self.ghosts:
            if g.mode in (GhostMode.SCATTER, GhostMode.CHASE):
                g.mode = GhostMode.FRIGHTENED
                g.direction = opposite(g.direction) if g.direction != ZERO else g.direction

    def _check_collisions(self) -> None:
        ptile = self.pacman.tile
        for g in self.ghosts:
            if g.tile != ptile:
                continue
            if g.mode is GhostMode.FRIGHTENED:
                idx = min(self._ghost_chain, len(self.cfg["scoring"]["ghost_chain"]) - 1)
                val = int(self.cfg["scoring"]["ghost_chain"][idx])
                self._add_score(val)
                self._ghost_chain += 1
                g.mode = GhostMode.EATEN
                self.events.append(GameEvent("ghost_eaten", {"value": val,
                                                              "pos": (g.pos.x, g.pos.y)}))
            elif g.mode in (GhostMode.EATEN, GhostMode.HOUSE, GhostMode.LEAVING):
                continue
            else:
                self._die()
                return

        # Fruit pickup.
        if self._fruit_active and self._fruit_active["tile"] == ptile:
            kind = self._fruit_active["kind"]
            val = int(self.cfg["scoring"]["fruit"].get(kind, 100))
            self._add_score(val)
            # Apply effect based on kind.
            if kind == "cherry":
                self.effects.add("speed_up", float(self.cfg["effects"]["fruit_speed_boost_seconds"]))
                self.events.append(GameEvent("fruit_eaten",
                                              {"kind": kind, "effect": "speed_up", "value": val}))
            else:  # strawberry → freeze ghosts
                self.effects.add("freeze", float(self.cfg["effects"]["fruit_freeze_seconds"]))
                self.events.append(GameEvent("fruit_eaten",
                                              {"kind": kind, "effect": "freeze", "value": val}))
            self._fruit_active = None

    def _update_fruit(self, dt: float, pellets_eaten: int) -> None:
        # Spawn fruit at thresholds.
        while self._fruit_thresholds and pellets_eaten >= self._fruit_thresholds[0]:
            self._fruit_thresholds.pop(0)
            kind = random.choice(list(self.cfg["fruits"]["kinds"]))
            self._fruit_active = {
                "kind": kind,
                "tile": tuple(self.maze.fruit_position),
                "remaining": self._fruit_lifetime,
            }
            self.events.append(GameEvent("fruit_spawn", {"kind": kind}))
        if self._fruit_active is not None:
            self._fruit_active["remaining"] -= dt
            if self._fruit_active["remaining"] <= 0:
                self._fruit_active = None

    def _die(self) -> None:
        self.pacman.state = PacmanState.DYING
        self.phase = GamePhase.DYING
        self.death_timer = 0.0
        self.pacman.death_timer = 0.0
        self.events.append(GameEvent("pacman_died"))

    def _add_score(self, v: int) -> None:
        self.score += v
        if self.score > self.high_score:
            self.high_score = self.score
        extra = int(self.cfg["scoring"]["extra_life_at"])
        if not self._extra_life_given and self.score >= extra:
            self.lives += 1
            self._extra_life_given = True
            self.events.append(GameEvent("extra_life"))

    # ---- snapshot ----
    def snapshot(self) -> Snapshot:
        ghosts = []
        for g in self.ghosts:
            ghosts.append({
                "name": g.name,
                "pos": (g.pos.x, g.pos.y),
                "dir": dir_name(g.direction),
                "mode": g.mode.value,
            })
        fruit = None
        if self._fruit_active is not None:
            fruit = {
                "kind": self._fruit_active["kind"],
                "tile": self._fruit_active["tile"],
                "remaining": self._fruit_active["remaining"],
            }
        ready_text = ""
        if self.phase is GamePhase.READY:
            ready_text = "READY!"
        elif self.phase is GamePhase.LEVEL_CLEAR:
            ready_text = "LEVEL!"
        elif self.phase is GamePhase.GAME_OVER:
            ready_text = "GAME OVER"
        eff_remaining = {
            k: self.effects.remaining(k)
            for k in ("frightened", "speed_up", "freeze")
        }
        death_progress = (self.death_timer / self.death_duration) if self.phase is GamePhase.DYING else 0.0
        return Snapshot(
            maze_name=self.maze.name,
            grid=self.maze.grid,
            pellets=set(self.maze.pellets),
            powers=set(self.maze.power_pellets),
            pacman_pos=(self.pacman.pos.x, self.pacman.pos.y),
            pacman_dir=dir_name(self.pacman.direction) if self.pacman.direction != ZERO else "right",
            pacman_state=self.pacman.state.value,
            pacman_death_progress=death_progress,
            ghosts=ghosts,
            score=self.score,
            high_score=self.high_score,
            lives=self.lives,
            level=self.level,
            phase=self.phase.value,
            ready_text=ready_text,
            fruit=fruit,
            effect_remaining=eff_remaining,
        )
