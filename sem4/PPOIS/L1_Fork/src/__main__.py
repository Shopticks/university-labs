import sys
from src.presentation.app import MetroCLIApp

def main():
    try:
        app = MetroCLIApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nForced termination. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()