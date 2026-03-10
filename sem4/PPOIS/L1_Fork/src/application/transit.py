from src.domain import Ticket
from src.domain import Turnstile, TurnstileState
from src.exceptions import (
    TurnstileLockedDownError, 
    TurnstileAlreadyUnlockedError
)

class TransitService:
    """
    Service class that handles transit-related operations such as 
    turnstile passage processing and ticket validation.
    """
    @staticmethod
    def process_turnstile_passage(ticket: Ticket, turnstile: Turnstile) -> None:
        """
        Process a passenger's passage through a turnstile using a valid ticket.
        
        Validates the turnstile state and ticket validity before allowing passage.
        The ticket is consumed (used) and the turnstile operation is performed.

        Args:
            ticket (Ticket): The ticket to be used for passage.
            turnstile (Turnstile): The turnstile through which passage is attempted.

        Raises:
            TurnstileLockedDownError: If the turnstile is in lockdown mode.
            TurnstileAlreadyUnlockedError: If the turnstile is already unlocked.
        """
        if turnstile.state == TurnstileState.LOCKED_DOWN:
            raise TurnstileLockedDownError("Refusal: The station is in lockdown mode")
        
        if turnstile.state == TurnstileState.UNLOCKED:
            raise TurnstileAlreadyUnlockedError("Refusal: The turnstile is already open, a passage is expected")

        ticket.use()

        turnstile.unlock()
        turnstile.pass_through()