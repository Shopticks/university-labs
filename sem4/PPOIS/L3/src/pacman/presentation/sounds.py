import array
import math
import struct
from pathlib import Path

import pygame


class SoundManager:

    def __init__(self, root: str | Path = "assets/sounds", sfx_vol: float = 0.7,
                 music_vol: float = 0.35) -> None:
        self.root = Path(root)
        self.sfx_vol = sfx_vol
        self.music_vol = music_vol
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._enabled = True
        self._music_loaded: str | None = None
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        except pygame.error:
            self._enabled = False
            return
        pygame.mixer.set_num_channels(2)
        self._sfx_channel = pygame.mixer.Channel(0)
        self._prepare()

    def play(self, name: str) -> None:
        if not self._enabled:
            return
        snd = self._sounds.get(name)
        if snd is None:
            return
        if self._sfx_channel.get_busy():
            return
        snd.set_volume(self.sfx_vol)
        self._sfx_channel.play(snd)

    def stop_all(self) -> None:
        if not self._enabled:
            return
        pygame.mixer.stop()

    def play_music(self, name: str, loop: bool = True) -> None:
        if not self._enabled:
            return
        if self._music_loaded == name:
            return
        path = self.root / name
        if path.exists():
            try:
                pygame.mixer.music.load(str(path))
                pygame.mixer.music.set_volume(self.music_vol)
                pygame.mixer.music.play(-1 if loop else 0)
                self._music_loaded = name
                return
            except pygame.error:
                pass

        snd = self._make_tone(frequency=261.6, ms=350, kind="square", volume=0.15)
        snd.set_volume(self.music_vol)
        snd.play(loops=-1)
        self._music_loaded = name

    def stop_music(self) -> None:
        if not self._enabled:
            return
        pygame.mixer.music.stop()
        self._music_loaded = None

    def _prepare(self) -> None:
        specs = {
            "chomp":      {"files": ["Chomp.mp3"],
                            "freq": 660, "ms": 70,  "kind": "square"},
            "power":      {"files": [],
                            "freq": 220, "ms": 280, "kind": "saw"},
            "fruit":      {"files": ["Fruit.mp3"],
                            "freq": 900, "ms": 200, "kind": "sine"},
            "ghost_eat":  {"files": ["Ghost.mp3"],
                            "freq": 1400, "ms": 220, "kind": "square"},
            "death":      {"files": ["Death.mp3"],
                            "freq": 110, "ms": 1100, "kind": "saw", "slide": -90},
            "extra_life": {"files": ["Extra.mp3"],
                            "freq": 1320, "ms": 400, "kind": "sine"},
            "menu_move":  {"files": [],
                            "freq": 540, "ms": 50,  "kind": "square"},
            "menu_pick":  {"files": [],
                            "freq": 880, "ms": 120, "kind": "square"},
            "ready":      {"files": ["Intro.mp3"],
                            "freq": 440, "ms": 300, "kind": "sine"},
            "level_clear": {"files": ["Cutscene.mp3"],
                            "freq": 880, "ms": 120, "kind": "square"},
        }
        for name, spec in specs.items():
            loaded = False
            for fname in [*spec.get("files", []), f"{name}.wav"]:
                path = self.root / fname
                if not path.exists():
                    continue
                try:
                    self._sounds[name] = pygame.mixer.Sound(str(path))
                    loaded = True
                    break
                except pygame.error:
                    continue
            if loaded:
                continue
            self._sounds[name] = self._make_tone(
                frequency=spec["freq"],
                ms=spec["ms"],
                kind=spec.get("kind", "sine"),
                volume=0.35,
                slide=spec.get("slide", 0),
            )

    @staticmethod
    def _make_tone(frequency: float, ms: int, kind: str = "sine",
                   volume: float = 0.3, slide: float = 0.0) -> pygame.mixer.Sound:
        rate = 22050
        n = int(rate * ms / 1000)
        amp = int(32767 * volume)
        buf = array.array("h")
        for i in range(n):
            t = i / rate

            f = frequency + slide * (i / max(n, 1))
            phase = (f * t) % 1.0
            if kind == "square":
                s = 1.0 if phase < 0.5 else -1.0
            elif kind == "saw":
                s = 2.0 * phase - 1.0
            elif kind == "tri":
                s = 4.0 * abs(phase - 0.5) - 1.0
            else:
                s = math.sin(2 * math.pi * phase)

            fade = 1.0
            if i > 0.7 * n:
                fade = max(0.0, 1.0 - (i - 0.7 * n) / max(1, 0.3 * n))
            buf.append(int(amp * s * fade))
        snd = pygame.mixer.Sound(buffer=buf.tobytes())
        return snd
