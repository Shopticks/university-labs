from typing import Optional

import pygame

from .config import load_config
from .highscores import HighScores
from .presentation.assets import AssetLoader
from .presentation.renderer import Renderer
from .presentation.sounds import SoundManager
from .scenes.base import Scene
from .scenes.menu import MenuScene


class Context:
    def __init__(self, config: dict) -> None:
        self.config = config
        win = config["window"]
        self.tile = int(win["tile"])
        self.screen_size = (int(win["width"]), int(win["height"]))
        self.fps = int(win["fps"])
        self.assets = AssetLoader(root="assets/images", tile=self.tile)
        self.sounds = SoundManager(
            root="assets/sounds",
            sfx_vol=float(config["audio"]["sfx_volume"]),
            music_vol=float(config["audio"]["music_volume"]),
        )
        self.highscores = HighScores(
            path=config.get("highscores_path", "save/highscores.json"),
            limit=int(config.get("highscores_limit", 10)),
        )
        self.renderer: Renderer
        self.quit_flag = False

    def quit(self) -> None:
        self.quit_flag = True


class App:
    def __init__(self, config_path: str = "config/game.json") -> None:
        cfg = load_config(config_path)
        pygame.init()
        self.ctx = Context(cfg)
        self.screen = pygame.display.set_mode(self.ctx.screen_size)
        pygame.display.set_caption(cfg["window"]["title"])
        self.ctx.renderer = Renderer(
            assets=self.ctx.assets,
            tile=self.ctx.tile,
            screen_size=self.ctx.screen_size,
            cfg=cfg,
        )
        self.clock = pygame.time.Clock()
        self.scene: Optional[Scene] = MenuScene(self.ctx)
        self.scene.enter()

    def run(self) -> None:
        running = True
        while running and self.scene is not None and not self.ctx.quit_flag:
            dt = self.clock.tick(self.ctx.fps) / 1000.0 # To seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                self.scene.handle_event(event)
            if not running:
                break

            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()

            nxt = self.scene.next_scene
            if nxt is not None:
                self.scene.leave()
                self.scene = nxt
                self.scene.next_scene = None
                self.scene.enter()

        pygame.quit()
