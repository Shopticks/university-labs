import pygame

from .base import Scene


class MapSelectScene(Scene):
    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.maps = list(ctx.config["maps"])
        self.idx = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_UP, pygame.K_w, pygame.K_LEFT, pygame.K_a):
            self.idx = (self.idx - 1) % len(self.maps)
            self.ctx.sounds.play("menu_move")
        elif event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_RIGHT, pygame.K_d):
            self.idx = (self.idx + 1) % len(self.maps)
            self.ctx.sounds.play("menu_move")
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.ctx.sounds.play("menu_pick")
            from .game import GameScene
            self.next_scene = GameScene(self.ctx, map_path=self.maps[self.idx]["path"])
        elif event.key == pygame.K_ESCAPE:
            from .menu import MenuScene
            self.next_scene = MenuScene(self.ctx)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        W, _ = screen.get_size()
        font_big = self.ctx.renderer.font_big
        font_med = self.ctx.renderer.font_med
        font_small = self.ctx.renderer.font_small

        title = font_big.render("SELECT MAP", True, (255, 255, 0))
        screen.blit(title, title.get_rect(center=(W // 2, 80)))

        y = 200
        for i, m in enumerate(self.maps):
            sel = (i == self.idx)
            color = (255, 255, 0) if sel else (220, 220, 220)
            prefix = ">  " if sel else "   "
            img = font_med.render(prefix + m["name"], True, color)
            screen.blit(img, img.get_rect(center=(W // 2, y)))
            y += 48

        hint = font_small.render("UP/DOWN — choose,  ENTER — start,  ESC — back",
                                  True, (140, 140, 140))
        screen.blit(hint, hint.get_rect(center=(W // 2, screen.get_height() - 28)))
