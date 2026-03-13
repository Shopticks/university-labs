from decimal import Decimal
import os

from src.exceptions import MetroSystemError, StationError
from src.domain.models.money import Money
from src.domain.models.ticket_office import TicketOffice
from src.domain.models.ticket import TicketType
from src.domain.models.turnstile import Turnstile
from src.domain.models.platform import Platform
from src.domain.models.station import Station
from src.domain.models.route import Route, RouteStop
from src.domain.models.train import Train
from src.domain.models.passenger import Passenger

from src.application.transit import TransitService
from src.application.sales import SalesService

from src.application.state import AppState
from src.infrastructure.storage import StorageService, setup_world
from src.presentation.cli_utils import print_header, get_int, get_decimal, get_string, get_name, select_item


def _find_passenger_location(state: AppState, passenger: Passenger) -> tuple[str, str] | None:
    """Return (kind, description) if the passenger is somewhere in the system, else None.

    kind: 'concourse' | 'platform' | 'train'
    """
    for station in state.stations.values():
        if passenger in station.concourse_passengers:
            return ('concourse', f"concourse of {station.name}")
        for platform in station.platforms:
            if passenger in platform.waiting_passengers:
                return ('platform', f"platform {platform.number} at {station.name}")
    for train in state.trains.values():
        if passenger in train.passengers:
            return ('train', f"train {train.id}")
    return None


# -- Passenger menu ---

def handle_passenger_menu(state: AppState):
    while True:
        print_header("PASSENGER MANAGEMENT")
        print("1. Create passenger")
        print("2. Buy ticket at ticket office")
        print("3. Pass through turnstile (enter station)")
        print("4. Route to platform")
        print("0. Back")

        choice = get_int("\nSelect action: ", 0, 4)
        if choice == 1:
            _action_spawn_passenger(state)
        elif choice == 2:
            _action_buy_ticket(state)
        elif choice == 3:
            _action_enter_station(state)
        elif choice == 4:
            _action_route_to_platform(state)
        elif choice == 0:
            break


def _action_spawn_passenger(state: AppState):
    print("\n--- Create Passenger ---")
    p_id = get_string("Enter passenger ID (e.g., P2): ")
    if p_id in state.passengers:
        print("[Error] Passenger with this ID already exists.")
        return

    name = get_name("Enter passenger name: ")

    stations_list = list(state.stations.values())
    if not stations_list:
        print("[Error] No stations exist yet. Create a station first.")
        return

    dest_station = select_item(
        stations_list,
        lambda s: f"{s.id} ({s.name})",
        "destination station",
    )
    if not dest_station:
        return

    passenger = Passenger(p_id, name, dest_station.id)
    state.passengers[p_id] = passenger
    print(f"[Success] Passenger '{name}' ({p_id}) created. Destination: {dest_station.name}.")


