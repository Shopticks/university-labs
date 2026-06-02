import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

WALL = "X"
PELLET = "."
POWER = "o"
EMPTY = " "
DOOR = "-"
TUNNEL = "T"

PACMAN_WALKABLE = {PELLET, POWER, EMPTY, TUNNEL}
GHOST_WALKABLE = {PELLET, POWER, EMPTY, TUNNEL, DOOR}


@dataclass
class Maze:
    name: str
    cols: int
    rows: int
    grid: list[list[str]]
    pacman_start: tuple[int, int]
    ghost_spawn: dict[str, tuple[int, int]]
    ghost_door: list[tuple[int, int]]
    scatter_corners: dict[str, tuple[int, int]]
    tunnels_row: int
    fruit_position: tuple[int, int]
    initial_pellet_count: int = 0
    pellets: set[tuple[int, int]] = field(default_factory=set)
    power_pellets: set[tuple[int, int]] = field(default_factory=set)

    @classmethod
    def load(cls, path: str | Path) -> "Maze":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        rows_layout = data["rows_layout"]
        grid = [list(r) for r in rows_layout]
        pellets: set[tuple[int, int]] = set()
        powers: set[tuple[int, int]] = set()
        for y, row in enumerate(grid):
            for x, ch in enumerate(row):
                if ch == PELLET:
                    pellets.add((x, y))
                elif ch == POWER:
                    powers.add((x, y))
        gh = data["ghost_house"]
        spawn = {k: tuple(v) for k, v in gh["spawn"].items()}
        door = [tuple(d) for d in gh["door"]]
        corners = {k: tuple(v) for k, v in data["scatter_corners"].items()}
        m = cls(
            name=data["name"],
            cols=int(data["cols"]),
            rows=int(data["rows"]),
            grid=grid,
            pacman_start=tuple(data["pacman_start"]),
            ghost_spawn=spawn,
            ghost_door=door,
            scatter_corners=corners,
            tunnels_row=int(data.get("tunnels_row", -1)),
            fruit_position=tuple(data.get("fruit_position", [0, 0])),
            pellets=pellets,
            power_pellets=powers,
        )
        m.initial_pellet_count = len(pellets) + len(powers)
        return m

    def tile_at(self, x: int, y: int) -> str:
        if not (0 <= y < self.rows and 0 <= x < self.cols):
            return WALL
        return self.grid[y][x]

    def is_pacman_walkable(self, x: int, y: int) -> bool:
        # Wrap horizontally at tunnel row
        if y == self.tunnels_row:
            x = x % self.cols
        if not (0 <= y < self.rows and 0 <= x < self.cols):
            return False
        return self.grid[y][x] in PACMAN_WALKABLE

    def is_ghost_walkable(self, x: int, y: int) -> bool:
        if y == self.tunnels_row:
            x = x % self.cols
        if not (0 <= y < self.rows and 0 <= x < self.cols):
            return False
        return self.grid[y][x] in GHOST_WALKABLE

    def is_door(self, x: int, y: int) -> bool:
        return (x, y) in self.ghost_door

    def consume_pellet(self, tile: tuple[int, int]) -> str | None:
        if tile in self.pellets:
            self.pellets.discard(tile)
            return "pellet"
        if tile in self.power_pellets:
            self.power_pellets.discard(tile)
            return "power"
        return None

    def pellets_left(self) -> int:
        return len(self.pellets) + len(self.power_pellets)

    def pellets_eaten(self) -> int:
        return self.initial_pellet_count - self.pellets_left()

    def reset_pellets(self) -> None:
        self.pellets.clear()
        self.power_pellets.clear()
        for y, row in enumerate(self.grid):
            for x, ch in enumerate(row):
                if ch == PELLET:
                    self.pellets.add((x, y))
                elif ch == POWER:
                    self.power_pellets.add((x, y))

    def neighbours(self, x: int, y: int, *, for_ghost: bool) -> Iterable[tuple[int, int]]:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            ok = self.is_ghost_walkable(nx, ny) if for_ghost else self.is_pacman_walkable(nx, ny)
            if ok:
                yield (nx, ny)
