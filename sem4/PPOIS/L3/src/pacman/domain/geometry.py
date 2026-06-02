import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Vec2:
    x: float
    y: float

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, k: float) -> "Vec2":
        return Vec2(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __neg__(self) -> "Vec2":
        return Vec2(-self.x, -self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec2):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def length2(self) -> float:
        return self.x * self.x + self.y * self.y

    def dist(self, other: "Vec2") -> float:
        return (self - other).length()

    def dist2(self, other: "Vec2") -> float:
        return (self - other).length2()

    def as_int_tile(self) -> tuple[int, int]:
        return (int(self.x), int(self.y))


ZERO = Vec2(0, 0)
LEFT = Vec2(-1, 0)
RIGHT = Vec2(1, 0)
UP = Vec2(0, -1)
DOWN = Vec2(0, 1)
DIRECTIONS: tuple[Vec2, ...] = (UP, LEFT, DOWN, RIGHT)

def opposite(d: Vec2) -> Vec2:
    return Vec2(-d.x, -d.y)


def dir_name(d: Vec2) -> str:
    if d == LEFT:
        return "left"
    if d == RIGHT:
        return "right"
    if d == UP:
        return "up"
    if d == DOWN:
        return "down"
    return "right"
