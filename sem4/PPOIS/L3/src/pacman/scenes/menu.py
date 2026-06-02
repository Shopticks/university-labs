import math

import pygame

from .base import Scene


class MenuScene(Scene):
    ITEMS = [
        ("Start game", "start"),
        ("High scores", "scores"),
        ("Help", "help"),
        ("Exit", "exit"),
    ]

    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.idx = 0
        self._t = 0.0

    def enter(self) -> None:
        self.ctx.sounds.play_music("Cutscene.mp3")

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_UP, pygame.K_w):
            self.idx = (self.idx - 1) % len(self.ITEMS)
            self.ctx.sounds.play("menu_move")
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.idx = (self.idx + 1) % len(self.ITEMS)
            self.ctx.sounds.play("menu_move")
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.ctx.sounds.play("menu_pick")
            self._activate()
        elif event.key == pygame.K_ESCAPE:
            self.ctx.quit()

    def update(self, dt: float) -> None:
        self._t += dt

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        W, H = screen.get_size()
        font_big = self.ctx.renderer.font_big
        font_med = self.ctx.renderer.font_med
        font_small = self.ctx.renderer.font_small
        title = font_big.render("PAC-MAN", True, (255, 255, 0))
        # title pulse
        scale = 1.0 + 0.05 * math.sin(self._t * 3.5)
        sw, sh = int(title.get_width() * scale), int(title.get_height() * scale)
        title_s = pygame.transform.smoothscale(title, (sw, sh))
        screen.blit(title_s, title_s.get_rect(center=(W // 2, H // 4)))
        sub = font_small.render("PPOIS L3  /  pygame", True, (170, 170, 170))
        screen.blit(sub, sub.get_rect(center=(W // 2, H // 4 + sh // 2 + 16)))

        y = H // 2
        for i, (label, _key) in enumerate(self.ITEMS):
            sel = (i == self.idx)
            color = (255, 255, 0) if sel else (220, 220, 220)
            prefix = "> " if sel else "  "
            txt = font_med.render(prefix + label, True, color)
            screen.blit(txt, txt.get_rect(center=(W // 2, y)))
            y += 44

        hint = font_small.render("UP/DOWN — move,  ENTER — select,  ESC — quit",
                                  True, (140, 140, 140))
        screen.blit(hint, hint.get_rect(center=(W // 2, H - 28)))

    def _activate(self) -> None:
        from .high_scores import HighScoresScene
        from .help import HelpScene
        from .map_select import MapSelectScene

        key = self.ITEMS[self.idx][1]
        if key == "start":
            self.next_scene = MapSelectScene(self.ctx)
        elif key == "scores":
            self.next_scene = HighScoresScene(self.ctx)
        elif key == "help":
            self.next_scene = HelpScene(self.ctx)
        elif key == "exit":
            self.ctx.quit()
