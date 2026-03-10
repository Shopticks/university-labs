import pytest
from decimal import Decimal
from src.domain.models.money import Money

def test_money_initialization():
    m = Money(Decimal('10.50'))
    assert m.amount == Decimal('10.50')

def test_money_addition():
    m1 = Money(Decimal('10.00'))
    m2 = Money(Decimal('5.50'))
    result = m1 + m2
    assert result.amount == Decimal('15.50')

def test_money_subtraction_success():
    m1 = Money(Decimal('10.00'))
    m2 = Money(Decimal('5.50'))
    result = m1 - m2
    assert result.amount == Decimal('4.50')

def test_money_subtraction_failure_negative():
    m1 = Money(Decimal('5.00'))
    m2 = Money(Decimal('10.00'))
    with pytest.raises(ValueError, match="Resulting money cannot be negative"):
        m1 - m2

def test_money_greater_or_equal():
    assert Money(Decimal('10.00')) >= Money(Decimal('5.00'))
    assert Money(Decimal('10.00')) >= Money(Decimal('10.00'))
    assert not (Money(Decimal('5.00')) >= Money(Decimal('10.00')))

def test_money_string_representation():
    m = Money(Decimal('10.50'))
    assert str(m) == "10.50 BYN"