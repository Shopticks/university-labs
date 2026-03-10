import json
import os
from datetime import datetime
from decimal import Decimal
from typing import Any

from src.application.schedule import ActiveDispatch, ScheduleService
from src.application.state import AppState
from src.domain.models.money import Money
from src.domain.models.passenger import Passenger
from src.domain.models.platform import Platform
from src.domain.models.route import Route, RouteStop
from src.domain.models.station import Station
from src.domain.models.ticket import Ticket, TicketType
from src.domain.models.ticket_office import TicketOffice
from src.domain.models.train import Train, TrainState
from src.domain.models.turnstile import Turnstile, TurnstileState


class MetroSerializer:
    """
    Converts domain objects to JSON-serializable dicts and reconstructs them from those dicts.
    """

    # --- Ticket ---

    @staticmethod
    def ticket_to_dict(ticket: Ticket) -> dict:
        return {
            "id": ticket.id,
            "type": ticket.ticket_type.value,
            "max_trips": ticket.max_trips,
            "current_trips": ticket.current_trips,
            "expires_at": ticket.expires_at.isoformat() if ticket.expires_at else None,
        }

    @staticmethod
    def ticket_from_dict(data: dict) -> Ticket:
        ticket = Ticket(
            ticket_id=data["id"],
            ticket_type=TicketType(data["type"]),
            max_trips=data["max_trips"],
            expires_at=datetime.fromisoformat(data["expires_at"]) if data["expires_at"] else None,
        )
        ticket._current_trips = data["current_trips"]
        return ticket

    # --- Passenger ---

    @staticmethod
    def passenger_to_dict(passenger: Passenger) -> dict:
        return {
            "id": passenger.id,
            "name": passenger.name,
            "destination_station_id": passenger.destination_station_id,
            "ticket": MetroSerializer.ticket_to_dict(passenger.ticket) if passenger.ticket else None,
        }

    @staticmethod
    def passenger_from_dict(data: dict) -> Passenger:
        passenger = Passenger(data["id"], data["name"], data["destination_station_id"])
        if data["ticket"] is not None:
            passenger.buy_ticket(MetroSerializer.ticket_from_dict(data["ticket"]))
        return passenger

    # --- Platform ---

    @staticmethod
    def platform_to_dict(platform: Platform) -> dict:
        return {
            "id": platform.id,
            "number": platform.number,
            # Store only IDs — passengers are reconstructed separately
            "waiting_passenger_ids": [p.id for p in platform.waiting_passengers],
        }

    @staticmethod
    def platform_from_dict(data: dict, passengers: dict[str, Passenger]) -> Platform:
        platform = Platform(data["id"], data["number"])
        for p_id in data["waiting_passenger_ids"]:
            if p_id not in passengers:
                raise KeyError(f"Passenger '{p_id}' referenced by platform '{data['id']}' was not found.")
            platform.add_passenger(passengers[p_id])
        return platform

    # --- Turnstile ---

    @staticmethod
    def turnstile_to_dict(turnstile: Turnstile) -> dict:
        return {
            "id": turnstile.id,
            "state": turnstile.state.value,
        }

    @staticmethod
    def turnstile_from_dict(data: dict) -> Turnstile:
        turnstile = Turnstile(data["id"])
        turnstile._state = TurnstileState(data["state"])
        return turnstile

    # --- TicketOffice ---

    @staticmethod
    def ticket_office_to_dict(office: TicketOffice) -> dict:
        return {
            "id": office.id,
            "balance": str(office.balance.amount),
        }

    @staticmethod
    def ticket_office_from_dict(data: dict) -> TicketOffice:
        office = TicketOffice(data["id"])
        office._balance = Money(Decimal(data["balance"]))
        return office

    # --- Station ---

    @staticmethod
    def station_to_dict(station: Station) -> dict:
        return {
            "id": station.id,
            "name": station.name,
            "platforms": [MetroSerializer.platform_to_dict(p) for p in station.platforms],
            "turnstiles": [MetroSerializer.turnstile_to_dict(t) for t in station.turnstiles],
            "ticket_offices": [MetroSerializer.ticket_office_to_dict(o) for o in station.ticket_offices],
            "concourse_passenger_ids": [p.id for p in station.concourse_passengers],
        }

    @staticmethod
    def station_from_dict(data: dict, passengers: dict[str, Passenger]) -> Station:
        station = Station(data["id"], data["name"])

        for p_data in data["platforms"]:
            station.add_platform(MetroSerializer.platform_from_dict(p_data, passengers))

        for t_data in data["turnstiles"]:
            station.add_turnstile(MetroSerializer.turnstile_from_dict(t_data))

        for o_data in data["ticket_offices"]:
            station.add_ticket_office(MetroSerializer.ticket_office_from_dict(o_data))

        for p_id in data["concourse_passenger_ids"]:
            if p_id not in passengers:
                raise KeyError(f"Passenger '{p_id}' referenced by station '{data['id']}' concourse was not found.")
            station.enter_concourse(passengers[p_id])

        return station

    # --- Train ---

    @staticmethod
    def train_to_dict(train: Train) -> dict:
        return {
            "id": train.id,
            "capacity": train.capacity,
            "stops_for_service": train.stops_for_service,
            "stops_count": train.stops_count,
            "state": train.state.value,
            "passenger_ids": [p.id for p in train.passengers],
        }

    @staticmethod
    def train_from_dict(data: dict, passengers: dict[str, Passenger]) -> Train:
        train = Train(data["id"], data["capacity"], data["stops_for_service"])
        train._stops_count = data["stops_count"]
        train._state = TrainState(data["state"])
        for p_id in data["passenger_ids"]:
            if p_id not in passengers:
                raise KeyError(f"Passenger '{p_id}' referenced by train '{data['id']}' was not found.")
            train.board(passengers[p_id])
        return train

    # --- Route ---

    @staticmethod
    def route_to_dict(route: Route) -> dict:
        return {
            "id": route.id,
            "name": route.name,
            "stops": [
                {
                    "station_id": stop.station.id,
                    "platform_number": stop.platform_number,
                    "travel_time_to_next": stop.travel_time_to_next,
                }
                for stop in route.stops
            ],
        }

    @staticmethod
    def route_from_dict(data: dict, stations: dict[str, Station]) -> Route:
        route = Route(data["id"], data["name"])
        for stop_data in data["stops"]:
            s_id = stop_data["station_id"]
            if s_id not in stations:
                raise KeyError(f"Station '{s_id}' referenced by route '{data['id']}' was not found.")
            route.add_stop(RouteStop(
                station=stations[s_id],
                platform_number=stop_data["platform_number"],
                travel_time_to_next=stop_data["travel_time_to_next"],
            ))
        return route

    # --- ActiveDispatch ---

    @staticmethod
    def dispatch_to_dict(dispatch: ActiveDispatch) -> dict:
        return {
            "train_id": dispatch.train.id,
            "route_id": dispatch.route.id,
            "current_stop_index": dispatch.current_stop_index,
            "timer": dispatch.timer,
        }

    @staticmethod
    def dispatch_from_dict(
        data: dict,
        trains: dict[str, Train],
        routes: dict[str, Route],
    ) -> ActiveDispatch:
        t_id, r_id = data["train_id"], data["route_id"]
        if t_id not in trains:
            raise KeyError(f"Train '{t_id}' referenced by a dispatch was not found.")
        if r_id not in routes:
            raise KeyError(f"Route '{r_id}' referenced by a dispatch was not found.")

        dispatch = ActiveDispatch(trains[t_id], routes[r_id])
        dispatch.current_stop_index = data["current_stop_index"]
        dispatch.timer = data["timer"]
        return dispatch

    @staticmethod
    def state_to_dict(state: AppState) -> dict[str, Any]:
        return {
            "passengers": {p_id: MetroSerializer.passenger_to_dict(p) for p_id, p in state.passengers.items()},
            "stations":   {s_id: MetroSerializer.station_to_dict(s)   for s_id, s in state.stations.items()},
            "trains":     {t_id: MetroSerializer.train_to_dict(t)      for t_id, t in state.trains.items()},
            "routes":     {r_id: MetroSerializer.route_to_dict(r)      for r_id, r in state.routes.items()},
            "schedule": {
                "current_time_minutes": state.schedule.current_time_minutes,
                "dispatches": [MetroSerializer.dispatch_to_dict(d) for d in state.schedule.active_dispatches],
            },
        }

    @staticmethod
    def state_from_dict(data: dict[str, Any]) -> AppState:
        staging = AppState()

        for p_id, p_data in data.get("passengers", {}).items():
            staging.passengers[p_id] = MetroSerializer.passenger_from_dict(p_data)

        for s_id, s_data in data.get("stations", {}).items():
            staging.stations[s_id] = MetroSerializer.station_from_dict(s_data, staging.passengers)

        for t_id, t_data in data.get("trains", {}).items():
            staging.trains[t_id] = MetroSerializer.train_from_dict(t_data, staging.passengers)

        for r_id, r_data in data.get("routes", {}).items():
            staging.routes[r_id] = MetroSerializer.route_from_dict(r_data, staging.stations)

        sched = data.get("schedule", {})
        staging.schedule.current_time_minutes = sched.get("current_time_minutes", 0)
        for d_data in sched.get("dispatches", []):
            dispatch = MetroSerializer.dispatch_from_dict(d_data, staging.trains, staging.routes)
            staging.schedule.active_dispatches.append(dispatch)

        return staging


