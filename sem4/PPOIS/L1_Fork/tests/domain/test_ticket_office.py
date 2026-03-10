import pytest
from decimal import Decimal
from src.domain.models.ticket_office import TicketOffice
from src.domain.models.money import Money
from src.domain.models.ticket import TicketType
from src.exceptions import InsufficientFundsError, InvalidTicketRequestError


@pytest.fixture
def office():
    return TicketOffice("O1")


class TestTicketOfficeGetPrice:
    def test_known_ticket_types_return_price(self, office):
        assert office.get_price(TicketType.DAILY).amount == Decimal("4.00")
        assert office.get_price(TicketType.WEEKLY).amount == Decimal("10.00")
        assert office.get_price(TicketType.MONTHLY).amount == Decimal("38.00")

    def test_by_trips_prices(self, office):
        assert office.get_price(TicketType.BY_TRIPS, trips=1).amount == Decimal("0.90")
        assert office.get_price(TicketType.BY_TRIPS, trips=5).amount == Decimal("4.30")
        assert office.get_price(TicketType.BY_TRIPS, trips=10).amount == Decimal("8.10")

    def test_unknown_trips_count_raises(self, office):
        with pytest.raises(InvalidTicketRequestError):
            office.get_price(TicketType.BY_TRIPS, trips=7)

    def test_unknown_ticket_type_trips_combination_raises(self, office):
        # DAILY with a non-zero trips value is not in the catalog
        with pytest.raises(InvalidTicketRequestError):
            office.get_price(TicketType.DAILY, trips=5)


class TestTicketOfficeSell:
    def test_exact_money_no_change(self, office):
        tendered = Money(Decimal("4.00"))
        ticket, change = office.sell_ticket(TicketType.DAILY, 0, tendered)
        assert ticket.ticket_type == TicketType.DAILY
        assert change.amount == Decimal("0.00")
        assert office.balance.amount == Decimal("4.00")

    def test_overpayment_returns_change(self, office):
        tendered = Money(Decimal("10.00"))
        ticket, change = office.sell_ticket(TicketType.DAILY, 0, tendered)
        assert change.amount == Decimal("6.00")

    def test_insufficient_funds_raises(self, office):
        tendered = Money(Decimal("1.00"))
        with pytest.raises(InsufficientFundsError):
            office.sell_ticket(TicketType.DAILY, 0, tendered)

    def test_balance_accumulates_across_sales(self, office):
        office.sell_ticket(TicketType.DAILY, 0, Money(Decimal("4.00")))
        office.sell_ticket(TicketType.DAILY, 0, Money(Decimal("4.00")))
        assert office.balance.amount == Decimal("8.00")

    def test_sold_trips_ticket_has_correct_max_trips(self, office):
        tendered = Money(Decimal("5.00"))
        ticket, _ = office.sell_ticket(TicketType.BY_TRIPS, 5, tendered)
        assert ticket.max_trips == 5

    def test_sold_daily_ticket_has_expiry(self, office):
        tendered = Money(Decimal("4.00"))
        ticket, _ = office.sell_ticket(TicketType.DAILY, 0, tendered)
        assert ticket.expires_at is not None
        assert ticket.is_valid is True