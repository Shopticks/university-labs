from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Union

from pharma_distributor.common.enums import Currency
from pharma_distributor.exceptions import FinanceError, InsufficientFundsError, CurrencyMismatchError


@dataclass(frozen=True)
class Money:
    """
    Value Object representing a monetary amount associated with a specific currency.
    Supports arithmetic operations while ensuring currency safety.
    """
    amount: Decimal
    currency: Currency

    def __post_init__(self):
        """
        Validates the amount and ensures it is rounded to 2 decimal places.
        """
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, 'amount', Decimal(str(self.amount)))

        quantized = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        object.__setattr__(self, 'amount', quantized)

        if self.amount < 0:
            raise FinanceError(f"Money amount cannot be negative: {self.amount}")

    def _check_currency(self, other: 'Money'):
        """
        Helper to validate that both Money objects share the same currency.

        Raises:
            CurrencyMismatchError: If currencies differ.
        """
        if self.currency != other.currency:
            raise CurrencyMismatchError(f"Currency mismatch: {self.currency} vs {other.currency}")

    def __add__(self, other: 'Money') -> 'Money':
        """
        Adds two Money objects of the same currency.
        """
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        """
        Subtracts one Money object from another. Must be same currency.
        """
        self._check_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, other: Union[int, float, Decimal]) -> 'Money':
        """
        Multiplies the monetary amount by a scalar value.
        """
        if isinstance(other, Money):
            raise FinanceError("Cannot multiply Money by Money")

        multiplier = Decimal(str(other)) if not isinstance(other, Decimal) else other
        return Money(self.amount * multiplier, self.currency)

    def __lt__(self, other: 'Money') -> bool:
        self._check_currency(other)
        return self.amount < other.amount

    def __le__(self, other: 'Money') -> bool:
        self._check_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other: 'Money') -> bool:
        self._check_currency(other)
        return self.amount > other.amount

    def __ge__(self, other: 'Money') -> bool:
        self._check_currency(other)
        return self.amount >= other.amount


@dataclass
class BankAccount:
    """
    Represents a bank account holding a balance in a specific currency.
    Acts as an Entity that mutates state via deposit and withdrawal.
    """
    iban: str
    bank_name: str
    balance: Money
    is_active: bool = True

    def _activity_check(self) -> None:
        """
        Ensures the account is active before performing operations.
        """
        if not self.is_active:
            raise FinanceError(f"Account {self.iban} is inactive")

    def deposit(self, amount: Money) -> None:
        """
        Adds funds to the account.

        Args:
            amount: The Money to add. Must match account currency.
        """
        self._activity_check()

        self.balance = self.balance + amount

    def withdraw(self, amount: Money) -> None:
        """
        Removes funds from the account.

        Args:
            amount: The Money to remove. Must match account currency.

        Raises:
            FinanceError: If the withdrawal amount is not positive.
            InsufficientFundsError: If the balance is lower than the requested amount.
        """
        self._activity_check()

        if amount.amount <= 0:
            raise FinanceError("Withdrawal amount must be positive")

        if amount > self.balance:
            raise InsufficientFundsError(
                f"Insufficient funds in {self.iban}. "
                f"Required: {amount.amount}, Available: {self.balance.amount}"
            )

        self.balance = self.balance - amount


@dataclass
class Transaction:
    """
    Represents an immutable record of a financial transfer.
    """
    id: str
    source_account_id: str
    target_account_id: str
    amount: Money
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    description: str = ""