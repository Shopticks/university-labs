from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from src.pharma_distributor.common.enums import DriverStatus, VehicleStatus, RouteStatus
from src.pharma_distributor.common.models import Address
from src.pharma_distributor.exceptions import LogisticsError, ValidationError


@dataclass
class Driver:
    id: int
    license_number: str
    full_name: str
    experience_years: int
    _status: DriverStatus = field(default=DriverStatus.AVAILABLE)

    @property
    def status(self) -> DriverStatus:
        return self._status

    @property
    def is_available(self) -> bool:
        return self._status == DriverStatus.AVAILABLE

    def assign_to_trip(self) -> None:
        if not self.is_available:
            raise LogisticsError(f"Driver {self.full_name} is not available (Status: {self.status})")
        self._status = DriverStatus.ON_TRIP

    def release_from_trip(self) -> None:
        if self._status != DriverStatus.ON_TRIP:
            pass
        self._status = DriverStatus.AVAILABLE

    def go_off_duty(self) -> None:
        if self._status == DriverStatus.ON_TRIP:
            raise LogisticsError("Cannot go off-duty while on a trip")
        self._status = DriverStatus.OFF_DUTY


@dataclass(frozen=True)
class VehicleStats:
    fuel_capacity_liters: float
    avg_consumption_per_100km: float
    max_load_kg: float
    maintenance_interval_km: float = 10000.0


@dataclass
class Vehicle:
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
        return self._status

    @property
    def current_driver(self) -> Optional[Driver]:
        return self._current_driver

    @property
    def mileage(self) -> float:
        return self._mileage_km

    def assign_driver(self, driver: Driver) -> None:
        if self._status != VehicleStatus.IDLE:
            raise LogisticsError(f"Vehicle {self.plate_number} is not idle (Status: {self._status})")

        if self._current_driver is not None:
            raise LogisticsError(f"Vehicle already has a driver: {self._current_driver.full_name}")

        self._current_driver = driver

    def release_driver(self) -> None:
        if self._status == VehicleStatus.ON_ROUTE:
            raise LogisticsError("Cannot release driver while vehicle is on route")

        self._current_driver = None

    def start_trip(self) -> None:
        if self._status != VehicleStatus.IDLE:
            raise LogisticsError(f"Vehicle not ready. Status: {self._status}")

        if not self._current_driver:
            raise LogisticsError("Cannot start trip without a driver")

        if self.needs_maintenance():
            raise LogisticsError(f"Vehicle {self.plate_number} needs maintenance before trip")

        self._status = VehicleStatus.ON_ROUTE
        self._current_driver.assign_to_trip()

    def complete_trip(self, distance_traveled_km: float) -> None:
        if self._status != VehicleStatus.ON_ROUTE:
            raise LogisticsError("Vehicle is not on route")

        self._mileage_km += distance_traveled_km
        self._status = VehicleStatus.IDLE

        if self._current_driver:
            self._current_driver.release_from_trip()

    def needs_maintenance(self) -> bool:
        km_since_service = self._mileage_km - self._last_maintenance_km
        return km_since_service >= self.stats.maintenance_interval_km

    def perform_maintenance(self) -> None:
        if self._status == VehicleStatus.ON_ROUTE:
            raise LogisticsError("Cannot service vehicle while on route")

        self._last_maintenance_km = self._mileage_km
        self._status = VehicleStatus.IDLE

    def calculate_fuel_required(self, distance_km: float) -> float:
        return (distance_km / 100.0) * self.stats.avg_consumption_per_100km


@dataclass
class RoutePoint:
    id: str
    address: Address
    expected_arrival: datetime
    # Можно добавить ссылку на OrderID
    is_visited: bool = False
    actual_arrival: Optional[datetime] = None

    def mark_visited(self, arrival_time: datetime) -> None:
        self.is_visited = True
        self.actual_arrival = arrival_time


@dataclass
class DeliveryRoute:
    id: str
    vehicle: Vehicle
    points: List[RoutePoint] = field(default_factory=list)
    status: RouteStatus = RouteStatus.PLANNED
    estimated_distance_km: float = 0.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    def add_point(self, point: RoutePoint, distance_from_prev_km: float) -> None:
        if self.status != RouteStatus.PLANNED:
            raise LogisticsError("Cannot add points to a route that has already started")

        self.points.append(point)
        self.estimated_distance_km += distance_from_prev_km

    def start_route(self) -> None:
        if not self.points:
            raise ValidationError("Cannot start an empty route")

        if self.status != RouteStatus.PLANNED:
            raise LogisticsError("Route is not in PLANNED state")

        self.vehicle.start_trip()

        self.status = RouteStatus.IN_PROGRESS
        self.start_time = datetime.now()

    def complete_point(self, point_index: int) -> None:
        if self.status != RouteStatus.IN_PROGRESS:
            raise LogisticsError("Route is not in progress")

        if 0 <= point_index < len(self.points):
            self.points[point_index].mark_visited(datetime.now())
        else:
            raise ValidationError("Invalid point index")

    def finish_route(self, actual_total_distance_km: Optional[float] = None) -> None:
        if self.status != RouteStatus.IN_PROGRESS:
            raise LogisticsError("Route is not in progress")

        final_distance = actual_total_distance_km if actual_total_distance_km else self.estimated_distance_km

        self.vehicle.complete_trip(final_distance)

        self.status = RouteStatus.COMPLETED
        self.end_time = datetime.now()

    @property
    def estimated_fuel_consumption(self) -> float:
        return self.vehicle.calculate_fuel_required(self.estimated_distance_km)