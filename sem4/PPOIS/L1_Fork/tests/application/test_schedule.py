import pytest
from src.domain.models.train import Train, TrainState
from src.domain.models.station import Station
from src.domain.models.platform import Platform
from src.domain.models.route import Route, RouteStop
from src.application.schedule import ScheduleService


def make_route(travel_time: int = 2) -> tuple[Route, Station, Station]:
    s1 = Station("S1", "Start")
    s2 = Station("S2", "End")
    s1.add_platform(Platform("P1", 1))
    s2.add_platform(Platform("P2", 1))

    route = Route("R1", "Line 1")
    route.add_stop(RouteStop(s1, 1, travel_time_to_next=travel_time))
    route.add_stop(RouteStop(s2, 1, travel_time_to_next=0))
    return route, s1, s2


@pytest.fixture
def service():
    return ScheduleService()


@pytest.fixture
def train():
    return Train("TR-01", capacity=50, stops_for_service=10)


class TestScheduleServiceTime:
    def test_initial_time_is_zero(self, service):
        assert service.current_time_minutes == 0

    def test_tick_advances_time(self, service):
        service.tick()
        assert service.current_time_minutes == 1

    def test_current_time_str_format(self, service):
        assert service.current_time_str == "06:00"

    def test_current_time_str_after_ticks(self, service):
        for _ in range(65):
            service.tick()
        assert service.current_time_str == "07:05"


class TestDispatchTrain:
    def test_dispatch_sets_train_in_transit(self, service, train):
        route, _, _ = make_route()
        service.dispatch_train(train, route)
        assert train.state == TrainState.IN_TRANSIT

    def test_dispatch_adds_to_active_dispatches(self, service, train):
        route, _, _ = make_route()
        service.dispatch_train(train, route)
        assert len(service.active_dispatches) == 1

    def test_dispatch_sets_timer_to_first_segment(self, service, train):
        route, _, _ = make_route(travel_time=5)
        service.dispatch_train(train, route)
        dispatch = service.active_dispatches[0]
        assert dispatch.timer == 5


class TestTrainMovement:
    def test_train_arrives_at_station_after_travel_time(self, service, train):
        route, _, _ = make_route(travel_time=2)
        service.dispatch_train(train, route)

        service.tick()
        service.tick()

        assert train.state == TrainState.AT_STATION

    def test_train_departs_after_dwell(self, service, train):
        route, _, _ = make_route(travel_time=2)
        service.dispatch_train(train, route)

        for _ in range(3):
            service.tick()

        assert train.state == TrainState.IN_TRANSIT

    def test_train_completes_full_route_and_goes_to_depo(self, service, train):
        route, _, _ = make_route(travel_time=2)
        service.dispatch_train(train, route)

        for _ in range(10):
            service.tick()

        assert train.state == TrainState.IN_DEPO
        assert len(service.active_dispatches) == 0

    def test_still_in_transit_before_arrival(self, service, train):
        route, _, _ = make_route(travel_time=3)
        service.dispatch_train(train, route)

        service.tick()
        assert train.state == TrainState.IN_TRANSIT