def _action_buy_ticket(state: AppState):
    passenger = select_item(
        list(state.passengers.values()),
        lambda p: f"{p.id} ({p.name})",
        "passenger",
    )
    if not passenger:
        return

    if passenger.ticket:
        valid_str = "valid" if passenger.ticket.is_valid else "expired/exhausted"
        print(f"[Warning] Passenger already has ticket {passenger.ticket.id} ({valid_str}).")
        confirm = get_int("Replace it? (1=Yes / 0=No): ", 0, 1)
        if confirm == 0:
            return

    station = select_item(
        list(state.stations.values()),
        lambda s: f"{s.id} ({s.name})",
        "station",
    )
    if not station:
        return

    offices = station.ticket_offices
    if not offices:
        print("[Error] No ticket offices at this station.")
        return

    office = select_item(
        offices,
        lambda o: f"Office {o.id} (Balance: {o.balance})",
        "ticket office",
    )
    if not office:
        return

    print("\nSelect ticket type:")
    print("1. By Trips")
    print("2. Daily    (4.00 BYN)")
    print("3. Weekly   (10.00 BYN)")
    print("4. Monthly  (38.00 BYN)")
    t_choice = get_int("Choice: ", 1, 4)

    t_mapping = {
        1: TicketType.BY_TRIPS,
        2: TicketType.DAILY,
        3: TicketType.WEEKLY,
        4: TicketType.MONTHLY,
    }
    ticket_type = t_mapping[t_choice]

    trips = 0
    if ticket_type == TicketType.BY_TRIPS:
        # Restrict to catalog options only
        print("Select number of trips:")
        print("1. 1 trip  (0.90 BYN)")
        print("2. 5 trips (4.30 BYN)")
        print("3. 10 trips (8.10 BYN)")
        trips_choice = get_int("Choice: ", 1, 3)
        trips = {1: 1, 2: 5, 3: 10}[trips_choice]

    try:
        price = office.get_price(ticket_type, trips)
    except MetroSystemError as e:
        print(f"[Error] {e}")
        return

    print(f"\n--- TICKET PURCHASE ---")
    print(f"  Passenger : {passenger.name}")
    print(f"  Type      : {ticket_type.value}" + (f" × {trips}" if trips else ""))
    print(f"  Price     : {price}")

    amount = get_decimal(f"Enter tendered amount (min {price.amount} BYN): ", float(price.amount))

    try:
        ticket, change = SalesService.process_ticket_purchase(
            passenger, office, ticket_type, trips, Money(amount)
        )
        print(f"\n  Ticket issued : {ticket.id}")
        if change.amount > 0:
            print(f"  Change        : {change}")
        print(f"  Office balance: {office.balance}")
        print("[Success] Transaction complete.")
    except MetroSystemError as e:
        print(f"[Business Error] {e}")


def _action_enter_station(state: AppState):
    passenger = select_item(
        list(state.passengers.values()),
        lambda p: f"{p.id} ({p.name})",
        "passenger",
    )
    if not passenger:
        return

    if not passenger.ticket:
        print("[Error] Passenger has no ticket. Buy a ticket first.")
        return

    if not passenger.ticket.is_valid:
        print("[Error] Passenger's ticket is no longer valid (expired or exhausted).")
        return

    location = _find_passenger_location(state, passenger)
    if location:
        print(f"[Error] Passenger is already at {location[1]}.")
        return

    station = select_item(
        list(state.stations.values()),
        lambda s: f"{s.id} ({s.name})",
        "station",
    )
    if not station:
        return

    if not station.turnstiles:
        print(f"[Error] Station {station.name} has no turnstiles.")
        return

    turnstile = select_item(
        station.turnstiles,
        lambda t: f"Turnstile {t.id} [{t.state.value}]",
        "turnstile",
    )
    if not turnstile:
        return

    try:
        TransitService.process_turnstile_passage(passenger.ticket, turnstile)
        station.enter_concourse(passenger)
        print(f"[Success] {passenger.name} entered the concourse of {station.name}.")
    except MetroSystemError as e:
        print(f"[Error] {e}")


def _action_route_to_platform(state: AppState):
    passenger = select_item(
        list(state.passengers.values()),
        lambda p: f"{p.id} ({p.name})",
        "passenger",
    )
    if not passenger:
        return

    home_station: Station | None = None
    for station in state.stations.values():
        if passenger in station.concourse_passengers:
            home_station = station
            break

    if home_station is None:
        print("[Error] Passenger is not in any station concourse. They must enter a station first.")
        return

    print(f"[Info] Passenger is in the concourse of {home_station.name}.")

    if not home_station.platforms:
        print(f"[Error] Station {home_station.name} has no platforms.")
        return

    platform = select_item(
        home_station.platforms,
        lambda p: f"Platform {p.number} ({len(p.waiting_passengers)} waiting)",
        "platform",
    )
    if not platform:
        return

    try:
        home_station.route_to_platform(passenger, platform.number)
        print(f"[Success] {passenger.name} is now waiting on platform {platform.number} at {home_station.name}.")
    except MetroSystemError as e:
        print(f"[Error] {e}")


# -- Train menu ---

