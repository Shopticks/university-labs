from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from pharma_distributor.common.enums import DriverStatus, VehicleStatus, RouteStatus
from pharma_distributor.common.models import Address
from pharma_distributor.exceptions import LogisticsError, ValidationError


@dataclass
class Driver:
    """
    Represents a fleet driver.
    Tracks licensing, experience, and current availability status.
    """
    id: int
    license_number: str
    full_name: str
    experience_years: int
    _status: DriverStatus = field(default=DriverStatus.AVAILABLE)

    @property
    def status(self) -> DriverStatus:
        """
        Current operational status of the driver.
        """
        return self._status

    @property
    def is_available(self) -> bool:
        """
        Checks if the driver is currently available to take a new assignment.
        """
        return self._status == DriverStatus.AVAILABLE

    def assign_to_trip(self) -> None:
        """
        Marks the driver as currently performing a trip.

        Raises:
            LogisticsError: If the driver is not currently AVAILABLE.
        """
        if not self.is_available:
            raise LogisticsError(f"Driver {self.full_name} is not available (Status: {self.status})")
        self._status = DriverStatus.ON_TRIP

    def release_from_trip(self) -> None:
        """
        Marks the driver as available after completing a trip.
        """
        if self._status != DriverStatus.ON_TRIP:
            # Idempotent or log warning
            pass
        self._status = DriverStatus.AVAILABLE

    def go_off_duty(self) -> None:
        """
        Marks the driver as off-duty (e.g., end of shift).

        Raises:
            LogisticsError: If the driver is currently on a trip.
        """
        if self._status == DriverStatus.ON_TRIP:
            raise LogisticsError("Cannot go off-duty while on a trip")
        self._status = DriverStatus.OFF_DUTY


@dataclass(frozen=True)
class VehicleStats:
    """
    Technical specifications of a vehicle.
    """
    fuel_capacity_liters: float
    avg_consumption_per_100km: float
    max_load_kg: float
    maintenance_interval_km: float = 10000.0


@dataclass
class Vehicle:
    """
    Aggregate Root representing a delivery vehicle.
    Manages driver assignment, trip status, mileage tracking, and maintenance cycles.
    """
    id: str
    plate_number: str
    model: str
    stats: VehicleStats
    _status: VehicleStatus = field(default=VehicleStatus.IDLE)
    _current_driver: Optional[Driver] = None
    _mileage_km: float = 0.0
    _last_maintenance_km: float = 0.0

    @property
    def status(self) -> VehicleStatus:
        """
        Current operational status of the vehicle.
        """
        return self._status

    @property
    def current_driver(self) -> Optional[Driver]:
        """
        The driver currently assigned to this vehicle.
        """
        return self._current_driver

    @property
    def mileage(self) -> float:
        """
        Total accumulated mileage in kilometers.
        """
        return self._mileage_km

    def assign_driver(self, driver: Driver) -> None:
        """
        Assigns a driver to the vehicle.
        The vehicle must be IDLE and empty.

        Args:
            driver: The driver to assign.

        Raises:
            LogisticsError: If vehicle is not IDLE or already has a driver.
        """
        if self._status != VehicleStatus.IDLE:
            raise LogisticsError(f"Vehicle {self.plate_number} is not idle (Status: {self._status})")

        if self._current_driver is not None:
            raise LogisticsError(f"Vehicle already has a driver: {self._current_driver.full_name}")

        self._current_driver = driver

    def release_driver(self) -> None:
        """
        Unassigns the current driver.
        Cannot occur if the vehicle is currently on a route.
        """
        if self._status == VehicleStatus.ON_ROUTE:
            raise LogisticsError("Cannot release driver while vehicle is on route")

        self._current_driver = None

    def start_trip(self) -> None:
        """
        Transitions the vehicle to ON_ROUTE status.
        Requires a driver and valid maintenance status.

        Raises:
            LogisticsError: If no driver, vehicle not ready, or maintenance required.
        """
        if self._status != VehicleStatus.IDLE:
            raise LogisticsError(f"Vehicle not ready. Status: {self._status}")

        if not self._current_driver:
            raise LogisticsError("Cannot start trip without a driver")

        if self.needs_maintenance():
            raise LogisticsError(f"Vehicle {self.plate_number} needs maintenance before trip")

        self._status = VehicleStatus.ON_ROUTE
        self._current_driver.assign_to_trip()

    def complete_trip(self, distance_traveled_km: float) -> None:
        """
        Completes a trip, updates mileage, and releases the driver back to AVAILABLE status.

        Args:
            distance_traveled_km: The distance covered during the trip.

        Raises:
            LogisticsError: If vehicle was not on route.
        """
        if self._status != VehicleStatus.ON_ROUTE:
            raise LogisticsError("Vehicle is not on route")

        self._mileage_km += distance_traveled_km
        self._status = VehicleStatus.IDLE

        if self._current_driver:
            self._current_driver.release_from_trip()

    def needs_maintenance(self) -> bool:
        """
        Checks if the vehicle has exceeded its maintenance interval mileage.
        """
        km_since_service = self._mileage_km - self._last_maintenance_km
        return km_since_service >= self.stats.maintenance_interval_km

    def perform_maintenance(self) -> None:
        """
        Records maintenance performance and resets the service interval counter.
        """
        if self._status == VehicleStatus.ON_ROUTE:
            raise LogisticsError("Cannot service vehicle while on route")

        self._last_maintenance_km = self._mileage_km
        self._status = VehicleStatus.IDLE

    def calculate_fuel_required(self, distance_km: float) -> float:
        """
        Estimates fuel required for a given distance based on average consumption.
        """
        return (distance_km / 100.0) * self.stats.avg_consumption_per_100km


