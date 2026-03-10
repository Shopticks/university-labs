import pytest
from src.domain.models.platform import Platform
from src.domain.models.passenger import Passenger
from src.exceptions import PlatformOperationError


@pytest.fixture
def platform():
    return Platform("P1", 1)


@pytest.fixture
def passenger():
    return Passenger("PAS-1", "Alice", "S2")


class TestPlatformInit:
    def test_id_and_number(self, platform):
        assert platform.id == "P1"
        assert platform.number == 1

    def test_initially_empty(self, platform):
        assert platform.waiting_passengers == []


class TestPlatformAddPassenger:
    def test_add_single_passenger(self, platform, passenger):
        platform.add_passenger(passenger)
        assert passenger in platform.waiting_passengers

    def test_add_duplicate_raises(self, platform, passenger):
        platform.add_passenger(passenger)
        with pytest.raises(PlatformOperationError):
            platform.add_passenger(passenger)

    def test_add_multiple_passengers(self, platform):
        p1 = Passenger("P1", "Alice", "S2")
        p2 = Passenger("P2", "Bob", "S2")
        platform.add_passengers([p1, p2])
        assert len(platform.waiting_passengers) == 2

    def test_add_multiple_with_duplicate_raises(self, platform):
        p1 = Passenger("P1", "Alice", "S2")
        platform.add_passenger(p1)
        with pytest.raises(PlatformOperationError):
            platform.add_passengers([p1])


class TestPlatformRemovePassengers:
    def test_remove_existing(self, platform):
        p1 = Passenger("P1", "Alice", "S2")
        p2 = Passenger("P2", "Bob", "S2")
        platform.add_passengers([p1, p2])
        platform.remove_passengers([p1])
        assert p1 not in platform.waiting_passengers
        assert p2 in platform.waiting_passengers

    def test_remove_all(self, platform):
        p1 = Passenger("P1", "Alice", "S2")
        p2 = Passenger("P2", "Bob", "S2")
        platform.add_passengers([p1, p2])
        platform.remove_passengers([p1, p2])
        assert platform.waiting_passengers == []

    def test_remove_nonexistent_is_noop(self, platform, passenger):
        platform.remove_passengers([passenger])
        assert platform.waiting_passengers == []


class TestPlatformWaitingPassengersIsACopy:
    def test_mutating_returned_list_does_not_affect_platform(self, platform, passenger):
        platform.add_passenger(passenger)
        snapshot = platform.waiting_passengers
        snapshot.clear()
        assert len(platform.waiting_passengers) == 1