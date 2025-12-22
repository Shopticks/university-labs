import pytest
from unittest.mock import Mock
from decimal import Decimal

from pharma_distributor.finance.services import FinanceService
from pharma_distributor.finance.models import BankAccount, Money
from pharma_distributor.common.enums import Currency
from pharma_distributor.exceptions import FinanceError, InsufficientFundsError


@pytest.fixture
def mock_converter():
    return Mock()


@pytest.fixture
def finance_service(mock_converter):
    return FinanceService(converter=mock_converter)


@pytest.fixture
def source_acc():
    return BankAccount(
        iban="SRC001",
        bank_name="Source Bank",
        balance=Money(Decimal("1000.00"), Currency.USD)
    )


@pytest.fixture
def target_acc_same_currency():
    return BankAccount(
        iban="TGT001",
        bank_name="Target Bank",
        balance=Money(Decimal("0.00"), Currency.USD)
    )


@pytest.fixture
def target_acc_diff_currency():
    return BankAccount(
        iban="TGT002",
        bank_name="Target BYN",
        balance=Money(Decimal("0.00"), Currency.BYN)
    )



def test_transfer_funds_same_currency(finance_service, source_acc, target_acc_same_currency):
    amount = Money(Decimal("100.00"), Currency.USD)

    tx = finance_service.transfer_funds(source_acc, target_acc_same_currency, amount)

    assert source_acc.balance.amount == Decimal("900.00")
    assert target_acc_same_currency.balance.amount == Decimal("100.00")
    assert tx.amount == amount
    assert tx.source_account_id == source_acc.iban

    finance_service.converter.convert.assert_not_called()


def test_transfer_funds_with_conversion(finance_service, source_acc, target_acc_diff_currency):
    amount_usd = Money(Decimal("100.00"), Currency.USD)

    finance_service.converter.convert.return_value = Decimal("320.00")

    tx = finance_service.transfer_funds(source_acc, target_acc_diff_currency, amount_usd)

    assert source_acc.balance.amount == Decimal("900.00")
    assert target_acc_diff_currency.balance.amount == Decimal("320.00")
    assert target_acc_diff_currency.balance.currency == Currency.BYN

    finance_service.converter.convert.assert_called_once_with(
        Decimal("100.00"), Currency.USD, Currency.BYN
    )


def test_transfer_insufficient_funds(finance_service, source_acc, target_acc_same_currency):
    too_much = Money(Decimal("5000.00"), Currency.USD)

    with pytest.raises(InsufficientFundsError):
        finance_service.transfer_funds(source_acc, target_acc_same_currency, too_much)

    assert source_acc.balance.amount == Decimal("1000.00")
    assert target_acc_same_currency.balance.amount == Decimal("0.00")


def test_transfer_rollback_on_deposit_fail(finance_service, source_acc, target_acc_same_currency):
    amount = Money(Decimal("100.00"), Currency.USD)

    original_deposit = target_acc_same_currency.deposit
    target_acc_same_currency.deposit = Mock(side_effect=Exception("Database Error"))

    with pytest.raises(FinanceError, match="Transfer failed during deposit"):
        finance_service.transfer_funds(source_acc, target_acc_same_currency, amount)

    assert source_acc.balance.amount == Decimal("1000.00")

    assert target_acc_same_currency.balance.amount == Decimal("0.00")