@dataclass
class RoutePoint:
    """
    Represents a stop on a delivery route.
    """
    id: str
    address: Address
    expected_arrival: datetime
    is_visited: bool = False
    actual_arrival: Optional[datetime] = None

    def mark_visited(self, arrival_time: datetime) -> None:
        """
        Marks this point as visited and records the actual arrival time.
        """
        self.is_visited = True
        self.actual_arrival = arrival_time


@dataclass
class DeliveryRoute:
    """
    Aggregate Root representing a planned sequence of delivery stops for a specific vehicle.
    """
    id: str
    vehicle: Vehicle
    points: List[RoutePoint] = field(default_factory=list)
    status: RouteStatus = RouteStatus.PLANNED
    estimated_distance_km: float = 0.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    def add_point(self, point: RoutePoint, distance_from_prev_km: float) -> None:
        """
        Adds a stop to the route. Can only be done during the planning phase.

        Args:
            point: The RoutePoint to add.
            distance_from_prev_km: Distance from the previous point (or start).

        Raises:
            LogisticsError: If the route has already started.
        """
        if self.status != RouteStatus.PLANNED:
            raise LogisticsError("Cannot add points to a route that has already started")

        self.points.append(point)
        self.estimated_distance_km += distance_from_prev_km

    def start_route(self) -> None:
        """
        Commences the delivery route.
        Starts the assigned vehicle and updates route status.

        Raises:
            ValidationError: If the route is empty.
            LogisticsError: If the route is not in PLANNED state.
        """
        if not self.points:
            raise ValidationError("Cannot start an empty route")

        if self.status != RouteStatus.PLANNED:
            raise LogisticsError("Route is not in PLANNED state")

        self.vehicle.start_trip()

        self.status = RouteStatus.IN_PROGRESS
        self.start_time = datetime.now()

    def complete_point(self, point_index: int) -> None:
        """
        Marks a specific stop on the route as completed.

        Args:
            point_index: The index of the point in the points list.
        """
        if self.status != RouteStatus.IN_PROGRESS:
            raise LogisticsError("Route is not in progress")

        if 0 <= point_index < len(self.points):
            self.points[point_index].mark_visited(datetime.now())
        else:
            raise ValidationError("Invalid point index")

    def finish_route(self, actual_total_distance_km: Optional[float] = None) -> None:
        """
        Completes the route and the vehicle's trip.

        Args:
            actual_total_distance_km: Optional actual distance recorded by odometer/GPS.
                                      Defaults to estimated distance if not provided.
        """
        if self.status != RouteStatus.IN_PROGRESS:
            raise LogisticsError("Route is not in progress")

        final_distance = actual_total_distance_km if actual_total_distance_km else self.estimated_distance_km

        self.vehicle.complete_trip(final_distance)

        self.status = RouteStatus.COMPLETED
        self.end_time = datetime.now()

    @property
    def estimated_fuel_consumption(self) -> float:
        """
        Calculates expected fuel consumption for the entire route.
        """
        return self.vehicle.calculate_fuel_required(self.estimated_distance_km)