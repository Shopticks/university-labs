import pygame

from .base import Scene


class HighScoresScene(Scene):
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN,
                                                          pygame.K_SPACE):
            from .menu import MenuScene
            self.next_scene = MenuScene(self.ctx)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        W, _ = screen.get_size()
        font_big = self.ctx.renderer.font_big
        font_med = self.ctx.renderer.font_med
        font_small = self.ctx.renderer.font_small

        title = font_big.render("HIGH SCORES", True, (255, 255, 0))
        screen.blit(title, title.get_rect(center=(W // 2, 60)))

        entries = self.ctx.highscores.entries
        if not entries:
            empty = font_med.render("No records yet — go play!", True, (200, 200, 200))
            screen.blit(empty, empty.get_rect(center=(W // 2, 200)))
        else:
            y = 130
            header = font_small.render("RANK  NAME           POINTS  MAP",
                                        True, (140, 140, 140))
            screen.blit(header, header.get_rect(center=(W // 2, y)))
            y += 28
            for i, e in enumerate(entries[:10], 1):
                line = f"{i:>2}.  {e['name']:<12}  {e['points']:>7}  {e['map']}"
                color = (255, 255, 0) if i == 1 else (240, 240, 240)
                img = font_small.render(line, True, color)
                screen.blit(img, img.get_rect(center=(W // 2, y)))
                y += 22

        hint = font_small.render("ESC / ENTER — back", True, (140, 140, 140))
        screen.blit(hint, hint.get_rect(center=(W // 2, screen.get_height() - 28)))
