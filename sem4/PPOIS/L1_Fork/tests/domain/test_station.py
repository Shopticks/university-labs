import pytest
from src.domain.models.station import Station
from src.domain.models.platform import Platform
from src.domain.models.turnstile import Turnstile, TurnstileState
from src.domain.models.ticket_office import TicketOffice
from src.domain.models.passenger import Passenger
from src.exceptions import StationError


@pytest.fixture
def station():
    s = Station("S1", "Central")
    s.add_platform(Platform("P1", 1))
    s.add_turnstile(Turnstile("T1"))
    s.add_ticket_office(TicketOffice("O1"))
    return s


@pytest.fixture
def passenger():
    return Passenger("PAS-1", "Alice", "S2")


class TestStationInit:
    def test_id_and_name(self, station):
        assert station.id == "S1"
        assert station.name == "Central"

    def test_initial_collections(self, station):
        assert len(station.platforms) == 1
        assert len(station.turnstiles) == 1
        assert len(station.ticket_offices) == 1
        assert station.concourse_passengers == []


class TestStationGetPlatform:
    def test_get_existing_platform(self, station):
        p = station.get_platform(1)
        assert p.number == 1

    def test_get_nonexistent_platform_raises(self, station):
        with pytest.raises(StationError):
            station.get_platform(99)


class TestStationConcourse:
    def test_enter_concourse(self, station, passenger):
        station.enter_concourse(passenger)
        assert passenger in station.concourse_passengers

    def test_exit_station(self, station, passenger):
        station.enter_concourse(passenger)
        station.exit_station(passenger)
        assert passenger not in station.concourse_passengers

    def test_concourse_is_a_copy(self, station, passenger):
        station.enter_concourse(passenger)
        snapshot = station.concourse_passengers
        snapshot.clear()
        assert len(station.concourse_passengers) == 1


class TestStationRouteToPlatform:
    def test_route_moves_passenger_from_concourse_to_platform(self, station, passenger):
        station.enter_concourse(passenger)
        station.route_to_platform(passenger, 1)
        assert passenger not in station.concourse_passengers
        assert passenger in station.get_platform(1).waiting_passengers

    def test_route_passenger_not_in_concourse_raises(self, station, passenger):
        with pytest.raises(StationError):
            station.route_to_platform(passenger, 1)

    def test_route_to_nonexistent_platform_raises(self, station, passenger):
        station.enter_concourse(passenger)
        with pytest.raises(StationError):
            station.route_to_platform(passenger, 99)


class TestStationLockdown:
    def test_lockdown_affects_all_turnstiles(self, station):
        station.lockdown()
        for t in station.turnstiles:
            assert t.state == TurnstileState.LOCKED_DOWN

    def test_lift_lockdown_restores_all_turnstiles(self, station):
        station.lockdown()
        station.lift_lockdown()
        for t in station.turnstiles:
            assert t.state == TurnstileState.LOCKED