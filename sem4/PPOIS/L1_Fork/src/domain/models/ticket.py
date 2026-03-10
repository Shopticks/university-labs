from enum import Enum
from datetime import datetime
from typing import Optional, Union

from src.exceptions import (
    TicketError,
    TicketExpiredError, 
    TicketExhaustedError
)

class TicketType(Enum):
    """
    Enumeration of different ticket types available in the system.
    """
    BY_TRIPS = "by_trips" 
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Ticket:
    """
    Ticket class representing a valid pass for transportation services.
    Supports both trip-based and time-based ticket types with appropriate
    validity checks and usage tracking.
    """
    def __init__(
            self, 
            ticket_id: str, 
            ticket_type: TicketType,
            max_trips: int = 0,
            expires_at: Optional[datetime] = None
            ):
        """
        Initialize a Ticket instance.

        Args:
            ticket_id (str): Unique identifier for the ticket/
            ticket_type (TicketType): Type of ticket (BY_TRIPS, DAILY, WEEKLY, or MONTHLY).
            max_trips (int, optional): Maximum number of trips allowed for BY_TRIPS tickets. Defaults to 0.
            expires_at (Optional[datetime], optional): Expiration datetime for time-based tickets. \
                                                        Defaults to current datetime if None provided.
        """

        self._id = ticket_id
        self._ticket_type = ticket_type

        if max_trips < 0:
            raise ValueError("max_trips cannot be negative")
        self._max_trips = max_trips
        self._current_trips = 0

        self._expires_at  = expires_at if expires_at is not None else datetime.now()

    def _validity_check(self):
        """
        Internal method to check if the ticket is still valid based on its type.

        Raises:
            TicketExhaustedError: If a BY_TRIPS ticket has reached its maximum trip limit.
            TicketExpiredError: If a time-based ticket has passed its expiration date.
        """
        if self._ticket_type == TicketType.BY_TRIPS:
            if self._current_trips >= self._max_trips:
                raise TicketExhaustedError(f"The ticket (ID: {self._id}) has exhausted")
        else:
            if datetime.now() >= self._expires_at:
                raise TicketExpiredError(f"The ticket (ID: {self._id}) has expired")

    @property
    def id(self) -> str:
        """
        Get the ticket's unique identifier.

        Returns:
            str: The ticket's ID.
        """
        return self._id
    
    @property
    def ticket_type(self) -> TicketType:
        """
        Get the ticket's type.

        Returns:
            TicketType: The type of the ticket.
        """
        return self._ticket_type
        
    @property
    def max_trips(self) -> int:
        """
        Get the maximum number of trips allowed for this ticket.

        Returns:
            int: Maximum number of trips (0 for time-based tickets).
        """
        return self._max_trips
        
    @property
    def current_trips(self) -> int:
        """
        Get the number of trips already used on this ticket.

        Returns:
            int: Number of trips already taken.
        """
        return self._current_trips
        
    @property
    def expires_at(self) -> datetime:
        """
        Get the expiration datetime of the ticket.

        Returns:
            datetime: The datetime when the ticket expires.
        """
        return self._expires_at
    
    @property
    def remaining_trips(self) -> Union[int, float]:
        """
        Get the number of remaining trips for this ticket.

        Returns:
            Union[int, float]: Number of remaining trips (infinity for time-based tickets).
        """
        if self._ticket_type == TicketType.BY_TRIPS:
            return self._max_trips - self._current_trips
        
        return float('inf')
    
    @property
    def expiration_date(self) -> datetime:
        """
        Get the expiration date and time of the ticket.

        Returns:
            datetime: The expiration datetime of the ticket.
        """
        return self._expires_at
    
    @property
    def is_valid(self) -> bool:
        """
        Check if the ticket is currently valid.

        Returns:
            bool: True if the ticket is valid, False otherwise.
        """
        try:
            self._validity_check()
            return True
        except TicketError:
            return False

    def use(self) -> None:
        """
        Mark the ticket as used once, incrementing the trip counter for BY_TRIPS tickets.
        
        Raises:
            TicketExhaustedError: If a BY_TRIPS ticket has reached its maximum trip limit.
            TicketExpiredError: If a time-based ticket has passed its expiration date.
        """
        self._validity_check()

        if self._ticket_type == TicketType.BY_TRIPS:
            self._current_trips += 1