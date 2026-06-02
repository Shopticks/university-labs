import pygame

from .base import Scene


HELP_LINES = [
    "PAC-MAN — RULES",
    "",
    "Eat every pellet on the map to clear the level.",
    "Power pellets (the big ones) scare ghosts for a few seconds —",
    "while frightened, ghosts can be eaten for bonus points.",
    "",
    "GHOSTS — each behaves differently:",
    "  BLINKY (red)    chases you directly",
    "  PINKY  (pink)   aims 4 tiles ahead of you",
    "  INKY   (cyan)   moves erratically, anchored to BLINKY",
    "  CLYDE  (orange) chases until close, then runs to his corner",
    "",
    "FRUITS — appear in the centre after some pellets eaten:",
    "  CHERRY     (100) — Pac-Man gets a speed boost",
    "  STRAWBERRY (300) — ghosts freeze for several seconds",
    "",
    "CONTROLS:",
    "  ARROWS / WASD — move",
    "  P / SPACE     — pause",
    "  ESC           — back to menu",
    "",
    "Hit ESC to return.",
]


class HelpScene(Scene):
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN,
                                                          pygame.K_SPACE):
            from .menu import MenuScene
            self.next_scene = MenuScene(self.ctx)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        font_big = self.ctx.renderer.font_big
        font_small = self.ctx.renderer.font_small
        W, _ = screen.get_size()
        y = 32
        for i, line in enumerate(HELP_LINES):
            if i == 0:
                img = font_big.render(line, True, (255, 255, 0))
            else:
                color = (255, 255, 255) if line and not line.startswith(" ") else (200, 200, 200)
                img = font_small.render(line, True, color)
            screen.blit(img, img.get_rect(midtop=(W // 2, y)))
            y += img.get_height() + 6
