import os
import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from src.application.state import AppState
from src.application.schedule import ActiveDispatch
from src.domain.models.money import Money
from src.domain.models.passenger import Passenger
from src.domain.models.platform import Platform
from src.domain.models.route import Route, RouteStop
from src.domain.models.station import Station
from src.domain.models.ticket import Ticket, TicketType
from src.domain.models.ticket_office import TicketOffice
from src.domain.models.train import Train, TrainState
from src.domain.models.turnstile import Turnstile, TurnstileState
from src.infrastructure.storage import MetroSerializer, StorageService


def make_trips_ticket(tid="TKT-1", trips=5, used=2) -> Ticket:
    t = Ticket(tid, TicketType.BY_TRIPS, max_trips=trips)
    t._current_trips = used
    return t


def make_daily_ticket(tid="TKT-2") -> Ticket:
    future = datetime.now() + timedelta(days=1)
    return Ticket(tid, TicketType.DAILY, expires_at=future)


def make_passenger(pid="P1", name="Alice", dest="S2", ticket=None) -> Passenger:
    p = Passenger(pid, name, dest)
    if ticket:
        p.buy_ticket(ticket)
    return p


def make_station(sid="S1", name="Central") -> Station:
    s = Station(sid, name)
    s.add_platform(Platform("P1", 1))
    s.add_turnstile(Turnstile("T1"))
    s.add_ticket_office(TicketOffice("O1"))
    return s


def make_route(s1: Station, s2: Station) -> Route:
    r = Route("R1", "Blue Line")
    r.add_stop(RouteStop(s1, 1, travel_time_to_next=3))
    r.add_stop(RouteStop(s2, 1, travel_time_to_next=0))
    return r


class TestSerializeTicket:
    def test_trips_ticket_roundtrip(self):
        original = make_trips_ticket()
        restored = MetroSerializer.ticket_from_dict(MetroSerializer.ticket_to_dict(original))

        assert restored.id == original.id
        assert restored.ticket_type == TicketType.BY_TRIPS
        assert restored.max_trips == original.max_trips
        assert restored.current_trips == original.current_trips

    def test_daily_ticket_roundtrip(self):
        original = make_daily_ticket()
        restored = MetroSerializer.ticket_from_dict(MetroSerializer.ticket_to_dict(original))

        assert restored.id == original.id
        assert restored.ticket_type == TicketType.DAILY
        assert restored.expires_at == original.expires_at

    def test_ticket_without_explicit_expiry(self):
        original = Ticket("TKT-3", TicketType.BY_TRIPS, max_trips=1)
        data = MetroSerializer.ticket_to_dict(original)
        assert data["expires_at"] is not None
        restored = MetroSerializer.ticket_from_dict(data)
        assert restored.id == "TKT-3"
        assert restored.ticket_type == TicketType.BY_TRIPS


class TestSerializePassenger:
    def test_passenger_without_ticket(self):
        original = make_passenger(ticket=None)
        restored = MetroSerializer.passenger_from_dict(MetroSerializer.passenger_to_dict(original))

        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.destination_station_id == original.destination_station_id
        assert restored.ticket is None

    def test_passenger_with_ticket(self):
        ticket = make_trips_ticket()
        original = make_passenger(ticket=ticket)
        restored = MetroSerializer.passenger_from_dict(MetroSerializer.passenger_to_dict(original))

        assert restored.ticket is not None
        assert restored.ticket.id == ticket.id
        assert restored.ticket.current_trips == ticket.current_trips


class TestSerializePlatform:
    def test_platform_roundtrip_with_passengers(self):
        passengers = {"P1": make_passenger("P1"), "P2": make_passenger("P2", "Bob")}
        platform = Platform("PL1", 2)
        for p in passengers.values():
            platform.add_passenger(p)

        data = MetroSerializer.platform_to_dict(platform)
        restored = MetroSerializer.platform_from_dict(data, passengers)

        assert restored.id == "PL1"
        assert restored.number == 2
        assert len(restored.waiting_passengers) == 2

    def test_platform_missing_passenger_raises(self):
        platform = Platform("PL1", 1)
        platform.add_passenger(make_passenger("GHOST"))
        data = MetroSerializer.platform_to_dict(platform)

        with pytest.raises(KeyError):
            MetroSerializer.platform_from_dict(data, {})  # empty registry


