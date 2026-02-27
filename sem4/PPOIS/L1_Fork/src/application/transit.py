from src.domain import Ticket
from src.domain import Turnstile, TurnstileState
from src.exceptions import (
    TurnstileLockedDownError, 
    TurnstileAlreadyUnlockedError
)

class TransitService:
    @staticmethod
    def process_turnstile_passage(ticket: Ticket, turnstile: Turnstile) -> None:
        if turnstile.state == TurnstileState.LOCKED_DOWN:
            raise TurnstileLockedDownError("Refusal: The station is in lockdown mode.")
        
        if turnstile.state == TurnstileState.UNLOCKED:
            raise TurnstileAlreadyUnlockedError("Refusal: The turnstile is already open, a passage is expected.")

        ticket.use()

        turnstile.unlock()
        turnstile.pass_through()