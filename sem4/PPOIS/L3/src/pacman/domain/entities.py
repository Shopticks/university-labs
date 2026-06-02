import random
from dataclasses import dataclass, field
from enum import Enum

from .geometry import (
    DIRECTIONS,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    ZERO,
    Vec2,
    dir_name,
    opposite,
)
from .maze import Maze


EPS = 1e-6


def _tile_of(pos: Vec2) -> tuple[int, int]:
    return (int(pos.x), int(pos.y))


def _tile_center(tile: tuple[int, int]) -> Vec2:
    return Vec2(tile[0] + 0.5, tile[1] + 0.5)


def _is_centered(pos: Vec2, tile: tuple[int, int]) -> bool:
    c = _tile_center(tile)
    return abs(pos.x - c.x) < 1e-3 and abs(pos.y - c.y) < 1e-3


class PacmanState(Enum):
    READY = "ready"
    ALIVE = "alive"
    DYING = "dying"
    DEAD = "dead"


@dataclass
class Pacman:
    pos: Vec2
    direction: Vec2 = ZERO
    queued: Vec2 = ZERO
    speed: float = 8.0  # tiles per second
    state: PacmanState = PacmanState.READY
    death_timer: float = 0.0
    dot_speed_penalty_until: float = 0.0

    @property
    def tile(self) -> tuple[int, int]:
        return _tile_of(self.pos)

    def request(self, d: Vec2) -> None:
        self.queued = d

    def reset(self, start_tile: tuple[int, int]) -> None:
        self.pos = _tile_center(start_tile)
        self.direction = ZERO
        self.queued = ZERO
        self.state = PacmanState.READY
        self.death_timer = 0.0

    def step(self, dt: float, maze: Maze, speed_mul: float = 1.0) -> None:
        if self.state is not PacmanState.ALIVE:
            return
        if self.direction == ZERO and self.queued == ZERO:
            return

        # Allow 180' turn immediately
        if (self.queued != ZERO and self.direction != ZERO
                and self.queued == opposite(self.direction)):
            self.direction = self.queued
            self.queued = ZERO

        remaining = self.speed * speed_mul * dt
        while remaining > EPS:
            if self.direction == ZERO:
                if self.queued != ZERO and self._can_enter(maze, self.queued):
                    self.direction = self.queued
                    self.queued = ZERO
                else:
                    break

            tile = self.tile
            tile_center = _tile_center(tile)
            rel = self.pos - tile_center
            proj = rel.x * self.direction.x + rel.y * self.direction.y
            if proj < -EPS:
                dist_to_decision = -proj
                target = tile_center
            else:
                dist_to_decision = 1.0 - proj
                target = tile_center + self.direction * 1.0

            if dist_to_decision <= remaining + EPS:
                self.pos = target
                remaining -= dist_to_decision
                # Apply queued turn if possible at decision point.
                if self.queued != ZERO and self._can_enter(maze, self.queued):
                    self.direction = self.queued
                    self.queued = ZERO
                if not self._can_enter(maze, self.direction):
                    self.direction = ZERO
            else:
                self.pos = self.pos + self.direction * remaining
                remaining = 0.0

        # Horizontal tunnel wrap-around.
        if self.pos.x < 0:
            self.pos = Vec2(self.pos.x + maze.cols, self.pos.y)
        elif self.pos.x >= maze.cols:
            self.pos = Vec2(self.pos.x - maze.cols, self.pos.y)

    def _can_enter(self, maze: Maze, d: Vec2) -> bool:
        if d == ZERO:
            return False
        col, row = self.tile
        return maze.is_pacman_walkable(col + int(d.x), row + int(d.y))


class GhostMode(Enum):
    HOUSE = "house"
    LEAVING = "leaving"
    SCATTER = "scatter"
    CHASE = "chase"
    FRIGHTENED = "frightened"
    EATEN = "eaten"


