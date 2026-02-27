from typing import List
from src.domain.models.passenger import Passenger

class Platform:
    def __init__(self, platform_id: str, number: int):
        self._id = platform_id
        self._number = number
        self._waiting_passengers: List[Passenger] =[]

    @property
    def id(self) -> str:
        return self._id

    @property
    def number(self) -> int:
        return self._number

    @property
    def waiting_passengers(self) -> List[Passenger]:
        return self._waiting_passengers.copy()

    def add_passenger(self, passenger: Passenger) -> None:
        self._waiting_passengers.append(passenger)

    def remove_passengers(self, passengers_to_remove: List[Passenger]) -> None:
        self._waiting_passengers =[
            p for p in self._waiting_passengers if p not in passengers_to_remove
        ]