class TestSerializeTurnstile:
    def test_locked_state_preserved(self):
        t = Turnstile("T1")
        restored = MetroSerializer.turnstile_from_dict(MetroSerializer.turnstile_to_dict(t))
        assert restored.state == TurnstileState.LOCKED

    def test_lockdown_state_preserved(self):
        t = Turnstile("T1")
        t.lockdown()
        restored = MetroSerializer.turnstile_from_dict(MetroSerializer.turnstile_to_dict(t))
        assert restored.state == TurnstileState.LOCKED_DOWN


class TestSerializeTicketOffice:
    def test_balance_preserved(self):
        office = TicketOffice("O1")
        office._balance = Money(Decimal("42.50"))
        restored = MetroSerializer.ticket_office_from_dict(MetroSerializer.ticket_office_to_dict(office))
        assert restored.balance.amount == Decimal("42.50")


class TestSerializeStation:
    def test_full_station_roundtrip(self):
        passengers = {
            "P1": make_passenger("P1"),
            "P2": make_passenger("P2", "Bob"),
        }
        s = Station("S1", "Central")
        p = Platform("PL1", 1)
        p.add_passenger(passengers["P1"])
        s.add_platform(p)
        s.add_turnstile(Turnstile("T1"))
        s.add_ticket_office(TicketOffice("O1"))
        s.enter_concourse(passengers["P2"])

        data = MetroSerializer.station_to_dict(s)
        restored = MetroSerializer.station_from_dict(data, passengers)

        assert restored.id == "S1"
        assert restored.name == "Central"
        assert len(restored.platforms) == 1
        assert len(restored.turnstiles) == 1
        assert len(restored.ticket_offices) == 1
        assert len(restored.concourse_passengers) == 1

    def test_station_missing_concourse_passenger_raises(self):
        passengers = {"P1": make_passenger("P1")}
        s = Station("S1", "Central")
        s.enter_concourse(passengers["P1"])
        data = MetroSerializer.station_to_dict(s)

        with pytest.raises(KeyError):
            MetroSerializer.station_from_dict(data, {})


class TestSerializeTrain:
    def test_train_roundtrip(self):
        passengers = {"P1": make_passenger("P1")}
        t = Train("TR-01", capacity=50, stops_for_service=5)
        t._stops_count = 3
        t.set_state(TrainState.IN_TRANSIT)
        t.board(passengers["P1"])

        data = MetroSerializer.train_to_dict(t)
        restored = MetroSerializer.train_from_dict(data, passengers)

        assert restored.id == "TR-01"
        assert restored.capacity == 50
        assert restored.stops_count == 3
        assert restored.state == TrainState.IN_TRANSIT
        assert restored.passenger_count == 1

    def test_train_missing_passenger_raises(self):
        passengers = {"P1": make_passenger("P1")}
        t = Train("TR-01", capacity=50, stops_for_service=5)
        t.set_state(TrainState.IN_TRANSIT)
        t.board(passengers["P1"])
        data = MetroSerializer.train_to_dict(t)

        with pytest.raises(KeyError):
            MetroSerializer.train_from_dict(data, {})


class TestSerializeRoute:
    def test_route_roundtrip(self):
        stations = {
            "S1": make_station("S1", "Start"),
            "S2": make_station("S2", "End"),
        }
        route = make_route(stations["S1"], stations["S2"])

        data = MetroSerializer.route_to_dict(route)
        restored = MetroSerializer.route_from_dict(data, stations)

        assert restored.id == "R1"
        assert restored.name == "Blue Line"
        assert len(restored.stops) == 2
        assert restored.stops[0].station.id == "S1"
        assert restored.stops[0].travel_time_to_next == 3
        assert restored.stops[1].travel_time_to_next == 0

    def test_route_missing_station_raises(self):
        stations = {"S1": make_station("S1"), "S2": make_station("S2")}
        route = make_route(stations["S1"], stations["S2"])
        data = MetroSerializer.route_to_dict(route)

        with pytest.raises(KeyError):
            MetroSerializer.route_from_dict(data, {})


class TestSerializeDispatch:
    def test_dispatch_roundtrip(self):
        s1, s2 = make_station("S1"), make_station("S2", "End")
        trains = {"TR-01": Train("TR-01", 50, 5)}
        routes = {"R1": make_route(s1, s2)}

        dispatch = ActiveDispatch(trains["TR-01"], routes["R1"])
        dispatch.current_stop_index = 1
        dispatch.timer = 3

        data = MetroSerializer.dispatch_to_dict(dispatch)
        restored = MetroSerializer.dispatch_from_dict(data, trains, routes)

        assert restored.train.id == "TR-01"
        assert restored.route.id == "R1"
        assert restored.current_stop_index == 1
        assert restored.timer == 3

    def test_dispatch_missing_train_raises(self):
        s1, s2 = make_station("S1"), make_station("S2", "End")
        train = Train("TR-01", 50, 5)
        route = make_route(s1, s2)
        dispatch = ActiveDispatch(train, route)
        data = MetroSerializer.dispatch_to_dict(dispatch)

        with pytest.raises(KeyError):
            MetroSerializer.dispatch_from_dict(data, {}, {"R1": route})


