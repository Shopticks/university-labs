from src.domain.models.train import Train, TrainState
from src.domain.models.platform import Platform

class BoardingService:
    @staticmethod
    def process_terminal_stop(train: Train, platform: Platform) -> None:
        train.set_state(TrainState.AT_STATION)
        
        evicted_passengers = train.unload_all()
        
        for passenger in evicted_passengers:
            platform.add_passenger(passenger)
            
        train.set_state(TrainState.IN_DEPO)

    @staticmethod
    def process_regular_stop(train: Train, platform: Platform) -> None:
        train.set_state(TrainState.AT_STATION)
        
        passengers_alighting = train.passengers[:2]
        train.alight(passengers_alighting)
        for p in passengers_alighting:
            platform.add_passenger(p)
            
        waiting = platform.waiting_passengers
        for i in range(min(len(waiting), train.free_seats)):
            p = waiting[i]
            train.board(p)
            platform.remove_passengers([p])