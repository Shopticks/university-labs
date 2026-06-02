"""Pac-Man — PPOIS L3.

Layers:
  domain/         pure-Python game rules
  presentation/   pygame rendering, audio, animations
  scenes/         menu / map-select / game / help / high-scores state machine
  app.py          ties scenes + presentation together
  main.py         entry point
"""

__all__ = ["main"]


def main() -> None:  # pragma: no cover - thin shim
    from .main import main as _main
    _main()
