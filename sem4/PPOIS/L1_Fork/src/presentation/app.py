import sys
from src.application.state import AppState
from src.presentation.cli_utils import print_header, get_int
from src.infrastructure.storage import StorageService, setup_world
from src.presentation.menus import (
    handle_passenger_menu,
    handle_train_menu,
    handle_route_menu,
    handle_station_menu,
    handle_simulation_menu,
    handle_status_menu,
    handle_system_menu,
)


class MetroCLIApp:
    def __init__(self):
        self.state = AppState()
        self.storage = StorageService(self.state.save_file)

        if not self.storage.load(self.state):
            setup_world(self.state)

    def run(self):
        try:
            self._main_loop()
        except KeyboardInterrupt:
            print("\n\nInterrupted.")
            self._shutdown()

    def _main_loop(self):
        while True:
            print_header("METRO 44 — MAIN MENU")
            print("1. Passenger Management")
            print("2. Train Management")
            print("3. Route Management")
            print("4. Station Management")
            print("5. Time Simulation")
            print("6. System Status")
            print("7. Save & Load (JSON)")
            print("0. Exit")

            choice = get_int("\nSelect: ", 0, 7)

            if choice == 1:
                handle_passenger_menu(self.state)
            elif choice == 2:
                handle_train_menu(self.state)
            elif choice == 3:
                handle_route_menu(self.state)
            elif choice == 4:
                handle_station_menu(self.state)
            elif choice == 5:
                handle_simulation_menu(self.state)
            elif choice == 6:
                handle_status_menu(self.state)
            elif choice == 7:
                handle_system_menu(self.state, self.storage)
            elif choice == 0:
                self._shutdown()

    def _shutdown(self):
        print("\nSaving state...")
        self.storage.save(self.state)
        print("Goodbye!")
        sys.exit(0)