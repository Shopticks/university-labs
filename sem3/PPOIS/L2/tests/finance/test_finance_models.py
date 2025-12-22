import pytest
from decimal import Decimal
from pharma_distributor.finance.models import Money, BankAccount
from pharma_distributor.common.enums import Currency
from pharma_distributor.exceptions import (
    FinanceError,
    InsufficientFundsError,
    CurrencyMismatchError
)


@pytest.fixture
def money_usd_100():
    return Money(Decimal("100.00"), Currency.USD)


@pytest.fixture
def money_usd_50():
    return Money(Decimal("50.00"), Currency.USD)


@pytest.fixture
def money_byn_100():
    return Money(Decimal("100.00"), Currency.BYN)


@pytest.fixture
def account_active(money_usd_100):
    return BankAccount(
        iban="US123",
        bank_name="Test Bank",
        balance=money_usd_100,
        is_active=True
    )



def test_money_initialization_rounding():
    m = Money(Decimal("10.555"), Currency.USD)
    assert m.amount == Decimal("10.56")

    m2 = Money(Decimal("10.554"), Currency.USD)
    assert m2.amount == Decimal("10.55")


def test_money_negative_amount():
    with pytest.raises(FinanceError, match="cannot be negative"):
        Money(Decimal("-10.00"), Currency.USD)


def test_money_addition(money_usd_100, money_usd_50):
    result = money_usd_100 + money_usd_50
    assert result.amount == Decimal("150.00")
    assert result.currency == Currency.USD


def test_money_subtraction(money_usd_100, money_usd_50):
    result = money_usd_100 - money_usd_50
    assert result.amount == Decimal("50.00")


def test_money_multiplication(money_usd_100):
    result = money_usd_100 * 2
    assert result.amount == Decimal("200.00")

    result_decimal = money_usd_100 * Decimal("0.5")
    assert result_decimal.amount == Decimal("50.00")


def test_money_currency_mismatch(money_usd_100, money_byn_100):
    with pytest.raises(CurrencyMismatchError):
        _ = money_usd_100 + money_byn_100

    with pytest.raises(CurrencyMismatchError):
        _ = money_usd_100 - money_byn_100

    with pytest.raises(CurrencyMismatchError):
        assert money_usd_100 > money_byn_100


def test_money_comparison(money_usd_100, money_usd_50):
    assert money_usd_100 > money_usd_50
    assert money_usd_50 < money_usd_100
    assert money_usd_100 != money_usd_50
    assert money_usd_100 == Money(Decimal("100.00"), Currency.USD)



def test_account_deposit(account_active):
    deposit_amount = Money(Decimal("50.00"), Currency.USD)
    account_active.deposit(deposit_amount)
    assert account_active.balance.amount == Decimal("150.00")


def test_account_withdraw_success(account_active):
    withdraw_amount = Money(Decimal("40.00"), Currency.USD)
    account_active.withdraw(withdraw_amount)
    assert account_active.balance.amount == Decimal("60.00")


def test_account_withdraw_insufficient_funds(account_active):
    withdraw_amount = Money(Decimal("150.00"), Currency.USD)
    with pytest.raises(InsufficientFundsError):
        account_active.withdraw(withdraw_amount)


def test_account_withdraw_negative_amount(account_active):
    zero_money = Money(Decimal("0.00"), Currency.USD)
    with pytest.raises(FinanceError, match="Withdrawal amount must be positive"):
        account_active.withdraw(zero_money)


def test_account_inactive_operations(account_active):
    account_active.is_active = False
    amount = Money(Decimal("10.00"), Currency.USD)

    with pytest.raises(FinanceError, match="is inactive"):
        account_active.deposit(amount)

    with pytest.raises(FinanceError, match="is inactive"):
        account_active.withdraw(amount)