@dataclass
class Ghost:
    name: str  # "blinky" | "pinky" | "inky" | "clyde"
    pos: Vec2
    direction: Vec2
    home_tile: tuple[int, int]
    scatter_corner: tuple[int, int]
    mode: GhostMode = GhostMode.HOUSE
    target: tuple[int, int] = (0, 0)
    release_at_pellets: int = 0
    in_house_bob_dir: int = 1  # +1 down, -1 up
    frozen: bool = False

    @property
    def tile(self) -> tuple[int, int]:
        return _tile_of(self.pos)

    def reset(self) -> None:
        self.pos = _tile_center(self.home_tile)
        self.direction = LEFT if self.name in ("blinky",) else UP
        self.mode = GhostMode.HOUSE if self.name != "blinky" else GhostMode.SCATTER
        self.target = self.scatter_corner

    def step(self, dt: float, maze: Maze, pacman: Pacman, blinky: "Ghost | None",
             global_mode: GhostMode, speeds: dict, door_exit_tile: tuple[int, int]) -> None:
        if self.frozen and self.mode not in (GhostMode.EATEN,):
            return

        if self.mode is GhostMode.HOUSE:
            self._bob(dt, maze, speeds["frightened"])
            return

        if self.mode is GhostMode.LEAVING:
            self._move_towards_door(dt, maze, door_exit_tile, speeds["normal"])
            return

        if self.mode is GhostMode.EATEN:
            sp = speeds["eaten"]
        elif self.mode is GhostMode.FRIGHTENED:
            sp = speeds["frightened"]
        elif self.tile[1] == maze.tunnels_row and maze.tile_at(*self.tile) == "T":
            sp = speeds["tunnel"]
        else:
            sp = speeds["normal"]

        remaining = sp * dt
        while remaining > EPS:
            tile = self.tile
            center = _tile_center(tile)
            rel = self.pos - center
            proj = rel.x * self.direction.x + rel.y * self.direction.y if self.direction != ZERO else -1
            if proj < -EPS:
                dist_to_decision = -proj
                target = center
            else:
                dist_to_decision = 1.0 - proj
                target = center + self.direction * 1.0

            if dist_to_decision <= remaining + EPS:
                self.pos = target
                remaining -= dist_to_decision
                self._update_target(pacman, blinky, global_mode, maze)
                self._pick_direction(maze, global_mode)
            else:
                self.pos = self.pos + self.direction * remaining
                remaining = 0.0

        if self.pos.x < 0:
            self.pos = Vec2(self.pos.x + maze.cols, self.pos.y)
        elif self.pos.x >= maze.cols:
            self.pos = Vec2(self.pos.x - maze.cols, self.pos.y)

        if self.mode is GhostMode.EATEN and self.tile == self.home_tile:
            self.mode = GhostMode.LEAVING

    def _bob(self, dt: float, maze: Maze, sp: float) -> None:
        d = Vec2(0, self.in_house_bob_dir)
        ny = self.pos.y + d.y * sp * dt
        lo = self.home_tile[1] - 0.35
        hi = self.home_tile[1] + 1.35
        if ny < lo:
            ny = lo
            self.in_house_bob_dir = 1
        elif ny > hi:
            ny = hi
            self.in_house_bob_dir = -1
        self.pos = Vec2(self.pos.x, ny)

    def _move_towards_door(self, dt: float, maze: Maze, exit_tile: tuple[int, int], sp: float) -> None:
        door_x = (maze.ghost_door[0][0] + maze.ghost_door[-1][0]) / 2 + 0.5
        if abs(self.pos.x - door_x) > 0.02:
            d = 1 if door_x > self.pos.x else -1
            self.pos = Vec2(self.pos.x + d * sp * dt, self.pos.y)
            if abs(self.pos.x - door_x) <= sp * dt:
                self.pos = Vec2(door_x, self.pos.y)
            return
        target_y = exit_tile[1] + 0.5
        if self.pos.y > target_y + 0.02:
            self.pos = Vec2(self.pos.x, self.pos.y - sp * dt)
            if self.pos.y - target_y < 0:
                self.pos = Vec2(self.pos.x, target_y)
            return
        self.pos = Vec2(self.pos.x, target_y)
        self.direction = LEFT
        self.mode = GhostMode.SCATTER

    def _update_target(self, pacman: Pacman, blinky: "Ghost | None",
                       global_mode: GhostMode, maze: Maze) -> None:
        if self.mode is GhostMode.EATEN:
            self.target = self.home_tile
            return
        if self.mode is GhostMode.FRIGHTENED:
            self.target = self.tile
            return
        if global_mode is GhostMode.SCATTER:
            self.target = self.scatter_corner
            return

        px, py = pacman.tile
        if self.name == "blinky":
            self.target = (px, py)
        elif self.name == "pinky":
            d = pacman.direction if pacman.direction != ZERO else RIGHT
            self.target = (px + int(d.x) * 4, py + int(d.y) * 4)
        elif self.name == "inky":
            d = pacman.direction if pacman.direction != ZERO else RIGHT
            ahead = (px + int(d.x) * 2, py + int(d.y) * 2)
            if blinky is not None:
                bx, by = blinky.tile
                self.target = (2 * ahead[0] - bx, 2 * ahead[1] - by)
            else:
                self.target = ahead
        elif self.name == "clyde":
            dx = px - self.tile[0]
            dy = py - self.tile[1]
            if dx * dx + dy * dy > 64:
                self.target = (px, py)
            else:
                self.target = self.scatter_corner

    def _pick_direction(self, maze: Maze, global_mode: GhostMode) -> None:
        opts: list[Vec2] = []
        for d in DIRECTIONS:
            if d == opposite(self.direction):
                continue
            nx, ny = self.tile[0] + int(d.x), self.tile[1] + int(d.y)
            if global_mode is GhostMode.EATEN:
                ok = maze.is_ghost_walkable(nx, ny)
            else:
                ok = maze.is_pacman_walkable(nx, ny)
            if ok:
                opts.append(d)

        if not opts:
            opts = [opposite(self.direction)]

        if global_mode is GhostMode.FRIGHTENED:
            self.direction = random.choice(opts)
            return

        tx, ty = self.target
        best = min(
            opts,
            key=lambda d: (self.tile[0] + int(d.x) - tx) ** 2
                          + (self.tile[1] + int(d.y) - ty) ** 2,
        )
        self.direction = best
