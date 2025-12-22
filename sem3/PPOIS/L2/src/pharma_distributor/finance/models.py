from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Union

from src.pharma_distributor.common.enums import Currency
from src.pharma_distributor.exceptions import FinanceError, InsufficientFundsError, CurrencyMismatchError


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: Currency

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, 'amount', Decimal(str(self.amount)))

        quantized = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        object.__setattr__(self, 'amount', quantized)

        if self.amount < 0:
            raise FinanceError(f"Money amount cannot be negative: {self.amount}")

    def _check_currency(self, other: 'Money'):
        if self.currency != other.currency:
            raise CurrencyMismatchError(f"Currency mismatch: {self.currency} vs {other.currency}")

    def __add__(self, other: 'Money') -> 'Money':
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        self._check_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, other: Union[int, float, Decimal]) -> 'Money':
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
    iban: str
    bank_name: str
    balance: Money
    is_active: bool = True

    def _activity_check(self) -> None:
        if not self.is_active:
            raise FinanceError(f"Account {self.iban} is inactive")

    def deposit(self, amount: Money) -> None:
        self._activity_check()

        self.balance = self.balance + amount

    def withdraw(self, amount: Money) -> None:
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
    id: str
    source_account_id: str
    target_account_id: str
    amount: Money
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    description: str = ""