import json
from pathlib import Path


def load_config(path: str | Path = "config/game.json") -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))
