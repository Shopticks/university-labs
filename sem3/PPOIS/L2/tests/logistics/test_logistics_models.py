from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from pharma_distributor.common.enums import (
    DriverStatus,
    VehicleStatus,
    RouteStatus
)
from pharma_distributor.common.models import Address
from pharma_distributor.exceptions import LogisticsError
from pharma_distributor.logistics.models import (
    Driver,
    Vehicle,
    VehicleStats,
    DeliveryRoute,
    RoutePoint
)


@pytest.fixture
def address():
    return Address("BY", "Minsk", "Lenina", "220000")


@pytest.fixture
def driver():
    return Driver(
        id=1,
        license_number="AB12345",
        full_name="Ivan Ivanov",
        experience_years=5
    )


@pytest.fixture
def vehicle_stats():
    return VehicleStats(
        fuel_capacity_liters=100.0,
        avg_consumption_per_100km=10.0,
        max_load_kg=1000.0,
        maintenance_interval_km=1000.0
    )


@pytest.fixture
def vehicle(vehicle_stats):
    return Vehicle(
        id="V-001",
        plate_number="1234 AB-7",
        model="Ford Transit",
        stats=vehicle_stats
    )


@pytest.fixture
def route_point(address):
    return RoutePoint(
        id="P-1",
        address=address,
        expected_arrival=datetime.now() + timedelta(hours=1)
    )



def test_driver_status_transitions(driver):
    assert driver.is_available is True

    driver.assign_to_trip()
    assert driver.status == DriverStatus.ON_TRIP
    assert driver.is_available is False

    driver.release_from_trip()
    assert driver.is_available is True


def test_driver_go_off_duty_fail(driver):
    driver.assign_to_trip()
    with pytest.raises(LogisticsError, match="Cannot go off-duty"):
        driver.go_off_duty()



def test_vehicle_assign_driver(vehicle, driver):
    vehicle.assign_driver(driver)
    assert vehicle.current_driver == driver

    driver2 = Driver(2, "CD56789", "Petr", 2)
    with pytest.raises(LogisticsError, match="already has a driver"):
        vehicle.assign_driver(driver2)


def test_vehicle_release_driver(vehicle, driver):
    vehicle.assign_driver(driver)
    vehicle.release_driver()
    assert vehicle.current_driver is None


def test_vehicle_start_trip_lifecycle(vehicle, driver):
    vehicle.assign_driver(driver)

    vehicle.start_trip()
    assert vehicle.status == VehicleStatus.ON_ROUTE
    assert driver.status == DriverStatus.ON_TRIP

    vehicle.complete_trip(distance_traveled_km=100.0)
    assert vehicle.status == VehicleStatus.IDLE
    assert vehicle.mileage == 100.0
    assert driver.status == DriverStatus.AVAILABLE


def test_vehicle_start_trip_no_driver(vehicle):
    with pytest.raises(LogisticsError, match="without a driver"):
        vehicle.start_trip()


def test_vehicle_maintenance_logic(vehicle, driver):
    vehicle.assign_driver(driver)
    vehicle.start_trip()
    vehicle.complete_trip(1001.0)

    assert vehicle.needs_maintenance() is True

    with pytest.raises(LogisticsError, match="needs maintenance"):
        vehicle.start_trip()

    vehicle.perform_maintenance()
    assert vehicle.needs_maintenance() is False
    assert vehicle.status == VehicleStatus.IDLE


def test_vehicle_fuel_calc(vehicle):
    required = vehicle.calculate_fuel_required(250.0)
    assert required == 25.0



def test_route_planning(vehicle, route_point):
    route = DeliveryRoute(id="R-1", vehicle=vehicle)

    route.add_point(route_point, distance_from_prev_km=50.0)

    assert len(route.points) == 1
    assert route.estimated_distance_km == 50.0
    assert route.status == RouteStatus.PLANNED


def test_route_execution(vehicle, driver, route_point):
    vehicle.assign_driver(driver)
    route = DeliveryRoute(id="R-1", vehicle=vehicle)
    route.add_point(route_point, 10.0)

    route.start_route()
    assert route.status == RouteStatus.IN_PROGRESS
    assert vehicle.status == VehicleStatus.ON_ROUTE
    assert route.start_time is not None

    route.complete_point(0)
    assert route.points[0].is_visited is True
    assert route.points[0].actual_arrival is not None

    route.finish_route(actual_total_distance_km=12.0)
    assert route.status == RouteStatus.COMPLETED
    assert vehicle.status == VehicleStatus.IDLE
    assert vehicle.mileage == 12.0


def test_route_cannot_add_points_after_start(vehicle, driver, route_point):
    vehicle.assign_driver(driver)
    route = DeliveryRoute(id="R-1", vehicle=vehicle)
    route.add_point(route_point, 10.0)
    route.start_route()

    new_point = RoutePoint("P-2", Mock(), datetime.now())

    with pytest.raises(LogisticsError, match="already started"):
        route.add_point(new_point, 5.0)