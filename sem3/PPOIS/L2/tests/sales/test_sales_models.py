from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest

from pharma_distributor.catalog.models import Medicine, ProductSpecification
from pharma_distributor.common.enums import OrderStatus, Currency, VolumeUnit
from pharma_distributor.common.models import Address, ContactInfo, Volume
from pharma_distributor.exceptions import (
    ValidationError,
    InvalidOrderStatusError,
    CurrencyMismatchError
)
from pharma_distributor.finance.models import Money
from pharma_distributor.sales.models import Order, OrderItem, Customer


@pytest.fixture
def customer():
    addr = Address("BY", "Minsk", "St", "000")
    contact = ContactInfo("c@test.com", "+1234567890")
    return Customer(id=1, name="Client", billing_address=addr, shipping_address=addr, contact=contact)


@pytest.fixture
def product_usd():
    specs = ProductSpecification("M", "C", "S", Volume(Decimal("1"), VolumeUnit.LITER))
    return Medicine(
        id=1, name="Med USD", price=Money(Decimal("10.00"), Currency.USD),
        category=Mock(), specs=specs, dosage="D", active_substance="A",
        is_prescription_required=False, expiry_date=datetime.now(),
        is_active=True
    )


@pytest.fixture
def product_byn():
    specs = ProductSpecification("M", "C", "S", Volume(Decimal("1"), VolumeUnit.LITER))
    return Medicine(
        id=2, name="Med BYN", price=Money(Decimal("25.00"), Currency.BYN),
        category=Mock(), specs=specs, dosage="D", active_substance="A",
        is_prescription_required=False, expiry_date=datetime.now(),
        is_active=True
    )


@pytest.fixture
def order(customer):
    return Order(id="ORD-1", customer=customer)



def test_order_item_total(product_usd):
    item = OrderItem(product=product_usd, quantity=5, unit_price=product_usd.price)
    # 5 * 10.00 = 50.00
    assert item.total() == Money(Decimal("50.00"), Currency.USD)


def test_order_item_negative_qty(product_usd):
    with pytest.raises(ValidationError, match="Quantity must be positive"):
        OrderItem(product=product_usd, quantity=0, unit_price=product_usd.price)



def test_add_item_new(order, product_usd):
    order.add_item(product_usd, 2)
    assert len(order.items) == 1
    assert order.items[0].quantity == 2
    assert order.calculate_total() == Money(Decimal("20.00"), Currency.USD)


def test_add_item_merge(order, product_usd):
    order.add_item(product_usd, 2)
    order.add_item(product_usd, 3)

    assert len(order.items) == 1
    assert order.items[0].quantity == 5


def test_add_item_currency_mismatch(order, product_usd, product_byn):
    order.add_item(product_usd, 1)

    with pytest.raises(CurrencyMismatchError):
        order.add_item(product_byn, 1)


def test_add_item_inactive_product(order, product_usd):
    product_usd.is_active = False
    with pytest.raises(ValidationError, match="inactive"):
        order.add_item(product_usd, 1)


def test_add_item_wrong_status(order, product_usd):
    order.status = OrderStatus.PAID
    with pytest.raises(InvalidOrderStatusError):
        order.add_item(product_usd, 1)



def test_confirm_order(order, product_usd):
    order.add_item(product_usd, 1)
    order.confirm(warehouse_id=99)

    assert order.status == OrderStatus.PAID
    assert order.warehouse_id == 99


def test_confirm_empty_order(order):
    with pytest.raises(ValidationError, match="empty order"):
        order.confirm(warehouse_id=1)


def test_ship_order(order, product_usd):
    order.add_item(product_usd, 1)
    order.confirm(1)

    order.ship()
    assert order.status == OrderStatus.SHIPPED


def test_ship_unpaid_order(order):
    with pytest.raises(InvalidOrderStatusError):
        order.ship()


def test_deliver_order(order, product_usd):
    order.add_item(product_usd, 1)
    order.confirm(1)
    order.ship()

    order.deliver()
    assert order.status == OrderStatus.DELIVERED


def test_cancel_shipped_order(order, product_usd):
    order.add_item(product_usd, 1)
    order.confirm(1)
    order.ship()

    with pytest.raises(InvalidOrderStatusError, match="Cannot cancel shipped"):
        order.cancel()