def handle_train_menu(state: AppState):
    while True:
        print_header("TRAIN MANAGEMENT")
        print("1. Add new train")
        print("2. Dispatch train to route")
        print("3. Maintain train")
        print("0. Back")

        choice = get_int("\nSelect action: ", 0, 3)
        if choice == 1:
            _action_create_train(state)
        elif choice == 2:
            _action_dispatch_train(state)
        elif choice == 3:
            _action_maintain_train(state)
        elif choice == 0:
            break


def _action_create_train(state: AppState):
    print("\n--- Add Train ---")
    t_id = get_string("Enter train ID (e.g., TR-02): ")
    if t_id in state.trains:
        print("[Error] Train with this ID already exists.")
        return

    capacity = get_int("Enter train capacity: ", 10, 1000)
    stops_for_service = get_int("Stops before maintenance required: ", 1, 50)

    state.trains[t_id] = Train(t_id, capacity, stops_for_service)
    print(f"[Success] Train {t_id} (capacity: {capacity}, service interval: {stops_for_service}) added.")


def _action_dispatch_train(state: AppState):
    dispatched_ids = {d.train.id for d in state.schedule.active_dispatches}
    available = [t for t in state.trains.values() if t.id not in dispatched_ids]

    train = select_item(
        available,
        lambda t: f"{t.id} [State: {t.state.value}, Wear: {t.stops_count}/{t.stops_for_service}]",
        "train",
    )
    if not train:
        return

    if not state.routes:
        print("[Error] No routes exist yet.")
        return

    route = select_item(
        list(state.routes.values()),
        lambda r: f"{r.id} ({r.name})",
        "route",
    )
    if not route:
        return

    try:
        state.schedule.dispatch_train(train, route)
        print(f"[Success] Train {train.id} dispatched to route '{route.name}'.")
    except MetroSystemError as e:
        print(f"[Error] {e}")


def _action_maintain_train(state: AppState):
    train = select_item(
        list(state.trains.values()),
        lambda t: f"{t.id} (Wear: {t.stops_count}/{t.stops_for_service})",
        "train",
    )
    if not train:
        return

    try:
        train.maintain()
        print(f"[Success] Train {train.id} maintenance complete. Wear counter reset.")
    except MetroSystemError as e:
        print(f"[Error] {e}")

# --- Route menu ---

def handle_route_menu(state: AppState):
    while True:
        print_header("ROUTE MANAGEMENT")
        print("1. Create new route")
        print("2. View existing routes")
        print("0. Back")

        choice = get_int("\nSelect action: ", 0, 2)
        if choice == 1:
            _action_create_route(state)
        elif choice == 2:
            _action_view_routes(state)
        elif choice == 0:
            break


def _action_create_route(state: AppState):
    print("\n--- Configure New Route ---")

    if not state.stations:
        print("[Error] No stations exist yet. Create at least 2 stations first.")
        return

    r_id = get_string("Enter route ID (e.g., R2): ")
    if r_id in state.routes:
        print("[Error] Route with this ID already exists.")
        return

    r_name = get_string("Enter route name (e.g., Red Line): ")
    route = Route(r_id, r_name)

    print("\nAdd stops one by one. Enter '0' when done (min 2 stops required).")
    stop_index = 1
    last_station_id = None

    while True:
        print(f"\n--- Stop #{stop_index} ---")
        station = select_item(
            list(state.stations.values()),
            lambda s: f"{s.id} ({s.name})",
            "station",
        )
        if not station:
            if stop_index > 2:
                break
            else:
                print("[Error] A route requires at least 2 stops.")
                continue

        if station.id == last_station_id:
            print("[Error] Cannot select the same station consecutively.")
            continue

        if not station.platforms:
            print(f"[Error] Station {station.name} has no platforms. Add a platform first.")
            continue

        platform = select_item(
            station.platforms,
            lambda p: f"Platform {p.number}",
            "platform",
        )
        if not platform:
            continue

        is_last = get_int("Is this the terminal stop? (1=Yes / 0=No): ", 0, 1)
        travel_time = 0
        if not is_last:
            travel_time = get_int("Travel time to next station (minutes): ", 1, 120)

        route.add_stop(RouteStop(station, platform.number, travel_time))
        last_station_id = station.id
        stop_index += 1

        if is_last:
            print("[Info] Terminal stop added.")
            break

    if len(route.stops) >= 2:
        state.routes[r_id] = route
        print(f"[Success] Route '{r_name}' created with {len(route.stops)} stops.")
    else:
        print("[Error] Route not saved: need at least 2 stops.")


