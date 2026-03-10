import pytest
from decimal import Decimal
from src.domain.models.passenger import Passenger
from src.domain.models.ticket_office import TicketOffice
from src.domain.models.money import Money
from src.domain.models.ticket import TicketType
from src.application.sales import SalesService
from src.exceptions import InsufficientFundsError

def test_successful_sale():
    passenger = Passenger("P1", "Ivan")
    office = TicketOffice("O1")
    tendered = Money(Decimal('10.00'))
    
    ticket, change = SalesService.process_ticket_purchase(
        passenger, office, TicketType.DAILY, 0, tendered
    )
    
    assert ticket.ticket_type == TicketType.DAILY
    assert change.amount == Decimal('6.00')
    assert passenger.ticket == ticket
    assert office.balance.amount == Decimal('4.00')

def test_failed_sale_low_money():
    passenger = Passenger("P1", "Ivan")
    office = TicketOffice("O1")
    tendered = Money(Decimal('1.00'))
    
    with pytest.raises(InsufficientFundsError):
        SalesService.process_ticket_purchase(
            passenger, office, TicketType.DAILY, 0, tendered
        )