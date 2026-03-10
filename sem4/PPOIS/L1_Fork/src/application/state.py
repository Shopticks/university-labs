from typing import Dict
from src.domain.models.station import Station
from src.domain.models.route import Route
from src.domain.models.train import Train
from src.domain.models.passenger import Passenger
from src.application.schedule import ScheduleService

class AppState:
    def __init__(self):
        self.stations: Dict[str, Station] = {}
        self.routes: Dict[str, Route] = {}
        self.trains: Dict[str, Train] = {}
        self.passengers: Dict[str, Passenger] = {}
        self.schedule = ScheduleService()
        self.save_file = "metro_state.json"