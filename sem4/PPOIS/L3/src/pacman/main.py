import os
import sys
from pathlib import Path
from .app import App


def main() -> None:
    here = Path(__file__).resolve()
    candidates = [here.parent.parent.parent, Path.cwd()]
    for c in candidates:
        if (c / "config" / "game.json").exists():
            os.chdir(c)
            break

    App().run()


if __name__ == "__main__":
    main()