def _action_view_routes(state: AppState):
    if not state.routes:
        print("\nNo routes available.")
        return

    print()
    for r in state.routes.values():
        print(f"Route {r.id} — {r.name}")
        for idx, stop in enumerate(r.stops, 1):
            arrow = f" → {stop.travel_time_to_next} min" if stop.travel_time_to_next > 0 else " (terminal)"
            print(f"  {idx}. {stop.station.name} (platform {stop.platform_number}){arrow}")


# --- STation menu ---

def handle_station_menu(state: AppState):
    while True:
        print_header("STATION MANAGEMENT")
        print("1. Create station")
        print("2. Add platform")
        print("3. Add turnstile")
        print("4. Add ticket office")
        print("5. Security: lockdown / lift lockdown")
        print("0. Back")

        choice = get_int("\nSelect action: ", 0, 5)
        if choice == 1:
            _create_station(state)
        elif choice == 2:
            _add_platform(state)
        elif choice == 3:
            _add_turnstile(state)
        elif choice == 4:
            _add_ticket_office(state)
        elif choice == 5:
            _manage_lockdown(state)
        elif choice == 0:
            break


def _create_station(state: AppState):
    print("\n--- Create Station ---")
    s_id = get_string("Enter station ID (e.g., S3): ")
    if s_id in state.stations:
        print("[Error] Station with this ID already exists.")
        return

    name = get_string("Enter station name: ")
    state.stations[s_id] = Station(s_id, name)
    print(f"[Success] Station '{name}' ({s_id}) created.")


def _add_platform(state: AppState):
    if not state.stations:
        print("[Error] No stations exist yet.")
        return

    station = select_item(
        list(state.stations.values()),
        lambda s: f"{s.id} ({s.name})",
        "station",
    )
    if not station:
        return

    p_id = get_string("Enter platform ID (e.g., P3): ")
    p_num = get_int("Enter platform number: ", 1, 100)

    try:
        station.get_platform(p_num)
        print(f"[Error] Platform {p_num} already exists at {station.name}.")
        return
    except StationError:
        pass

    station.add_platform(Platform(p_id, p_num))
    print(f"[Success] Platform {p_num} added to {station.name}.")


def _add_turnstile(state: AppState):
    if not state.stations:
        print("[Error] No stations exist yet.")
        return

    station = select_item(
        list(state.stations.values()),
        lambda s: f"{s.id} ({s.name})",
        "station",
    )
    if not station:
        return

    t_id = get_string("Enter turnstile ID (e.g., TUR-3): ")
    station.add_turnstile(Turnstile(t_id))
    print(f"[Success] Turnstile {t_id} added to {station.name}.")


def _add_ticket_office(state: AppState):
    if not state.stations:
        print("[Error] No stations exist yet.")
        return

    station = select_item(
        list(state.stations.values()),
        lambda s: f"{s.id} ({s.name})",
        "station",
    )
    if not station:
        return

    o_id = get_string("Enter ticket office ID (e.g., O3): ")
    station.add_ticket_office(TicketOffice(o_id))
    print(f"[Success] Ticket office {o_id} added to {station.name}.")


def _manage_lockdown(state: AppState):
    if not state.stations:
        print("[Error] No stations exist yet.")
        return

    station = select_item(
        list(state.stations.values()),
        lambda s: f"{s.id} ({s.name})",
        "station",
    )
    if not station:
        return

    print(f"\nStation: {station.name}")
    print("1. Initiate lockdown")
    print("2. Lift lockdown")
    print("0. Cancel")

    action = get_int("Select: ", 0, 2)
    if action == 1:
        station.lockdown()
        print(f"[Success] Lockdown initiated at {station.name}. All turnstiles locked down.")
    elif action == 2:
        station.lift_lockdown()
        print(f"[Success] Lockdown lifted at {station.name}.")


