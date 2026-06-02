import math
from typing import Iterable

import pygame

from ..domain.game import Snapshot
from .assets import AssetLoader, Animator


PACMAN_DIRS = ("right", "left", "up", "down")
GHOSTS = ("blinky", "pinky", "inky", "clyde")


class Renderer:
    """
    Draws the snapshot. Stateful only with regard to animators and
    cached background surface.
    """

    def __init__(self, assets: AssetLoader, tile: int, screen_size: tuple[int, int],
                 cfg: dict) -> None:
        self.assets = assets
        self.tile = tile
        self.W, self.H = screen_size
        self.cfg = cfg
        self.maze_origin = (0, 0)
        self.bg: pygame.Surface | None = None
        self._bg_grid_id: int = -1
        self.sprite_size = max(tile + 2, (tile * 4) // 3)
        self._scaled_cache: dict[int, pygame.Surface] = {}

        self._pacman_anims = {
            d: Animator(
                frames=[assets(f"pacman_{d}_{i}.png") for i in (0, 1, 2)],
                fps=float(cfg["pacman"]["animation_fps"]),
            )
            for d in PACMAN_DIRS
        }
        self._pacman_death_frames = [assets(f"pacman_death_{i}.png") for i in range(11)]

        self._ghost_anims: dict[tuple[str, str], Animator] = {}
        for n in GHOSTS:
            for d in PACMAN_DIRS:
                self._ghost_anims[(n, d)] = Animator(
                    frames=[assets(f"ghost_{n}_{d}_{i}.png") for i in (0, 1)],
                    fps=float(cfg["ghosts"]["animation_fps"]),
                )
        self._frightened_anim = Animator(
            frames=[assets("ghost_frightened_0.png"), assets("ghost_frightened_1.png")],
            fps=float(cfg["ghosts"]["animation_fps"]),
        )
        self._frightened_white_anim = Animator(
            frames=[assets("ghost_frightened_white_0.png"),
                    assets("ghost_frightened_white_1.png")],
            fps=float(cfg["ghosts"]["animation_fps"]) * 2,
        )
        self.font_big = assets.font(28)
        self.font_med = assets.font(20)
        self.font_small = assets.font(14)

    def draw(self, screen: pygame.Surface, snap: Snapshot, dt: float) -> None:
        for a in self._pacman_anims.values():
            a.update(dt)
        for a in self._ghost_anims.values():
            a.update(dt)
        self._frightened_anim.update(dt)
        self._frightened_white_anim.update(dt)

        hud_h = 56
        screen.fill((0, 0, 0))
        self._draw_hud(screen, snap, hud_h)
        self.maze_origin = ((self.W - len(snap.grid[0]) * self.tile) // 2, hud_h)

        if self.bg is None or self._bg_grid_id != id(snap.grid):
            self._build_background(snap)
        screen.blit(self.bg, self.maze_origin)

        self._draw_pellets(screen, snap)

        # Fruit.
        if snap.fruit is not None:
            self._draw_fruit(screen, snap.fruit)

        # Ghosts.
        for g in snap.ghosts:
            self._draw_ghost(screen, g, snap)

        # Pacman.
        self._draw_pacman(screen, snap)

        # READY/GAME OVER overlay.
        if snap.ready_text:
            self._draw_overlay(screen, snap.ready_text)

    def _build_background(self, snap: Snapshot) -> None:
        rows = snap.grid
        h = len(rows) * self.tile
        w = len(rows[0]) * self.tile
        t = self.tile
        inset = max(2, t // 4)
        thick = max(2, t // 10)
        wall_color = (33, 33, 222)
        door_color = (255, 184, 222)

        def is_wall(x: int, y: int) -> bool:
            if y < 0 or y >= len(rows) or x < 0 or x >= len(rows[0]):
                return False
            return rows[y][x] == "X"

        outer = pygame.Surface((w, h), pygame.SRCALPHA)
        inner = pygame.Surface((w, h), pygame.SRCALPHA)
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch != "X":
                    continue
                px, py = x * t, y * t
                wn, ws = is_wall(x, y - 1), is_wall(x, y + 1)
                ww, we = is_wall(x - 1, y), is_wall(x + 1, y)

                ox = px + (0 if ww else inset)
                ex = px + (t if we else t - inset)
                oy = py + (0 if wn else inset)
                ey = py + (t if ws else t - inset)
                r = inset
                tl = r if (not wn and not ww) else 0
                tr = r if (not wn and not we) else 0
                bl = r if (not ws and not ww) else 0
                br = r if (not ws and not we) else 0
                pygame.draw.rect(
                    outer, wall_color, pygame.Rect(ox, oy, ex - ox, ey - oy),
                    border_top_left_radius=tl,
                    border_top_right_radius=tr,
                    border_bottom_left_radius=bl,
                    border_bottom_right_radius=br,
                )

                ix = ox + (thick if not ww else 0)
                ax = ex - (thick if not we else 0)
                iy = oy + (thick if not wn else 0)
                ay = ey - (thick if not ws else 0)
                if ax > ix and ay > iy:
                    ri = max(0, r - thick)
                    itl = ri if (not wn and not ww) else 0
                    itr = ri if (not wn and not we) else 0
                    ibl = ri if (not ws and not ww) else 0
                    ibr = ri if (not ws and not we) else 0
                    pygame.draw.rect(
                        inner, (0, 0, 0, 255),
                        pygame.Rect(ix, iy, ax - ix, ay - iy),
                        border_top_left_radius=itl,
                        border_top_right_radius=itr,
                        border_bottom_left_radius=ibl,
                        border_bottom_right_radius=ibr,
                    )

        r = inset
        ri = max(0, r - thick)
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch != "X":
                    continue
                px, py = x * t, y * t
                wn, ws = is_wall(x, y - 1), is_wall(x, y + 1)
                ww, we = is_wall(x - 1, y), is_wall(x + 1, y)
                specs = (
                    (wn and ww and not is_wall(x - 1, y - 1),
                     pygame.Rect(px, py, inset, inset),
                     (px + inset, py + inset)),
                    (wn and we and not is_wall(x + 1, y - 1),
                     pygame.Rect(px + t - inset, py, inset, inset),
                     (px + t - inset, py + inset)),
                    (ws and ww and not is_wall(x - 1, y + 1),
                     pygame.Rect(px, py + t - inset, inset, inset),
                     (px + inset, py + t - inset)),
                    (ws and we and not is_wall(x + 1, y + 1),
                     pygame.Rect(px + t - inset, py + t - inset, inset, inset),
                     (px + t - inset, py + t - inset)),
                )
                for cond, sq, center in specs:
                    if not cond:
                        continue
                    outer.fill((0, 0, 0, 0), sq)
                    inner.fill((0, 0, 0, 0), sq)
                    prev_o = outer.get_clip()
                    prev_i = inner.get_clip()
                    outer.set_clip(sq)
                    inner.set_clip(sq)
                    pygame.draw.circle(outer, wall_color, center, r)
                    if ri > 0:
                        pygame.draw.circle(inner, (0, 0, 0, 255), center, ri)
                    outer.set_clip(prev_o)
                    inner.set_clip(prev_i)

        outer.blit(inner, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.blit(outer, (0, 0))

        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch != "-":
                    continue
                px, py = x * t, y * t
                bar_h = max(2, t // 8)
                pygame.draw.rect(
                    surf, door_color,
                    pygame.Rect(px, py + (t - bar_h) // 2, t, bar_h),
                )
        self.bg = surf
        self._bg_grid_id = id(snap.grid)

    def _draw_pellets(self, screen: pygame.Surface, snap: Snapshot) -> None:
        pellet = self.assets("pellet.png")
        power = self.assets("power_pellet.png")
        ox, oy = self.maze_origin
        for (x, y) in snap.pellets:
            screen.blit(pellet, (ox + x * self.tile, oy + y * self.tile))

        blink = (pygame.time.get_ticks() // 250) % 2 == 0
        for (x, y) in snap.powers:
            if blink:
                screen.blit(power, (ox + x * self.tile, oy + y * self.tile))

    def _draw_fruit(self, screen: pygame.Surface, fruit: dict) -> None:
        kind = fruit["kind"]
        img = self.assets(f"{kind}.png")
        tx, ty = fruit["tile"]
        ox, oy = self.maze_origin
        screen.blit(img, (ox + tx * self.tile, oy + ty * self.tile))

    def _scaled(self, img: pygame.Surface) -> pygame.Surface:
        key = id(img)
        if key not in self._scaled_cache:
            self._scaled_cache[key] = pygame.transform.smoothscale(
                img, (self.sprite_size, self.sprite_size))
        return self._scaled_cache[key]

    def _draw_pacman(self, screen: pygame.Surface, snap: Snapshot) -> None:
        ox, oy = self.maze_origin
        s = self.sprite_size
        px = ox + int(round(snap.pacman_pos[0] * self.tile)) - s // 2
        py = oy + int(round(snap.pacman_pos[1] * self.tile)) - s // 2
        if snap.pacman_state == "dying":
            i = min(10, int(snap.pacman_death_progress * 11))
            img = self._pacman_death_frames[i]
        elif snap.pacman_state == "ready":
            img = self.assets("pacman_right_1.png")
        else:
            img = self._pacman_anims.get(snap.pacman_dir, self._pacman_anims["right"]).image
        screen.blit(self._scaled(img), (px, py))

    def _draw_ghost(self, screen: pygame.Surface, g: dict, snap: Snapshot) -> None:
        ox, oy = self.maze_origin
        s = self.sprite_size
        x = ox + int(round(g["pos"][0] * self.tile)) - s // 2
        y = oy + int(round(g["pos"][1] * self.tile)) - s // 2
        mode = g["mode"]
        d = g["dir"]
        if mode == "eaten":
            img = self.assets(f"ghost_eyes_{d}.png")
        elif mode == "frightened":
            blink_s = float(self.cfg["ghosts"]["frightened_blink_seconds"])
            remaining = snap.effect_remaining.get("frightened", 0.0)
            if 0 < remaining < blink_s:
                img = self._frightened_white_anim.image
            else:
                img = self._frightened_anim.image
        else:
            img = self._ghost_anims[(g["name"], d)].image
        screen.blit(self._scaled(img), (x, y))

    def _draw_hud(self, screen: pygame.Surface, snap: Snapshot, hud_h: int) -> None:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, self.W, hud_h))
        score_txt = self.font_med.render(f"SCORE {snap.score}", True, (255, 255, 0))
        screen.blit(score_txt, (12, 8))
        hi_txt = self.font_med.render(f"HIGH {snap.high_score}", True, (255, 255, 255))
        screen.blit(hi_txt, (self.W // 2 - hi_txt.get_width() // 2, 8))
        lvl_txt = self.font_small.render(f"LVL {snap.level}  MAP {snap.maze_name}", True, (180, 180, 180))
        screen.blit(lvl_txt, (self.W - lvl_txt.get_width() - 12, 10))

        pac_img = self.assets("pacman_right_1.png")
        for i in range(max(0, snap.lives - 1)):
            screen.blit(pac_img, (12 + i * (self.tile + 4), 30))

        ex, ey = self.W - 200, 30
        for kind in ("frightened", "speed_up", "freeze"):
            t = snap.effect_remaining.get(kind, 0.0)
            if t <= 0:
                continue
            label = {"frightened": "PWR", "speed_up": "SPD", "freeze": "FRZ"}[kind]
            color = {"frightened": (60, 60, 255), "speed_up": (255, 120, 0), "freeze": (60, 220, 255)}[kind]
            s = self.font_small.render(f"{label} {t:0.1f}s", True, color)
            screen.blit(s, (ex, ey))
            ex += s.get_width() + 12

    def _draw_overlay(self, screen: pygame.Surface, text: str) -> None:
        color = (255, 255, 0) if text != "GAME OVER" else (255, 80, 80)
        img = self.font_big.render(text, True, color)
        ox, oy = self.maze_origin
        bw = self.bg.get_width() if self.bg else screen.get_width()
        bh = self.bg.get_height() if self.bg else screen.get_height()
        screen.blit(img, img.get_rect(center=(ox + bw // 2, oy + bh // 2)))

    def text(self, s: str, size: int = 20, color=(255, 255, 255)) -> pygame.Surface:
        if size >= 26:
            f = self.font_big
        elif size >= 18:
            f = self.font_med
        else:
            f = self.font_small
        return f.render(s, True, color)
