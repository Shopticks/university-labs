import pytest
from src.domain.models.turnstile import Turnstile, TurnstileState
from src.exceptions import (
    TurnstileLockedError,
    TurnstileAlreadyUnlockedError,
    TurnstileLockedDownError,
)


@pytest.fixture
def turnstile():
    return Turnstile("TUR-1")


class TestTurnstileInitialState:
    def test_initial_state_is_locked(self, turnstile):
        assert turnstile.state == TurnstileState.LOCKED

    def test_id_is_set(self, turnstile):
        assert turnstile.id == "TUR-1"


class TestTurnstileUnlock:
    def test_unlock_from_locked(self, turnstile):
        turnstile.unlock()
        assert turnstile.state == TurnstileState.UNLOCKED

    def test_unlock_already_unlocked_raises(self, turnstile):
        turnstile.unlock()
        with pytest.raises(TurnstileAlreadyUnlockedError):
            turnstile.unlock()

    def test_unlock_during_lockdown_raises(self, turnstile):
        turnstile.lockdown()
        with pytest.raises(TurnstileLockedDownError):
            turnstile.unlock()


class TestTurnstileLock:
    def test_lock_after_unlock(self, turnstile):
        turnstile.unlock()
        turnstile.lock()
        assert turnstile.state == TurnstileState.LOCKED

    def test_lock_during_lockdown_raises(self, turnstile):
        turnstile.lockdown()
        with pytest.raises(TurnstileLockedDownError):
            turnstile.lock()


class TestTurnstilePassThrough:
    def test_pass_through_when_unlocked(self, turnstile):
        turnstile.unlock()
        turnstile.pass_through()
        assert turnstile.state == TurnstileState.LOCKED

    def test_pass_through_when_locked_raises(self, turnstile):
        with pytest.raises(TurnstileLockedError):
            turnstile.pass_through()

    def test_pass_through_during_lockdown_raises(self, turnstile):
        turnstile.lockdown()
        with pytest.raises(TurnstileLockedDownError):
            turnstile.pass_through()


class TestTurnstileLockdown:
    def test_lockdown_sets_state(self, turnstile):
        turnstile.lockdown()
        assert turnstile.state == TurnstileState.LOCKED_DOWN

    def test_remove_lockdown_restores_locked(self, turnstile):
        turnstile.lockdown()
        turnstile.remove_lockdown()
        assert turnstile.state == TurnstileState.LOCKED

    def test_lockdown_on_unlocked_turnstile(self, turnstile):
        """Lockdown should override any current state."""
        turnstile.unlock()
        turnstile.lockdown()
        assert turnstile.state == TurnstileState.LOCKED_DOWN