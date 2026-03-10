import pytest
from src.domain.models.train import Train, TrainState
from src.domain.models.station import Station
from src.domain.models.platform import Platform
from src.domain.models.passenger import Passenger
from src.application.boarding import BoardingService


def make_passenger(pid: str, dest: str = "S2") -> Passenger:
    return Passenger(pid, f"Passenger {pid}", dest)


@pytest.fixture
def station():
    s = Station("S1", "Central")
    s.add_platform(Platform("P1", 1))
    return s


@pytest.fixture
def train():
    t = Train("TR-01", capacity=3, stops_for_service=10)
    t.set_state(TrainState.IN_TRANSIT)
    return t


class TestProcessRegularStop:
    def test_passengers_going_to_this_station_alight(self, train, station):
        p_alighting = make_passenger("P1", dest="S1")
        train.board(p_alighting)

        platform = station.get_platform(1)
        BoardingService.process_regular_stop(train, station, platform)

        assert p_alighting not in train.passengers
        assert p_alighting not in station.concourse_passengers

    def test_passengers_not_at_destination_stay_on_train(self, train, station):
        p_through = make_passenger("P2", dest="S99")
        train.board(p_through)

        platform = station.get_platform(1)
        BoardingService.process_regular_stop(train, station, platform)

        assert p_through in train.passengers

    def test_waiting_passengers_board(self, train, station):
        platform = station.get_platform(1)
        waiting = make_passenger("P3", dest="S99")
        platform.add_passenger(waiting)

        BoardingService.process_regular_stop(train, station, platform)

        assert waiting in train.passengers
        assert waiting not in platform.waiting_passengers

    def test_boarding_respects_train_capacity(self, station):
        small_train = Train("TR-SMALL", capacity=1, stops_for_service=10)
        small_train.set_state(TrainState.IN_TRANSIT)
        small_train.board(make_passenger("P_existing", "S99"))

        platform = station.get_platform(1)
        platform.add_passenger(make_passenger("P_wait1", "S99"))
        platform.add_passenger(make_passenger("P_wait2", "S99"))

        BoardingService.process_regular_stop(small_train, station, platform)

        assert small_train.passenger_count == 1
        assert len(platform.waiting_passengers) == 2

    def test_train_state_is_at_station_after_stop(self, train, station):
        platform = station.get_platform(1)
        BoardingService.process_regular_stop(train, station, platform)
        assert train.state == TrainState.AT_STATION


class TestProcessTerminalStop:
    def test_all_passengers_evicted(self, train, station):
        p1 = make_passenger("P1", "S99")
        p2 = make_passenger("P2", "S99")
        train.board(p1)
        train.board(p2)

        BoardingService.process_terminal_stop(train, station)

        assert train.passenger_count == 0

    def test_evicted_passengers_go_to_concourse(self, train, station):
        p1 = make_passenger("P1", "S99")
        train.board(p1)

        BoardingService.process_terminal_stop(train, station)

        assert p1 in station.concourse_passengers

    def test_train_goes_to_depo_after_terminal(self, train, station):
        BoardingService.process_terminal_stop(train, station)
        assert train.state == TrainState.IN_DEPO

    def test_stop_is_recorded(self, train, station):
        stops_before = train.stops_count
        BoardingService.process_terminal_stop(train, station)
        assert train.stops_count == stops_before + 1