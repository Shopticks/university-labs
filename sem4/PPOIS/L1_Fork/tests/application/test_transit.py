import pytest
from datetime import datetime, timedelta
from src.domain.models.ticket import Ticket, TicketType
from src.domain.models.turnstile import Turnstile, TurnstileState
from src.application.transit import TransitService
from src.exceptions import (
    TurnstileLockedDownError,
    TurnstileAlreadyUnlockedError,
    TicketExpiredError,
    TicketExhaustedError,
)


@pytest.fixture
def valid_trips_ticket():
    return Ticket("T1", TicketType.BY_TRIPS, max_trips=5)


@pytest.fixture
def valid_daily_ticket():
    future = datetime.now() + timedelta(days=1)
    return Ticket("T2", TicketType.DAILY, expires_at=future)


@pytest.fixture
def unlocked_turnstile():
    t = Turnstile("TUR-1")
    return t


class TestProcessTurnstilePassage:
    def test_trips_ticket_is_consumed_on_passage(self, valid_trips_ticket, unlocked_turnstile):
        TransitService.process_turnstile_passage(valid_trips_ticket, unlocked_turnstile)
        assert valid_trips_ticket.remaining_trips == 4

    def test_turnstile_locks_after_passage(self, valid_trips_ticket, unlocked_turnstile):
        TransitService.process_turnstile_passage(valid_trips_ticket, unlocked_turnstile)
        assert unlocked_turnstile.state == TurnstileState.LOCKED

    def test_time_based_ticket_is_not_exhausted_after_passage(self, valid_daily_ticket, unlocked_turnstile):
        TransitService.process_turnstile_passage(valid_daily_ticket, unlocked_turnstile)
        assert valid_daily_ticket.is_valid is True

    def test_lockdown_blocks_passage(self, valid_trips_ticket):
        t = Turnstile("TUR-2")
        t.lockdown()
        with pytest.raises(TurnstileLockedDownError):
            TransitService.process_turnstile_passage(valid_trips_ticket, t)

    def test_already_unlocked_turnstile_raises(self, valid_trips_ticket):
        """
        A turnstile that is already UNLOCKED at the start of the call means
        a previous passage was not completed — this must be rejected to
        preserve the invariant that every passage consumes exactly one trip.
        """
        t = Turnstile("TUR-3")
        t.unlock()
        with pytest.raises(TurnstileAlreadyUnlockedError):
            TransitService.process_turnstile_passage(valid_trips_ticket, t)

    def test_expired_ticket_raises(self):
        past = datetime.now() - timedelta(days=1)
        expired = Ticket("T3", TicketType.DAILY, expires_at=past)
        t = Turnstile("TUR-4")
        with pytest.raises(TicketExpiredError):
            TransitService.process_turnstile_passage(expired, t)

    def test_exhausted_ticket_raises(self):
        exhausted = Ticket("T4", TicketType.BY_TRIPS, max_trips=1)
        exhausted.use()
        t = Turnstile("TUR-5")
        with pytest.raises(TicketExhaustedError):
            TransitService.process_turnstile_passage(exhausted, t)

    def test_trips_not_decremented_if_passage_fails(self, valid_trips_ticket):
        """Ticket must NOT be consumed when the turnstile is in lockdown."""
        t = Turnstile("TUR-6")
        t.lockdown()
        with pytest.raises(TurnstileLockedDownError):
            TransitService.process_turnstile_passage(valid_trips_ticket, t)
        assert valid_trips_ticket.remaining_trips == 5