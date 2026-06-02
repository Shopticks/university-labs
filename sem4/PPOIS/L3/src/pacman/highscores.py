import json
from pathlib import Path


class HighScores:
    def __init__(self, path: str | Path = "save/highscores.json", limit: int = 10) -> None:
        self.path = Path(path)
        self.limit = limit
        self.entries: list[dict] = []
        self.load()

    def load(self) -> None:
        if self.path.exists():
            try:
                raw = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(raw, list):
                    self.entries = [
                        {"name": str(e.get("name", "AAA"))[:12],
                         "points": int(e.get("points", 0)),
                         "map": str(e.get("map", "Classic"))}
                        for e in raw
                    ]
            except (json.JSONDecodeError, OSError):
                self.entries = []
        self._sort()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.entries, indent=2, ensure_ascii=False),
                              encoding="utf-8")

    def add(self, name: str, points: int, map_name: str = "Classic") -> None:
        self.entries.append({"name": (name or "AAA").strip()[:12] or "AAA",
                             "points": int(points),
                             "map": map_name})
        self._sort()
        self.save()

    def top_score(self) -> int:
        return self.entries[0]["points"] if self.entries else 0

    def is_new_top(self, points: int) -> bool:
        return points > self.top_score()

    def _sort(self) -> None:
        self.entries.sort(key=lambda e: -e["points"])
        self.entries = self.entries[: self.limit]
