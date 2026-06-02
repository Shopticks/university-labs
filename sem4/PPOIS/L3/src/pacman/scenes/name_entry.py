import pygame

from .base import Scene


class NameEntryScene(Scene):
    """Shown after the player beats the top high-score. Asks for a name and
    saves it, then returns to the menu via the high-score table."""

    def __init__(self, ctx, score: int, map_name: str) -> None:
        super().__init__(ctx)
        self.score = score
        self.map_name = map_name
        self.text = ""
        self._cursor_t = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif event.key == pygame.K_RETURN:
            self.ctx.highscores.add(self.text or "AAA", self.score, self.map_name)
            self.ctx.sounds.play("menu_pick")
            from .high_scores import HighScoresScene
            self.next_scene = HighScoresScene(self.ctx)
        elif event.key == pygame.K_ESCAPE:
            from .menu import MenuScene
            self.next_scene = MenuScene(self.ctx)
        elif event.unicode and event.unicode.isprintable() and len(self.text) < 12:
            self.text += event.unicode

    def update(self, dt: float) -> None:
        self._cursor_t += dt

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        W, H = screen.get_size()
        font_big = self.ctx.renderer.font_big
        font_med = self.ctx.renderer.font_med
        font_small = self.ctx.renderer.font_small

        title = font_big.render("NEW HIGH SCORE!", True, (255, 255, 0))
        screen.blit(title, title.get_rect(center=(W // 2, H // 3)))

        score = font_med.render(f"{self.score} points", True, (255, 255, 255))
        screen.blit(score, score.get_rect(center=(W // 2, H // 3 + 56)))

        prompt = font_small.render("Enter your name and press ENTER:", True, (200, 200, 200))
        screen.blit(prompt, prompt.get_rect(center=(W // 2, H // 2 + 8)))

        cursor = "_" if int(self._cursor_t * 2) % 2 == 0 else " "
        box = font_big.render((self.text or "") + cursor, True, (255, 200, 100))
        screen.blit(box, box.get_rect(center=(W // 2, H // 2 + 60)))
