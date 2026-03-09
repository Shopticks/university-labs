import uuid
from decimal import Decimal
from typing import Dict, Tuple
from datetime import datetime, timedelta

from src.domain.models.money import Money
from src.domain.models.ticket import Ticket, TicketType
from src.exceptions import InsufficientFundsError, InvalidTicketRequestError

class TicketOffice:
    """
    TicketOffice class responsible for selling tickets and managing transactions.
    Maintains a catalog of available ticket types and their prices, handles
    payment processing, and generates tickets for customers.
    """
    def __init__(self, office_id: str):
        """
        Initialize a TicketOffice instance.

        Args:
            office_id (str): Unique identifier for the ticket office.
        """
        self._id = office_id
        self._balance = Money(Decimal('0.00'))
        
        self._catalog: Dict[Tuple[TicketType, int], Money] = {
            (TicketType.BY_TRIPS, 1): Money(Decimal('0.90')),
            (TicketType.BY_TRIPS, 5): Money(Decimal('4.30')),
            (TicketType.BY_TRIPS, 10): Money(Decimal('8.10')),
            (TicketType.DAILY, 0): Money(Decimal('4.00')),
            (TicketType.WEEKLY, 0): Money(Decimal('10.00')),
            (TicketType.MONTHLY, 0): Money(Decimal('38.00')),
        }

    @property
    def id(self) -> str:
        """
        Retrieve the ticket office's unique identifier.

        Returns:
            str: The ticket office's ID.
        """
        return self._id

    @property
    def balance(self) -> Money:
        """
        Get the current balance of the ticket office.

        Returns:
            Money: The current monetary balance of the office.
        """
        return self._balance

    def get_price(self, ticket_type: TicketType, trips: int = 0) -> Money:
        """
        Get the price for a specific ticket type and trip count.

        Args:
            ticket_type (TicketType):  The type of ticket to check
            trips (int, optional): Number of trips for BY_TRIPS tickets. Defaults to 0.

        Raises:
            InvalidTicketRequestError: If the ticket type and trip combination is not available.

        Returns:
            Money: The price of the requested ticket.
        """
        key = (ticket_type, trips)
        if key not in self._catalog:
            raise InvalidTicketRequestError(f"Ticket {ticket_type.value} with {trips} trips is not available")
        return self._catalog[key]

    def sell_ticket(self, ticket_type: TicketType, trips: int, tendered_money: Money) -> Tuple[Ticket, Money]:
        """
        Sell a ticket to a customer after validating payment.

        Args:
            ticket_type (TicketType): The type of ticket to purchase.
            trips (int): Number of trips for BY_TRIPS tickets (ignored for time-based tickets).
            tendered_money (Money): The amount of money provided by the customer.

        Raises:
            InsufficientFundsError: If the tendered money is less than the ticket price

        Returns:
            Tuple[Ticket, Money]: A tuple containing the purchased ticket and any change due.
        """
        price = self.get_price(ticket_type, trips)

        if not (tendered_money >= price):
            raise InsufficientFundsError(
                f"Not enough money. Price is {price}, but {tendered_money} was tendered"
            )

        change = tendered_money - price
        self._balance += price

        # TODO: Generator for the uuid

        new_ticket_id = f"TKT-{uuid.uuid4().hex[:6].upper()}"
        
        expires_at = None
        now = datetime.now()
        if ticket_type == TicketType.DAILY:
            expires_at = now + timedelta(days=1)
        elif ticket_type == TicketType.WEEKLY:
            expires_at = now + timedelta(days=7)
        elif ticket_type == TicketType.MONTHLY:
            expires_at = now + timedelta(days=30)
        
        new_ticket = Ticket(
            ticket_id=new_ticket_id,
            ticket_type=ticket_type,
            max_trips=trips,
            expires_at=expires_at
        )

        return new_ticket, change