class StorageService:

    def __init__(self, filepath: str = "metro_state.json"):
        self._filepath = filepath

    @property
    def filepath(self) -> str:
        return self._filepath

    def save(self, state: AppState) -> bool:
        tmp_path = self._filepath + ".tmp"
        try:
            snapshot = MetroSerializer.state_to_dict(state)
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(snapshot, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, self._filepath)
            print(f"[Storage] State saved to '{self._filepath}'.")
            return True
        except Exception as exc:
            print(f"[Storage] Save failed: {exc}")
            # Clean up the temp file if it was created
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            return False

    def load(self, state: AppState) -> bool:
        if not os.path.exists(self._filepath):
            print(f"[Storage] No save file found at '{self._filepath}'.")
            return False

        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            staging = MetroSerializer.state_from_dict(data)
            _apply_staging(staging, state)

            print(f"[Storage] State loaded from '{self._filepath}'.")
            return True

        except (KeyError, ValueError) as exc:
            print(f"[Storage] Load failed — file is inconsistent: {exc}")
            return False
        except json.JSONDecodeError as exc:
            print(f"[Storage] Load failed — file is not valid JSON: {exc}")
            return False
        except Exception as exc:
            print(f"[Storage] Load failed — unexpected error: {exc}")
            return False


def _apply_staging(source: AppState, target: AppState) -> None:
    target.passengers.clear()
    target.stations.clear()
    target.trains.clear()
    target.routes.clear()
    target.schedule._active_dispatches.clear()

    target.passengers.update(source.passengers)
    target.stations.update(source.stations)
    target.trains.update(source.trains)
    target.routes.update(source.routes)
    target.schedule.current_time_minutes = source.schedule.current_time_minutes
    target.schedule._active_dispatches.extend(source.schedule.active_dispatches)


def setup_world(state: AppState) -> None:
    """Seeds the system with a minimal default scenario."""
    state.passengers.clear()
    state.stations.clear()
    state.trains.clear()
    state.routes.clear()
    state.schedule._current_time_minutes = 0
    state.schedule._active_dispatches.clear()

    s1 = Station("S1", "Oktyabrskaya")
    s1.add_platform(Platform("P1", 1))
    s1.add_turnstile(Turnstile("T1"))
    s1.add_ticket_office(TicketOffice("O1"))
    state.stations["S1"] = s1

    s2 = Station("S2", "Lenin Square")
    s2.add_platform(Platform("P2", 1))
    state.stations["S2"] = s2

    r1 = Route("R1", "Blue Line")
    r1.add_stop(RouteStop(s1, 1, travel_time_to_next=3))
    r1.add_stop(RouteStop(s2, 1, travel_time_to_next=0))
    state.routes["R1"] = r1

    t1 = Train("TR-01", capacity=50, stops_for_service=5)
    state.trains["TR-01"] = t1