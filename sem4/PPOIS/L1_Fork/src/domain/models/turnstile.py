from enum import Enum
from src.exceptions import (
    TurnstileLockedError,
    TurnstileAlreadyUnlockedError,
    TurnstileLockedDownError
)


class TurnstileState(Enum):
    """
    Enumeration representing the possible states of a turnstile.
    """
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    LOCKED_DOWN = "locked_down"


class Turnstile:
    """
    Turnstile class representing a gate control device that manages passenger access
    to and from a station, with support for lockdown functionality for security purposes.
    """

    def __init__(self, turnstile_id: str):
        """
        Initialize a Turnstile instance.

        Args:
            turnstile_id (str): Unique identifier for the turnstile.
        """
        self._id = turnstile_id
        self._state = TurnstileState.LOCKED

    def _check_lockdown(self):
        """
        Internal method to check if the turnstile is in lockdown mode.
        
        Raises:
            TurnstileLockedDownError: If the turnstile is in lockdown state.
        """
        if self._state == TurnstileState.LOCKED_DOWN:
            raise TurnstileLockedDownError(f"Turnstile {self._id} is in security LOCKDOWN")

    @property
    def id(self) -> str:
        """
        Get the turnstile's unique identifier.

        Returns:
            str: The turnstile's ID.
        """
        return self._id

    @property
    def state(self) -> TurnstileState:
        """
        Get the current state of the turnstile.

        Returns:
            TurnstileState: The current operational state of the turnstile.
        """
        return self._state

    def unlock(self) -> None:
        """
        Unlock the turnstile to allow passage.
        
        Raises:
            TurnstileLockedDownError: If the turnstile is in lockdown mode.
            TurnstileAlreadyUnlockedError: If the turnstile is already unlocked.
        """
        self._check_lockdown();
        
        if self._state == TurnstileState.UNLOCKED:
            raise TurnstileAlreadyUnlockedError(f"Turnstile {self._id} is already unlocked")

        self._state = TurnstileState.UNLOCKED

    def lock(self) -> None:
        """
        Lock the turnstile to prevent passage.
        
        Raises:
            TurnstileLockedDownError: If the turnstile is in lockdown mode.
        """
        self._check_lockdown()

        self._state = TurnstileState.LOCKED

    def pass_through(self) -> None:
        """
        Allow a passenger to pass through the turnstile.
        Automatically locks the turnstile after passage.
        
        Raises:
            TurnstileLockedDownError: If the turnstile is in lockdown mode.
            TurnstileLockedError: If the turnstile is in locked state.
        """
        self._check_lockdown()

        if self._state == TurnstileState.LOCKED:
            raise TurnstileLockedError(f"Turnstile {self._id} is locked. Cannot pass")

        self.lock()

    def lockdown(self) -> None:
        """
        Put the turnstile into lockdown mode, preventing all operations until lifted.
        """
        self._state = TurnstileState.LOCKED_DOWN

    def remove_lockdown(self) -> None:
        """
        Remove the lockdown mode and return the turnstile to locked state.
        """
        self._state = TurnstileState.LOCKED