import pygame

from ..domain.game import Game, GamePhase
from ..domain.geometry import DOWN, LEFT, RIGHT, UP
from ..domain.maze import Maze
from .base import Scene


KEY_TO_DIR = {
    pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
    pygame.K_UP: UP, pygame.K_w: UP,
    pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
}


class GameScene(Scene):
    def __init__(self, ctx, map_path: str) -> None:
        super().__init__(ctx)
        self.map_path = map_path
        self.maze = Maze.load(map_path)
        self.game = Game(self.maze, ctx.config, high_score=ctx.highscores.top_score())
        self.paused = False
        self._game_over_delay = 0.0

    def enter(self) -> None:
        self.ctx.sounds.stop_music()
        self.ctx.sounds.play("ready")

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key in KEY_TO_DIR:
            self.game.request_direction(KEY_TO_DIR[event.key])
        elif event.key == pygame.K_ESCAPE:
            from .menu import MenuScene
            self.next_scene = MenuScene(self.ctx)
        elif event.key in (pygame.K_p, pygame.K_SPACE):
            self.paused = not self.paused

    def update(self, dt: float) -> None:
        if self.paused:
            return

        dt = min(dt, 1 / 30)
        events = self.game.step(dt)
        for ev in events:
            self._handle_event(ev)

        if self.game.phase is GamePhase.GAME_OVER:
            self._game_over_delay += dt
            if self._game_over_delay >= 2.0:
                self._finish()

    def draw(self, screen: pygame.Surface) -> None:
        snap = self.game.snapshot()
        self.ctx.renderer.draw(screen, snap, 0.0 if self.paused else 1 / 60)
        if self.paused:
            self._draw_pause_overlay(screen)

    def _draw_pause_overlay(self, screen: pygame.Surface) -> None:
        W, H = screen.get_size()
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))
        txt = self.ctx.renderer.font_big.render("PAUSED", True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=(W // 2, H // 2)))
        hint = self.ctx.renderer.font_small.render("P/SPACE — resume,  ESC — menu",
                                                    True, (200, 200, 200))
        screen.blit(hint, hint.get_rect(center=(W // 2, H // 2 + 40)))

    def _handle_event(self, ev) -> None:
        s = self.ctx.sounds
        k = ev.kind
        if k == "pellet":
            s.play("chomp")
        elif k == "power":
            s.play("power")
        elif k == "ghost_eaten":
            s.play("ghost_eat")
        elif k == "fruit_eaten":
            s.play("fruit")
        elif k == "pacman_died":
            s.play("death")
        elif k == "extra_life":
            s.play("extra_life")
        elif k == "level_clear":
            s.play("level_clear")

    def _finish(self) -> None:
        score = self.game.score
        map_name = self.maze.name
        if self.ctx.highscores.is_new_top(score):
            from .name_entry import NameEntryScene
            self.next_scene = NameEntryScene(self.ctx, score, map_name)
        else:
            if (len(self.ctx.highscores.entries) < self.ctx.highscores.limit
                    or score > self.ctx.highscores.entries[-1]["points"]):
                self.ctx.highscores.add("PLAYER", score, map_name)
            from .high_scores import HighScoresScene
            self.next_scene = HighScoresScene(self.ctx)
