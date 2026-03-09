from dataclasses import dataclass
from typing import List

from src.domain.models.station import Station

@dataclass
class RouteStop:
    """
    Represents a stop along a route with associated station, platform, and travel time information.
    
    Attributes:
        station (Station): The station where the stop occurs
        platform_number (int): The platform number at the station
        travel_time_to_next (int): Travel time in minutes to the next stop (0 if last stop)
    """
    station: Station
    platform_number: int
    travel_time_to_next: int


class Route:
    """
    Route class representation that manages a sequence of stops for transportation.
    """

    def __init__(self, route_id: str, name: str):
        """
        Initialize a Route instance.

        Args:
            route_id (str): Unique identifier for the route
            name (str): Name of the route
        """
        self._id = route_id
        self._name = name
        self._stops: List[RouteStop] = []

    @property
    def id(self) -> str:
        """
        Get the route's unique identifier.

        Returns:
            str: The route's ID
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Get the route's name.

        Returns:
            str: The route's name
        """
        return self._name

    @property
    def stops(self) -> List[RouteStop]:
        """
        Get a copy of the list of stops along the route.

        Returns:
            List[RouteStop]: A copy of the list of route stops
        """
        return self._stops.copy()

    def add_stop(self, stop: RouteStop) -> None:
        """
        Add a stop to the route.

        Args:
            stop (RouteStop): The stop to add to the route.
        """
        self._stops.append(stop)