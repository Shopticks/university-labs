from typing import List

from src.domain.models.passenger import Passenger
from src.exceptions import PlatformOperationError

class Platform:
    """
    Platform class representation that manages passengers waiting at a specific platform.
    """

    def __init__(self, platform_id: str, number: int):
        """
        Initialize a Platform instance.

        Args:
            platform_id (str): Unique platform identifier.
            number (int): Platform number for the identication.
        """
        self._id = platform_id
        self._number = number
        self._waiting_passengers: List[Passenger] =[]

    @property
    def id(self) -> str:
        """
        Get the platform's unique identifier.

        Returns:
            str: The platform's ID.
        """
        return self._id

    @property
    def number(self) -> int:
        """
        Get the paltform's number.

        Returns:
            int: The platform number.
        """
        return self._number

    @property
    def waiting_passengers(self) -> List[Passenger]:
        """
        Get a copy of the list of passengers waiting on the platform.

        Returns:
            List[Passenger]: A copy of the list of waiting passengers.
        """
        return self._waiting_passengers.copy()

    def add_passenger(self, passenger: Passenger) -> None:
        """
        Add a passenger to the platform's waiting list.

        Args:
            passenger (Passenger): The passenger to add to the platform.

        Raises:
            PlatformOperationError: Raises when a passenger already in the waiting list.
        """
        
        if passenger in self._waiting_passengers:
            raise PlatformOperationError("The passenger are already in the waiting list.")
        
        self._waiting_passengers.append(passenger)

    def add_passengers(self, passengers: List[Passenger]) -> None:
        """
        Add multiple passengers to the platform's waiting list.

        Args:
            passengers (List[Passenger]): List of the passengers

        Raises:
            PlatformOperationError: Raises when aby passenger already in the waiting list.
        """

        for passenger in passengers:
            self.add_passenger(passenger)

    def remove_passengers(self, passengers_to_remove: List[Passenger]) -> None:
        """
        Remove 

        Args:
            passengers_to_remove (List[Passenger]): _description_
        """
        self._waiting_passengers =[
            p for p in self._waiting_passengers if p not in passengers_to_remove
        ]