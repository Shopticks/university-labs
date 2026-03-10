from typing import Tuple
from src.domain.models.passenger import Passenger
from src.domain.models.ticket_office import TicketOffice
from src.domain.models.ticket import TicketType, Ticket
from src.domain.models.money import Money

class SalesService:
    """
    Service class that handles ticket sales and purchases for passengers.
    Manages the transaction between passengers and ticket offices.
    """

    @staticmethod
    def process_ticket_purchase(
        passenger: Passenger, 
        office: TicketOffice, 
        ticket_type: TicketType, 
        trips: int, 
        tendered_money: Money
    ) -> Tuple[Ticket, Money]:
        """
        Process a ticket purchase transaction for a passenger.

        Args:
            passenger (Passenger): The passenger making the purchase.
            office (TicketOffice): The ticket office where the purchase is made.
            ticket_type (TicketType): The type of ticket to purchase.
            trips (int): Number of trips for BY_TRIPS tickets (ignored for time-based tickets).
            tendered_money (Money): The amount of money provided by the passenger.

        Returns:
            Tuple[Ticket, Money]: A tuple containing the purchased ticket and any change due.
        """

        ticket, change = office.sell_ticket(ticket_type, trips, tendered_money)
        passenger.buy_ticket(ticket)
        
        return ticket, change