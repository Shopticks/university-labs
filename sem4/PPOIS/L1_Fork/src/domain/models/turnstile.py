from enum import Enum
from src.exceptions import (
    TurnstileLockedError,
    TurnstileAlreadyUnlockedError,
    TurnstileLockedDownError
)


class TurnstileState(Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    LOCKED_DOWN = "locked_down"


class Turnstile:
    def __init__(self, turnstile_id: str):
        self._id = turnstile_id
        self._state = TurnstileState.LOCKED

    def _check_lockdown(self):
        if self._state == TurnstileState.LOCKED_DOWN:
            raise TurnstileLockedDownError(f"Turnstile {self._id} is in security LOCKDOWN")

    @property
    def id(self) -> str:
        return self._id

    @property
    def state(self) -> TurnstileState:
        return self._state

    def unlock(self) -> None:
        self._check_lockdown();
        
        if self._state == TurnstileState.UNLOCKED:
            raise TurnstileAlreadyUnlockedError(f"Turnstile {self._id} is already unlocked.")

        self._state = TurnstileState.UNLOCKED

    def lock(self) -> None:
        self._check_lockdown()

        self._state = TurnstileState.LOCKED

    def pass_through(self) -> None:
        self._check_lockdown()

        if self._state == TurnstileState.LOCKED:
            raise TurnstileLockedError(f"Turnstile {self._id} is locked. Cannot pass.")

        self.lock()

    def lockdown(self) -> None:
        self._state = TurnstileState.LOCKED_DOWN

    def remove_lockdown(self) -> None:
        self._state = TurnstileState.LOCKED