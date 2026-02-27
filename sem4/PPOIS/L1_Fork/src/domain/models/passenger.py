from typing import Optional
from src.domain.models.ticket import Ticket


class Passenger:
    def __init__(self, passenger_id: str, name: str):
        self._id = passenger_id
        self._name = name
        self._ticket: Optional[Ticket] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def ticket(self) -> Optional[Ticket]:
        return self._ticket

    def buy_ticket(self, ticket: Ticket) -> None:
        self._ticket = ticket

    def discard_ticket(self) -> None:
        self._ticket = None