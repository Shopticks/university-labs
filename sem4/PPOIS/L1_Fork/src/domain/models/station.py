from typing import Dict, List
from src.domain.models.platform import Platform
from src.domain.models.turnstile import Turnstile
from src.domain.models.passenger import Passenger
from src.domain.models.ticket_office import TicketOffice
from src.exceptions import StationError

class Station:
    """
    Station class representation that manages platforms, turnstiles, ticket offices,
    and passenger movement within a transportation station.
    """

    def __init__(self, station_id: str, name: str):
        """
        Initialize a Station instance.

        Args:
            station_id (str): Unique ID for the station.
            name (str): Name of the station.
        """
        self._id = station_id
        self._name = name
        
        self._platforms: Dict[int, Platform] = {}
        self._turnstiles: Dict[str, Turnstile] = {}
        self._ticket_offices: Dict[str, TicketOffice] = {}

        self._concourse_passengers: List[Passenger] = []

    @property
    def id(self) -> str:
        """
        Get the station's unique identifier.

        Returns:
            str: The station's id.
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Get the station's name.

        Returns:
            str: The station's name.
        """
        return self._name

    @property
    def platforms(self) -> List[Platform]:
        """
        Get a list of all platforms in the station.

        Returns:
            List[Platform]: List of the platforms.
        """
        return list(self._platforms.values())

    @property
    def turnstiles(self) -> List[Turnstile]:
        """
        Get a list of all turnstiles in the station.

        Returns:
            List[Turnstile]: List of the turnstiles.
        """
        return list(self._turnstiles.values())

    @property
    def concourse_passengers(self) -> List[Passenger]:
        """
        Get a list of all passengers on the concourse. 

        Returns:
            List[Passenger]: List of the passengers in the concourse.
        """
        return self._concourse_passengers.copy()
    
    @property
    def ticket_offices(self) -> List[TicketOffice]:
        """
        Get a list of all ticket offices in the station.

        Returns:
            List[TicketOffice]: List of the ticket offices.
        """
        return list(self._ticket_offices.values())

    def add_platform(self, platform: Platform) -> None:
        """
        Add a platform to the station.

        Args:
            platform (Platform): The platform object to add to the station
        """
        self._platforms[platform.number] = platform

    def get_platform(self, number: int) -> Platform:
        """
        Retrieve a platform by its number.

        Args:
            number (int): Number of the platform to get.

        Raises:
            StationError: If no platform exists with the given number.

        Returns:
            Platform: The platform object with the specified number.
        """

        if number not in self._platforms:
            raise StationError(f"Station {self._name} does not contain platform {number}")
        
        return self._platforms[number]

    def add_turnstile(self, turnstile: Turnstile) -> None:
        """
        Adding turnstile to the station.

        Args:
            turnstile (Turnstile): The turnstule object to add.
        """
        self._turnstiles[turnstile.id] = turnstile
    
    def lockdown(self) -> None:
        """
        Lockdown the station.
        """
        for turnstile in self._turnstiles.values():
            turnstile.lockdown()

    def lift_lockdown(self) -> None:
        """
        Lift lockdown from the station.
        """
        for turnstile in self._turnstiles.values():
            turnstile.remove_lockdown()

    def enter_concourse(self, passenger: Passenger) -> None:
        """
        Move the passenger to the station concourse.

        Args:
            passenger (Passenger): The passenger object to move on.
        """
        self._concourse_passengers.append(passenger)

    def route_to_platform(self, passenger: Passenger, platform_number: int) -> None:
        """
        Move the passenger to the platform.

        Args:
            passenger (Passenger): The passenger's object to move.
            platform_number (int): Moving platform number.

        Raises:
            StationError: If the passenger cannot be moved to the platform (passenger not in the concourse).
        """
        if passenger not in self._concourse_passengers:
            raise StationError(f"Passenger {passenger.name} is not in the concourse of station {self._name}")
        
        platform = self.get_platform(platform_number)
        
        self._concourse_passengers.remove(passenger)
        platform.add_passenger(passenger)

    def return_to_concourse(self, passenger: Passenger, platform_number: int) -> None:
        """
        Move the passenger to the concourse.

        Args:
            passenger (Passenger): The passenger's object to move.
            platform_number (int): The number of the platform from which to move.

        Raises:
            StationError: If the passenger not in the platform.
        """
        platform = self.get_platform(platform_number)
        
        if passenger not in platform.waiting_passengers:
            raise StationError(f"Passenger {passenger.name} is not on platform {platform_number}")
        
        platform.remove_passengers([passenger])
        self._concourse_passengers.append(passenger)
        
    def exit_station(self, passenger: Passenger) -> None:
        """
        Remove a passenger from the station concourse.

        Args:
            passenger (Passenger): The passenger to remove from the station

        Raises:
            StationError: If the passenger is not in the concourse
        """
        if passenger not in self._concourse_passengers:
            raise StationError(f"Passenger {passenger.name} is not in the concourse, cannot exit")
        
        self._concourse_passengers.remove(passenger)

    def add_ticket_office(self, office: TicketOffice) -> None:
        """
        Add a ticket office to the station.

        Args:
            office (TicketOffice): The ticket office object to add to the station.
        """
        self._ticket_offices[office.id] = office
        
    def get_ticket_office(self, office_id: str) -> TicketOffice:
        """
        Retrieve a ticket office by its ID.

        Args:
            office_id (str): The ID of the ticket office to retrieve.

        Raises:
            StationError: If no ticket office exists with the given ID.

        Returns:
            TicketOffice: The ticket office object with the specified ID
        """
        if office_id not in self._ticket_offices:
            raise StationError(f"Ticket office {office_id} not found at station {self._name}")
        
        return self._ticket_offices[office_id]