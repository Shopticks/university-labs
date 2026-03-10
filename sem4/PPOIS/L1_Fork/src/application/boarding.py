from typing import List

from src.domain.models.train import Train, TrainState
from src.domain.models.platform import Platform
from src.domain.models.station import Station
from src.domain.models.passenger import Passenger

class BoardingService:
    """
    Service class that handles passenger boarding and alighting operations
    for trains at stations, including terminal and regular stops.
    """

    @staticmethod
    def process_terminal_stop(train: Train, station: Station) -> List[Passenger]:
        """
        Process a train arriving at a terminal station where all passengers must leave.
        The train is moved to depot status after unloading all passengers.

        Args:
            train (Train): The train arriving at the terminal station.
            station (Station): The terminal station where the train arrives.

        Returns:
            List[Passenger]: List of all passengers who were on the train.
        """

        train.set_state(TrainState.AT_STATION)
        train.record_stop()
        
        evicted_passengers = train.unload_all()
        
        for passenger in evicted_passengers:
            station.enter_concourse(passenger)
            
        train.set_state(TrainState.IN_DEPO)
        
        return evicted_passengers

    @staticmethod
    def process_regular_stop(
            train: Train, 
            station: Station, 
            platform: Platform
        ) -> List[Passenger]:
        """
        Process a train arriving at a regular station where some passengers may
        alight and others may board. Handles both departure and arrival operations.

        Args:
            train (Train): The train arriving at the station.
            station (Station): The station where the train stops.
            platform (Platform): The platform where passengers wait and board.

        Returns:
            List[Passenger]: List of passengers who alighted at this station.
        """

        train.set_state(TrainState.AT_STATION)
        train.record_stop()
        
        passengers_to_alight = [
            p for p in train.passengers 
            if p.destination_station_id == station.id
        ]
        
        train.alight(passengers_to_alight)
        
        for passenger in passengers_to_alight:
            station.enter_concourse(passenger)
            station.exit_station(passenger) 
            
        waiting = platform.waiting_passengers
        boarded_passengers = []
        
        for i in range(min(len(waiting), train.free_seats)):
            p = waiting[i]
            train.board(p)
            boarded_passengers.append(p)
            
        if boarded_passengers:
            platform.remove_passengers(boarded_passengers)
            
        return passengers_to_alight