# --- Simulation and status ---

def handle_simulation_menu(state: AppState):
    while True:
        print_header("TIME SIMULATION")
        print(f"Current time: {state.schedule.current_time_str}")
        print("1. Advance time (tick)")
        print("0. Back")

        choice = get_int("\nSelect action: ", 0, 1)
        if choice == 1:
            minutes = get_int("Minutes to advance: ", 1, 1440)
            for _ in range(minutes):
                state.schedule.tick()
            print(f"\n[Info] Time is now {state.schedule.current_time_str}.")
        elif choice == 0:
            break


def handle_status_menu(state: AppState):
    while True:
        print_header("SYSTEM STATUS")
        print(f"Time: {state.schedule.current_time_str}")
        print("1. Passengers")
        print("2. Trains")
        print("3. Stations")
        print("4. Active dispatches")
        print("0. Back")

        choice = get_int("\nSelect: ", 0, 4)
        if choice == 1:
            _status_passengers(state)
        elif choice == 2:
            _status_trains(state)
        elif choice == 3:
            _status_stations(state)
        elif choice == 4:
            _status_dispatches(state)
        elif choice == 0:
            break


def _status_passengers(state: AppState):
    if not state.passengers:
        print("\nNo passengers.")
        return
    print()
    for p in state.passengers.values():
        t_info = f"Ticket: {p.ticket.id} ({'valid' if p.ticket.is_valid else 'invalid'})" if p.ticket else "No ticket"
        location = _find_passenger_location(state, p)
        loc_info = f" | At: {location[1]}" if location else " | Location: outside"
        print(f"  {p.id} ({p.name}) | Dest: {p.destination_station_id} | {t_info}{loc_info}")


def _status_trains(state: AppState):
    if not state.trains:
        print("\nNo trains.")
        return
    print()
    dispatched_ids = {d.train.id for d in state.schedule.active_dispatches}
    for t in state.trains.values():
        dispatch_info = " [DISPATCHED]" if t.id in dispatched_ids else ""
        print(f"  {t.id} | {t.state.value} | {t.passenger_count}/{t.capacity} pax | Wear: {t.stops_count}/{t.stops_for_service}{dispatch_info}")


def _status_stations(state: AppState):
    if not state.stations:
        print("\nNo stations.")
        return
    print()
    for s in state.stations.values():
        lockdown_info = ""
        if s.turnstiles and all(t.state.value == "locked_down" for t in s.turnstiles):
            lockdown_info = " [LOCKDOWN]"
        print(f"  {s.name} ({s.id}){lockdown_info} | Concourse: {len(s.concourse_passengers)} pax")
        for p in s.platforms:
            print(f"    Platform {p.number}: {len(p.waiting_passengers)} waiting")


def _status_dispatches(state: AppState):
    dispatches = state.schedule.active_dispatches
    if not dispatches:
        print("\nNo active dispatches.")
        return
    print()
    for d in dispatches:
        stop = d.route.stops[d.current_stop_index]
        status = "at station" if d.is_dwelling else f"en route (timer: {d.timer})"
        print(f"  Train {d.train.id} | Route: {d.route.name} | Stop {d.current_stop_index + 1}/{len(d.route.stops)}: {stop.station.name} | {status}")


# --- system/json ---

def handle_system_menu(state: AppState, storage: StorageService):
    while True:
        print_header("SYSTEM (JSON)")
        print(f"Save file: {storage.filepath}")
        print("1. Save state")
        print("2. Load state")
        print("3. Reset to defaults")
        print("0. Back")

        choice = get_int("\nSelect action: ", 0, 3)
        if choice == 1:
            storage.save(state)
        elif choice == 2:
            storage.load(state)
        elif choice == 3:
            confirm = get_int("Confirm reset? All unsaved data will be lost. (1=Yes / 0=No): ", 0, 1)
            if confirm == 1:
                setup_world(state)
                print("[Success] System reset to defaults.")
        elif choice == 0:
            break