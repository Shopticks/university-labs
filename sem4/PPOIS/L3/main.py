"""Pac-Man — entry point.

Run from project root:
    python main.py

Or as a module from src/:
    cd src && python -m pacman.main
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pacman.main import main

if __name__ == "__main__":
    main()
