from enum import Enum
from typing import List

from src.domain.models.passenger import Passenger
from src.exceptions import (
    TrainFullError, 
    TrainNotEmptyError, 
    TrainNeedsMaintenanceError
)

class TrainState(Enum):
    AT_STATION = "at_station"
    IN_TRANSIT = "in_transit"
    IN_DEPO = "in_depo"
    IDLE = "idle"


class Train:
    def __init__(self, train_id: str, capacity: int, stops_for_service: int = 10):
        self._id = train_id
        self._capacity = capacity
        self._state = TrainState.IN_DEPO
        self._passengers: List[Passenger] = []

        self._stops_for_service = stops_for_service
        self._stops_count = 0

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def state(self) -> TrainState:
        return self._state

    @property
    def passengers(self) -> List[Passenger]:
        return self._passengers.copy()

    @property
    def passenger_count(self) -> int:
        return len(self._passengers)

    @property
    def free_seats(self) -> int:
        return self._capacity - self.passenger_count
    
    @property
    def needs_maintenance(self) -> bool:
        return self._stops_count >= self._stops_for_service

    def set_state(self, new_state: TrainState) -> None:
        INACTIVE_STATES = [TrainState.IN_DEPO, TrainState.IDLE]
        ACTIVE_STATES = [TrainState.AT_STATION, TrainState.IN_TRANSIT]
        
        if new_state in INACTIVE_STATES and self.passenger_count > 0:
            raise TrainNotEmptyError(
                f"Train {self._id} cannot change state to {new_state.value} while passengers are inside"
            )
            
        if self._state in INACTIVE_STATES and new_state in ACTIVE_STATES:
            if self.needs_maintenance:
                raise TrainNeedsMaintenanceError(
                    f"Maintenance Block: Train {self._id} has reached its limit ({self._stops_count} stops). "
                    "It must be maintained before returning to service"
                )
        
        self._state = new_state

    def record_stop(self) -> None:
        self._stops_count += 1
        if self.needs_maintenance:
            print(f"[WARNING] Train {self._id} needs maintenance! Stops: {self._stops_count}/{self._stops_for_service}")

    def board(self, passenger: Passenger) -> None:
        if len(self._passengers) >= self._capacity:
            raise TrainFullError(f"Train {self._id} is full (Capacity: {self._capacity})")
        
        self._passengers.append(passenger)

    def alight(self, passengers_to_remove: List[Passenger]) -> None:
        self._passengers = [
            p for p in self._passengers if p not in passengers_to_remove
        ]
    
    def unload_all(self) -> List[Passenger]:
        all_passengers = self._passengers.copy()
        self._passengers.clear()
        return all_passengers
    
    def maintain(self) -> None:
        if self.passenger_count > 0:
            raise TrainNotEmptyError(f"Cannot maintain train {self._id} while passengers are still on the board")
        
        if self._state != TrainState.IN_DEPO:
            self.set_state(TrainState.IN_DEPO)
        
        print(f"Train {self._id} is under maintenance...")
        self._stops_count = 0