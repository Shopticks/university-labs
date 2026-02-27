from typing import Dict, List
from src.domain.models.platform import Platform
from src.domain.models.turnstile import Turnstile
from src.exceptions import StationError

class Station:
    def __init__(self, station_id: str, name: str):
        self._id = station_id
        self._name = name
        
        self._platforms: Dict[int, Platform] = {}
        self._turnstiles: Dict[str, Turnstile] = {}

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def platforms(self) -> List[Platform]:
        return list(self._platforms.values())

    @property
    def turnstiles(self) -> List[Turnstile]:
        return list(self._turnstiles.values())

    def add_platform(self, platform: Platform) -> None:
        self._platforms[platform.number] = platform

    def get_platform(self, number: int) -> Platform:
        if number not in self._platforms:
            raise StationError(f"Station {self._name} does not contain platform {number}")
        
        return self._platforms[number]

    def add_turnstile(self, turnstile: Turnstile) -> None:
        self._turnstiles[turnstile.id] = turnstile
    
    def lockdown(self) -> None:
        for turnstile in self._turnstiles.values():
            turnstile.lockdown()

    def lift_lockdown(self) -> None:
        for turnstile in self._turnstiles.values():
            turnstile.remove_lockdown()