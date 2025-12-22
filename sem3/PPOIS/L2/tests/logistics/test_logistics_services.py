from datetime import timedelta, datetime
from unittest.mock import Mock

import pytest

from pharma_distributor.common.enums import VehicleStatus
from pharma_distributor.exceptions import LogisticsError
from pharma_distributor.logistics.models import Vehicle, Driver, DeliveryRoute, RoutePoint
from pharma_distributor.logistics.services import FleetManager, RoutingService


@pytest.fixture
def fleet_manager():
    return FleetManager()


@pytest.fixture
def routing_service():
    return RoutingService()


@pytest.fixture
def mock_vehicle():
    v = Mock(spec=Vehicle)
    v.plate_number = "1234"
    v.status = VehicleStatus.IDLE
    v.current_driver = None
    return v


@pytest.fixture
def mock_driver():
    return Mock(spec=Driver)



def test_assign_driver(fleet_manager, mock_vehicle, mock_driver):
    fleet_manager.assign_driver_to_vehicle(mock_vehicle, mock_driver)
    mock_vehicle.assign_driver.assert_called_once_with(mock_driver)


def test_send_to_maintenance_success(fleet_manager, mock_vehicle, mock_driver):
    mock_vehicle.current_driver = mock_driver

    fleet_manager.send_to_maintenance(mock_vehicle)

    mock_vehicle.release_driver.assert_called_once()



def test_send_to_maintenance_fail_on_route(fleet_manager, mock_vehicle):
    mock_vehicle.status = VehicleStatus.ON_ROUTE

    with pytest.raises(LogisticsError, match="currently on route"):
        fleet_manager.send_to_maintenance(mock_vehicle)



def test_calculate_eta(routing_service):
    eta = routing_service.calculate_eta(60.0, 60.0)
    assert eta == timedelta(hours=1)

    assert routing_service.calculate_eta(100, 0) == timedelta(hours=0)


def test_create_route(routing_service, mock_vehicle):
    p1 = Mock(spec=RoutePoint)
    p2 = Mock(spec=RoutePoint)
    points = [p1, p2]
    dists = [10.0, 20.0]

    route = routing_service.create_route(mock_vehicle, points, dists)

    assert isinstance(route, DeliveryRoute)
    assert len(route.points) == 2
    assert route.estimated_distance_km == 30.0


def test_create_route_mismatch(routing_service, mock_vehicle):
    with pytest.raises(ValueError):
        routing_service.create_route(mock_vehicle, [Mock()], [])


def test_optimize_route(routing_service):
    now = datetime.now()
    p1 = Mock(spec=RoutePoint, expected_arrival=now + timedelta(hours=2))
    p2 = Mock(spec=RoutePoint, expected_arrival=now + timedelta(hours=1))

    route = Mock(spec=DeliveryRoute)
    route.points = [p1, p2]

    routing_service.optimize_route(route)

    assert route.points[0] == p2
    assert route.points[1] == p1


def test_dispatch_route(routing_service):
    route = Mock(spec=DeliveryRoute)
    routing_service.dispatch_route(route)
    route.start_route.assert_called_once()


def test_report_arrival(routing_service):
    p1 = RoutePoint("id-1", Mock(), datetime.now())
    p2 = RoutePoint("id-2", Mock(), datetime.now())

    route = Mock(spec=DeliveryRoute)
    route.points = [p1, p2]

    routing_service.report_arrival(route, "id-2")

    route.complete_point.assert_called_once_with(1)