class TestFullStateRoundTrip:
    def _build_state(self) -> AppState:
        state = AppState()

        ticket = make_trips_ticket(trips=10, used=3)
        p = make_passenger("P1", ticket=ticket)
        state.passengers["P1"] = p

        s1 = make_station("S1", "Central")
        s2 = make_station("S2", "North")
        s1.enter_concourse(p)
        state.stations["S1"] = s1
        state.stations["S2"] = s2

        t = Train("TR-01", capacity=50, stops_for_service=5)
        state.trains["TR-01"] = t

        route = make_route(s1, s2)
        state.routes["R1"] = route

        state.schedule.current_time_minutes = 42

        return state

    def test_state_to_dict_and_back(self):
        original = self._build_state()
        snapshot = MetroSerializer.state_to_dict(original)
        restored = MetroSerializer.state_from_dict(snapshot)

        assert set(restored.passengers) == set(original.passengers)
        assert set(restored.stations) == set(original.stations)
        assert set(restored.trains) == set(original.trains)
        assert set(restored.routes) == set(original.routes)
        assert restored.schedule.current_time_minutes == 42

    def test_passenger_ticket_state_preserved(self):
        original = self._build_state()
        snapshot = MetroSerializer.state_to_dict(original)
        restored = MetroSerializer.state_from_dict(snapshot)

        r_passenger = restored.passengers["P1"]
        assert r_passenger.ticket is not None
        assert r_passenger.ticket.current_trips == 3
        assert r_passenger.ticket.max_trips == 10

    def test_concourse_reference_is_same_object(self):
        """The passenger in the concourse must be the same object as in state.passengers."""
        original = self._build_state()
        snapshot = MetroSerializer.state_to_dict(original)
        restored = MetroSerializer.state_from_dict(snapshot)

        concourse = restored.stations["S1"].concourse_passengers
        assert len(concourse) == 1
        assert concourse[0] is restored.passengers["P1"]


class TestStorageService:
    @pytest.fixture
    def tmp_path_str(self, tmp_path):
        return str(tmp_path / "metro_test.json")

    @pytest.fixture
    def state(self):
        state = AppState()
        state.passengers["P1"] = make_passenger("P1", ticket=make_trips_ticket())
        state.stations["S1"] = make_station()
        return state

    def test_save_creates_file(self, tmp_path_str, state):
        storage = StorageService(tmp_path_str)
        result = storage.save(state)
        assert result is True
        assert os.path.exists(tmp_path_str)

    def test_save_and_load_roundtrip(self, tmp_path_str, state):
        storage = StorageService(tmp_path_str)
        storage.save(state)

        target = AppState()
        result = storage.load(target)

        assert result is True
        assert "P1" in target.passengers
        assert "S1" in target.stations

    def test_load_missing_file_returns_false(self, tmp_path_str):
        storage = StorageService(tmp_path_str)
        target = AppState()
        result = storage.load(target)
        assert result is False

    def test_load_corrupt_json_returns_false(self, tmp_path_str):
        with open(tmp_path_str, "w") as f:
            f.write("{ this is not valid json }")
        storage = StorageService(tmp_path_str)
        target = AppState()
        result = storage.load(target)
        assert result is False

    def test_load_corrupt_json_does_not_modify_state(self, tmp_path_str):
        """A failed load must leave the live state untouched."""
        with open(tmp_path_str, "w") as f:
            f.write("{ bad json")
        storage = StorageService(tmp_path_str)

        target = AppState()
        target.passengers["EXISTING"] = make_passenger("EXISTING")
        storage.load(target)

        assert "EXISTING" in target.passengers

    def test_atomic_write_no_tmp_file_after_save(self, tmp_path_str, state):
        storage = StorageService(tmp_path_str)
        storage.save(state)
        assert not os.path.exists(tmp_path_str + ".tmp")

    def test_load_preserves_schedule_time(self, tmp_path_str):
        storage = StorageService(tmp_path_str)

        source = AppState()
        source.schedule.current_time_minutes = 99
        storage.save(source)

        target = AppState()
        storage.load(target)
        assert target.schedule.current_time_minutes == 99

    def test_filepath_property(self, tmp_path_str):
        storage = StorageService(tmp_path_str)
        assert storage.filepath == tmp_path_str