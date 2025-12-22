from datetime import timedelta, datetime
from typing import List

from src.pharma_distributor.logistics.models import (
    Vehicle,
    Driver,
    DeliveryRoute,
    RoutePoint,
    VehicleStatus
)
from src.pharma_distributor.exceptions import LogisticsError


class FleetManager:

    def assign_driver_to_vehicle(self, vehicle: Vehicle, driver: Driver) -> None:
        vehicle.assign_driver(driver)

    def end_driver_shift(self, vehicle: Vehicle) -> None:
        vehicle.release_driver()

    def send_to_maintenance(self, vehicle: Vehicle) -> None:
        if vehicle.status == VehicleStatus.ON_ROUTE:
            raise LogisticsError(f"Cannot send vehicle {vehicle.plate_number} to maintenance: currently on route")

        if vehicle.current_driver:
            vehicle.release_driver()

        object.__setattr__(vehicle, '_status', VehicleStatus.MAINTENANCE)

    def complete_maintenance(self, vehicle: Vehicle) -> None:
        vehicle.perform_maintenance()


class RoutingService:

    def calculate_eta(self, distance_km: float, avg_speed_kmh: float = 60.0) -> timedelta:
        if avg_speed_kmh <= 0:
            return timedelta(hours=0)
        hours = distance_km / avg_speed_kmh
        return timedelta(hours=hours)

    def create_route(self, vehicle: Vehicle, points: List[RoutePoint], distances: List[float]) -> DeliveryRoute:
        if len(points) != len(distances):
            raise ValueError("Number of points must match number of distance segments")

        route = DeliveryRoute(
            id="ROUTE-" + datetime.now().strftime("%Y%m%d-%H%M%S"),
            vehicle=vehicle
        )

        for point, dist in zip(points, distances):
            route.add_point(point, dist)

        return route

    def optimize_route(self, route: DeliveryRoute) -> None:
        route.points.sort(key=lambda p: p.expected_arrival)
        pass

    def dispatch_route(self, route: DeliveryRoute) -> None:
        route.start_route()

    def report_arrival(self, route: DeliveryRoute, point_id: str) -> None:
        for i, point in enumerate(route.points):
            if point.id == point_id:
                route.complete_point(i)
                return