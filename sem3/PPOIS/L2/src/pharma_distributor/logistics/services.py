from datetime import timedelta, datetime
from typing import List

from pharma_distributor.logistics.models import (
    Vehicle,
    Driver,
    DeliveryRoute,
    RoutePoint,
    VehicleStatus
)
from pharma_distributor.exceptions import LogisticsError


class FleetManager:
    """
    Domain service for managing vehicle assets and driver assignments.
    """

    def assign_driver_to_vehicle(self, vehicle: Vehicle, driver: Driver) -> None:
        """
        Links a driver to a vehicle.
        """
        vehicle.assign_driver(driver)

    def end_driver_shift(self, vehicle: Vehicle) -> None:
        """
        Unassigns the driver from the vehicle at the end of a shift.
        """
        vehicle.release_driver()

    def send_to_maintenance(self, vehicle: Vehicle) -> None:
        """
        Flags a vehicle for maintenance.
        The vehicle must not be on an active route.
        If a driver is assigned, they are released.

        Args:
            vehicle: The vehicle to service.

        Raises:
            LogisticsError: If the vehicle is currently on a route.
        """
        if vehicle.status == VehicleStatus.ON_ROUTE:
            raise LogisticsError(f"Cannot send vehicle {vehicle.plate_number} to maintenance: currently on route")

        if vehicle.current_driver:
            vehicle.release_driver()

        # Accessing protected field for status update logic
        object.__setattr__(vehicle, '_status', VehicleStatus.MAINTENANCE)

    def complete_maintenance(self, vehicle: Vehicle) -> None:
        """
        Marks maintenance as complete and returns the vehicle to IDLE status.
        """
        vehicle.perform_maintenance()


class RoutingService:
    """
    Domain service for calculating logic related to routes, ETAs, and dispatching.
    """

    def calculate_eta(self, distance_km: float, avg_speed_kmh: float = 60.0) -> timedelta:
        """
        Estimates travel time based on distance and average speed.

        Args:
            distance_km: Distance in kilometers.
            avg_speed_kmh: Average speed (default 60 km/h).

        Returns:
            timedelta: The estimated time duration.
        """
        if avg_speed_kmh <= 0:
            return timedelta(hours=0)
        hours = distance_km / avg_speed_kmh
        return timedelta(hours=hours)

    def create_route(self, vehicle: Vehicle, points: List[RoutePoint], distances: List[float]) -> DeliveryRoute:
        """
        Factory method to create a new delivery route plan.

        Args:
            vehicle: The vehicle assigned to the route.
            points: Ordered list of stops.
            distances: List of distances (segment lengths) corresponding to points.

        Raises:
            ValueError: If the number of points does not match the number of distance segments.
        """
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
        """
        Reorders route points for efficiency.
        Currently implements a simple sort by expected arrival time.
        """
        route.points.sort(key=lambda p: p.expected_arrival)
        # In a real scenario, this would involve TSP algorithms (e.g., OR-Tools)
        pass

    def dispatch_route(self, route: DeliveryRoute) -> None:
        """
        Starts the execution of a planned route.
        """
        route.start_route()

    def report_arrival(self, route: DeliveryRoute, point_id: str) -> None:
        """
        Updates the route status indicating a specific point has been visited.

        Args:
            route: The active delivery route.
            point_id: The ID of the visited point.
        """
        for i, point in enumerate(route.points):
            if point.id == point_id:
                route.complete_point(i)
                return