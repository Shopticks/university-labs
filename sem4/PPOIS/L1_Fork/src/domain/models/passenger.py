from typing import Optional
from src.domain.models.ticket import Ticket


class Passenger:
    """
    Passenger class representation.
    """

    def __init__(self, passenger_id: str, name: str, destination_station_id: Optional[str] = None):
        """
        Initialize the class instance.

        Args:
            passenger_id (str): Unique identifier for the passenger.
            name (str): Name of the passenger.
            destination_station_id (Optional[str], optional): ID of the destination station. Defaults to None.
        """
        self._id = passenger_id
        self._name = name
        self._ticket: Optional[Ticket] = None
        self._destination_station_id = destination_station_id

    @property
    def id(self) -> str:
        """GGet the passenger's unique identifier.

        Returns:
            str: Passenger ID.
        """
        return self._id

    @property
    def name(self) -> str:
        """Get the passenger's name.

        Returns:
            str: Name of the passenger.
        """
        return self._name

    @property
    def ticket(self) -> Optional[Ticket]:
        """Get the passenger's ticket.

        Returns:
            Optional[Ticket]: Ticket of the passenger or None.
        """
        return self._ticket
    
    @property
    def destination_station_id(self) -> Optional[str]:
        """Get the passenger's destination station ID.

        Returns:
            Optional[str]: 
        """
        return self._destination_station_id

    def buy_ticket(self, ticket: Ticket) -> None:
        """Assign a ticket to the passenger.

        Args:
            ticket (Ticket): The ticket to assign.
        """
        self._ticket = ticket

    def discard_ticket(self) -> None:
        """
        Remove the passenger's current ticket.
        """
        self._ticket = None

    def set_destination(self, station_id: str) -> None:
        """Set new passenger's destination station.

        Args:
            station_id (str): The ID of the destination station to set.
        """
        self._destination_station_id = station_id