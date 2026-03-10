from typing import List
from datetime import datetime

from src.domain.models.train import Train, TrainState
from src.domain.models.route import Route
from src.application.boarding import BoardingService

class ActiveDispatch:
    """
    Represents a train currently operating on a route, tracking its position,
    timing, and operational state during transit.
    """
    def __init__(self, train: Train, route: Route):
        """
        Initialize an ActiveDispatch instance.

        Args:
            train (Train): The train being dispatched.
            route (Route): The route the train is following.
        """
        self.train = train
        self.route = route
        self.current_stop_index = 0
        self.timer = 0 

    @property
    def is_dwelling(self) -> bool: 
        """
        Check if the train is currently dwelling at a station.

        Returns:
            bool: True if the train is at a station, False otherwise.
        """
        return self.train.state == TrainState.AT_STATION
    

class ScheduleService:
    """
    Service class that manages the scheduling and movement of trains on routes,
    handling timing, dispatching, and the progression of trains through their routes.
    """
    def __init__(self):
        """
        Initialize a ScheduleService instance.
        """
        self._current_time_minutes = 0
        self._active_dispatches: List[ActiveDispatch] =[]

    @property
    def current_time_minutes(self) -> int:
        """
        Get the current simulation time in minutes.

        Returns:
            int: Current time in minutes since start of simulation.
        """
        return self._current_time_minutes

    @current_time_minutes.setter
    def current_time_minutes(self, value: int):
        """
        Set the current simulation time in minutes.

        Args:
            value (int): New time value in minutes.
        """

        self._current_time_minutes = value

    @property
    def active_dispatches(self) -> List[ActiveDispatch]:
        """
        Get the list of currently active train dispatches.

        Returns:
            List[ActiveDispatch]: List of active dispatch instances.
        """
        return self._active_dispatches

    @property
    def current_time_str(self) -> str:
        """
        Get the current simulation time formatted as HH:MM.

        Returns:
            str: Current time formatted as HH:MM string.
        """
        total_minutes = (6 * 60) + self._current_time_minutes
        hours = (total_minutes // 60) % 24
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"

    def dispatch_train(self, train: Train, route: Route) -> None:
        """
        Dispatch a train onto a route, starting its journey.

        Args:
            train (Train): The train to dispatch.
            route (Route): The route for the train to follow.
        """
        train.set_state(TrainState.IN_TRANSIT)
        
        dispatch = ActiveDispatch(train, route)
        dispatch.timer = route.stops[0].travel_time_to_next
        self._active_dispatches.append(dispatch)
        print(f"[{self.current_time_str}] Manager: The train {train.id} went on the route '{route.name}'")

    def tick(self) -> None:
        """
        Advance the simulation by one minute and process all active dispatches.
        """
        self._current_time_minutes += 1
        print(f"\n--- Time: {self.current_time_str} ---")

        for dispatch in self._active_dispatches.copy():
            self._process_dispatch(dispatch)

    def _process_dispatch(self, dispatch: ActiveDispatch) -> None:
        """
        Process the movement and actions for a single dispatch instance.

        Args:
            dispatch (ActiveDispatch): The dispatch instance to process.
        """
        dispatch.timer -= 1

        if dispatch.timer > 0:
            return

        current_stop = dispatch.route.stops[dispatch.current_stop_index]
        is_last_stop = (dispatch.current_stop_index == len(dispatch.route.stops) - 1)
        
        if not dispatch.is_dwelling:
            if is_last_stop:
                print(f"[{self.current_time_str}] The train {dispatch.train.id} arrived at the TERMINAL station {current_stop.station.name}")
                BoardingService.process_terminal_stop(dispatch.train, current_stop.station)
                self._active_dispatches.remove(dispatch)
                print(f"[{self.current_time_str}] The train {dispatch.train.id} is sent to the DEPO")
            else:
                BoardingService.process_regular_stop(
                    dispatch.train, current_stop.station, 
                    current_stop.station.get_platform(current_stop.platform_number)
                )
                dispatch.timer = 1 
                print(f"[{self.current_time_str}] The train {dispatch.train.id} arrived on {current_stop.station.name}. Boarding...")
        else:
            train = dispatch.train
            train.set_state(TrainState.IN_TRANSIT)
            dispatch.timer = current_stop.travel_time_to_next
            dispatch.current_stop_index += 1
            
            next_stop = dispatch.route.stops[dispatch.current_stop_index]
            print(f"[{self.current_time_str}] The train {dispatch.train.id} went to the next station ({next_stop.station.name})")