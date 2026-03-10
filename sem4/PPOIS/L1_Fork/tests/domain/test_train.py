import pytest
from src.domain.models.train import Train, TrainState
from src.domain.models.passenger import Passenger
from src.exceptions import TrainFullError, TrainNotEmptyError, TrainNeedsMaintenanceError


@pytest.fixture
def train():
    return Train("TR-01", capacity=3, stops_for_service=2)


@pytest.fixture
def passengers():
    return [Passenger(f"P{i}", f"Passenger {i}", "S2") for i in range(3)]


class TestTrainInit:
    def test_initial_state_is_idle(self, train):
        assert train.state == TrainState.IN_DEPO

    def test_initial_passenger_count(self, train):
        assert train.passenger_count == 0

    def test_free_seats_equals_capacity(self, train):
        assert train.free_seats == 3

    def test_does_not_need_maintenance_initially(self, train):
        assert train.needs_maintenance is False


class TestTrainBoarding:
    def test_board_increases_count(self, train, passengers):
        train.board(passengers[0])
        assert train.passenger_count == 1
        assert train.free_seats == 2

    def test_board_at_capacity_raises(self, train, passengers):
        for p in passengers:
            train.board(p)
        extra = Passenger("P99", "Extra", "S2")
        with pytest.raises(TrainFullError):
            train.board(extra)

    def test_passengers_list_is_a_copy(self, train, passengers):
        train.board(passengers[0])
        snapshot = train.passengers
        snapshot.clear()
        assert train.passenger_count == 1


class TestTrainAlight:
    def test_alight_removes_specified_passengers(self, train, passengers):
        train.board(passengers[0])
        train.board(passengers[1])
        train.alight([passengers[0]])
        assert passengers[0] not in train.passengers
        assert passengers[1] in train.passengers

    def test_unload_all_empties_train(self, train, passengers):
        for p in passengers:
            train.board(p)
        evicted = train.unload_all()
        assert train.passenger_count == 0
        assert len(evicted) == 3


class TestTrainStateTransitions:
    def test_set_state_to_in_transit(self, train):
        train.set_state(TrainState.IN_TRANSIT)
        assert train.state == TrainState.IN_TRANSIT

    def test_cannot_go_to_depo_with_passengers(self, train, passengers):
        train.set_state(TrainState.IN_TRANSIT)
        train.board(passengers[0])
        with pytest.raises(TrainNotEmptyError):
            train.set_state(TrainState.IN_DEPO)

    def test_maintenance_block_prevents_dispatch(self, train):
        train.set_state(TrainState.IN_TRANSIT)
        train.record_stop()
        train.record_stop()  # hits stops_for_service=2
        train.set_state(TrainState.IN_DEPO)
        with pytest.raises(TrainNeedsMaintenanceError):
            train.set_state(TrainState.IN_TRANSIT)


class TestTrainMaintenance:
    def test_maintain_resets_stops_count(self, train):
        train.set_state(TrainState.IN_TRANSIT)
        train.record_stop()
        train.record_stop()
        train.set_state(TrainState.IN_DEPO)
        train.maintain()
        assert train.stops_count == 0
        assert train.needs_maintenance is False

    def test_maintain_allows_redispatch(self, train):
        train.set_state(TrainState.IN_TRANSIT)
        train.record_stop()
        train.record_stop()
        train.set_state(TrainState.IN_DEPO)
        train.maintain()
        train.set_state(TrainState.IN_TRANSIT)
        assert train.state == TrainState.IN_TRANSIT

    def test_maintain_with_passengers_raises(self, train, passengers):
        train.set_state(TrainState.IN_TRANSIT)
        train.board(passengers[0])
        with pytest.raises(TrainNotEmptyError):
            train.maintain()