import pytest
from datetime import datetime, timedelta
from src.domain.models.ticket import Ticket, TicketType
from src.exceptions import TicketExhaustedError, TicketExpiredError


@pytest.fixture
def trips_ticket():
    return Ticket("T1", TicketType.BY_TRIPS, max_trips=3)


@pytest.fixture
def daily_ticket():
    future = datetime.now() + timedelta(days=1)
    return Ticket("T2", TicketType.DAILY, expires_at=future)


class TestByTripsTicket:
    def test_initial_state(self, trips_ticket):
        assert trips_ticket.is_valid is True
        assert trips_ticket.remaining_trips == 3
        assert trips_ticket.current_trips == 0

    def test_use_decrements_remaining(self, trips_ticket):
        trips_ticket.use()
        assert trips_ticket.remaining_trips == 2
        assert trips_ticket.current_trips == 1

    def test_exhausted_after_max_uses(self, trips_ticket):
        for _ in range(3):
            trips_ticket.use()
        assert trips_ticket.is_valid is False

    def test_use_after_exhausted_raises(self, trips_ticket):
        for _ in range(3):
            trips_ticket.use()
        with pytest.raises(TicketExhaustedError):
            trips_ticket.use()

    def test_remaining_trips_is_not_inf(self, trips_ticket):
        assert trips_ticket.remaining_trips != float("inf")


class TestTimeBasedTicket:
    def test_valid_ticket_is_valid(self, daily_ticket):
        assert daily_ticket.is_valid is True

    def test_expired_ticket_is_not_valid(self):
        past = datetime.now() - timedelta(seconds=1)
        ticket = Ticket("T3", TicketType.DAILY, expires_at=past)
        assert ticket.is_valid is False

    def test_use_expired_ticket_raises(self):
        past = datetime.now() - timedelta(days=1)
        ticket = Ticket("T3", TicketType.DAILY, expires_at=past)
        with pytest.raises(TicketExpiredError):
            ticket.use()

    def test_remaining_trips_is_inf_for_time_based(self, daily_ticket):
        assert daily_ticket.remaining_trips == float("inf")

    def test_use_does_not_decrement_time_based(self, daily_ticket):
        daily_ticket.use()
        assert daily_ticket.remaining_trips == float("inf")

    def test_weekly_ticket(self):
        future = datetime.now() + timedelta(days=7)
        ticket = Ticket("T4", TicketType.WEEKLY, expires_at=future)
        assert ticket.is_valid is True
        ticket.use()
        assert ticket.is_valid is True

    def test_monthly_ticket(self):
        future = datetime.now() + timedelta(days=30)
        ticket = Ticket("T5", TicketType.MONTHLY, expires_at=future)
        assert ticket.is_valid is True