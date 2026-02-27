from enum import Enum
from datetime import datetime
from typing import Optional, Union

from src.exceptions import (
    TicketError,
    TicketExpiredError, 
    TicketExhaustedError
)

class TicketType(Enum):
    BY_TRIPS = "by_trips" # By value of trips
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Ticket:
    def __init__(
            self, 
            ticket_id: str, 
            ticket_type: TicketType,
            max_trips: int = 0,
            expires_at: Optional[datetime] = None
            ):
        
        self._id = ticket_id
        self._ticket_type = ticket_type

        self._max_trips = max_trips
        self._current_trips = 0

        # For optional value
        self._expires_at  = expires_at if expires_at is not None else datetime.now()

    def _validity_check(self):
        if self._ticket_type == TicketType.BY_TRIPS:
            if self._current_trips >= self._max_trips:
                raise TicketExhaustedError(f"The ticket (ID: {self._id}) has exhausted")
        else:
            if datetime.now() >= self._expires_at:
                raise TicketExpiredError(f"The ticket (ID: {self._id}) has expired")

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def ticket_type(self) -> TicketType:
        return self._ticket_type
    
    @property
    def remaining_trips(self) -> Union[int, float]:
        if self._ticket_type == TicketType.BY_TRIPS:
            return self._max_trips - self._current_trips
        
        return float('inf')
    
    @property
    def expiration_date(self) -> datetime:
        return self._expires_at
    
    @property
    def is_valid(self) -> bool:
        try:
            self._validity_check()
            return True
        except TicketError:
            return False

    def use(self) -> None:
        self._validity_check()

        if self._ticket_type == TicketType.BY_TRIPS:
            self._current_trips += 1