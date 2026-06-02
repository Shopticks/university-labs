from __future__ import annotations

from pathlib import Path

import pygame


class AssetLoader:
    def __init__(self, root: str | Path = "assets/images", tile: int = 24) -> None:
        self._root = Path(root)
        self._cache: dict[str, pygame.Surface] = {}
        self.tile = tile

    def __call__(self, name: str) -> pygame.Surface:
        if name not in self._cache:
            path = self._root / name
            surf = pygame.image.load(str(path)).convert_alpha()
            if surf.get_width() != self.tile:
                surf = pygame.transform.smoothscale(surf, (self.tile, self.tile))
            self._cache[name] = surf
        return self._cache[name]

    def font(self, size: int) -> pygame.font.Font:
        return pygame.font.SysFont("PressStart2P,Menlo,Monaco,Courier", size, bold=True)


class Animator:
    def __init__(self, frames: list[pygame.Surface], fps: float) -> None:
        self.frames = frames
        self.duration = 1.0 / min(fps, 2)
        self._t = 0.0
        self._i = 0

    def update(self, dt: float) -> None:
        self._t += dt
        while self._t >= self.duration:
            self._t -= self.duration
            self._i = (self._i + 1) % len(self.frames)

    @property
    def image(self) -> pygame.Surface:
        return self.frames[self._i]

    @property
    def index(self) -> int:
        return self._i
