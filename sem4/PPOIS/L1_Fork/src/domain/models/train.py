from enum import Enum
from typing import List, Optional

from src.domain.models.passenger import Passenger
from src.exceptions import (
    TrainFullError, 
    TrainNotEmptyError, 
    TrainNeedsMaintenanceError
)

class TrainState(Enum):
    """
    Enumeration representing the possible states of a train.
    """
    AT_STATION = "at_station"
    IN_TRANSIT = "in_transit"
    IN_DEPO = "in_depo"
    IDLE = "idle"


class Train:
    """
    Train class representing a transportation vehicle that can carry passengers
    between stations, with capacity management, maintenance scheduling, and
    state tracking capabilities.
    """
    def __init__(
            self, 
            train_id: str, 
            capacity: int, 
            stops_for_service: int = 10):
        """
        Initialize a Train instance.

        Args:
            train_id (str): Unique identifier for the train.
            capacity (int): Maximum number of passengers the train can carry
            stops_for_service (int, optional): Number of stops after which maintenance is required. \
                                               Defaults to 10.
        """
        self._id = train_id
        
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._state = TrainState.IN_DEPO
        self._passengers: List[Passenger] =[]

        if stops_for_service <= 0:
            raise ValueError("stops_for_service must be positive")
        self._stops_for_service = stops_for_service
        self._stops_count = 0

    @property
    def id(self) -> str:
        """
        Get the train's unique identifier.

        Returns:
            str: The train's ID.
        """
        return self._id
    
    @property
    def capacity(self) -> int:
        """
        Get the train's maximum passenger capacity.

        Returns:
            int: The maximum number of passengers the train can carry.
        """
        return self._capacity

    @property
    def state(self) -> TrainState:
        """
        Get the current state of the train.

        Returns:
            TrainState: The current operational state of the train.
        """
        return self._state

    @property
    def stops_for_service(self) -> int:
        """
        Get the number of stops after which maintenance is required.

        Returns:
            int: The number of stops before maintenance is needed.
        """
        return self._stops_for_service

    @property
    def stops_count(self) -> int:
        """
        Get the current count of stops made since last maintenance.

        Returns:
            int: Number of stops completed since last maintenance.
        """
        return self._stops_count

    @property
    def passengers(self) -> List[Passenger]:
        """
        Get a copy of the list of passengers currently on the train.

        Returns:
            List[Passenger]: Copy of the list of passengers on board.
        """
        return self._passengers.copy()

    @property
    def passenger_count(self) -> int:
        """
        Get the current number of passengers on the train.

        Returns:
            int: Number of passengers currently on board.
        """
        return len(self._passengers)

    @property
    def free_seats(self) -> int:
        """
        Get the number of available seats on the train.

        Returns:
            int: Number of seats still available for boarding.
        """
        return self._capacity - self.passenger_count
    
    @property
    def needs_maintenance(self) -> bool:
        """
        Check if the train requires maintenance.

        Returns:
            bool: True if the train has reached its maintenance threshold, False otherwise.
        """
        return self._stops_count >= self._stops_for_service

    def set_state(self, new_state: TrainState) -> None:
        """
        Change the train's operational state, with validation checks.

        Args:
            new_state (TrainState): The new state to transition to.

        Raises:
            TrainNotEmptyError: If attempting to move an inactive train with passengers on board.
            TrainNeedsMaintenanceError: If attempting to activate a train that requires maintenance/.
        """
        INACTIVE_STATES =[TrainState.IN_DEPO, TrainState.IDLE]
        ACTIVE_STATES =[TrainState.AT_STATION, TrainState.IN_TRANSIT]
        
        if new_state in INACTIVE_STATES and self.passenger_count > 0:
            raise TrainNotEmptyError(
                f"Train {self._id} cannot change state to {new_state.value} while passengers are inside"
            )
            
        if self._state in INACTIVE_STATES and new_state in ACTIVE_STATES:
            if self.needs_maintenance:
                raise TrainNeedsMaintenanceError(
                    f"Maintenance Block: Train {self._id} has reached its limit ({self._stops_count} stops). "
                    "It must be maintained before returning to service."
                )
        
        self._state = new_state

    def record_stop(self) -> None:
        """
        Record a stop made by the train and check if maintenance is needed.
        
        Prints a warning if the train has reached its maintenance threshold.
        """
        self._stops_count += 1
        if self.needs_maintenance:
            print(f"[WARNING] Train {self._id} needs maintenance! Stops: {self._stops_count}/{self._stops_for_service}")

    def board(self, passenger: Passenger) -> None:
        """
        Add a passenger to the train.

        Args:
            passenger (Passenger): The passenger to board the train.

        Raises:
            TrainFullError: If the train is already at maximum capacity.
        """
        if len(self._passengers) >= self._capacity:
            raise TrainFullError(f"Train {self._id} is full (Capacity: {self._capacity})")
        
        self._passengers.append(passenger)

    def alight(self, passengers_to_remove: List[Passenger]) -> None:
        """
        Remove specified passengers from the train.

        Args:
            passengers_to_remove (List[Passenger]): List of passengers to remove from the train.
        """
        self._passengers =[
            p for p in self._passengers if p not in passengers_to_remove
        ]
    
    def unload_all(self) -> List[Passenger]:
        """
        Remove all passengers from the train.

        Returns:
            List[Passenger]: List of all passengers who were on the train.
        """
        all_passengers = self._passengers.copy()
        self._passengers.clear()
        return all_passengers
    
    def maintain(self) -> None:
        """
        Perform maintenance on the train, resetting the stop counter.

        Raises:
            TrainNotEmptyError: If attempting to maintain a train with passengers on board.
        """
        if self.passenger_count > 0:
            raise TrainNotEmptyError(f"Cannot maintain train {self._id} while passengers are still on the board")
        
        if self._state != TrainState.IN_DEPO:
            self.set_state(TrainState.IN_DEPO)
            
        self._stops_count = 0