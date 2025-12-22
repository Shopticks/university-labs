import pytest
from unittest.mock import Mock, ANY
from decimal import Decimal

from pharma_distributor.sales.services import SalesService
from pharma_distributor.sales.models import Order, Customer, OrderStatus
from pharma_distributor.inventory.services import InventoryManager
from pharma_distributor.inventory.models import Warehouse
from pharma_distributor.catalog.models import Medicine
from pharma_distributor.finance.models import Money
from pharma_distributor.common.enums import Currency
from pharma_distributor.exceptions import SalesError, OutOfStockError



@pytest.fixture
def mock_inventory():
    return Mock(spec=InventoryManager)


@pytest.fixture
def service(mock_inventory):
    return SalesService(inventory_manager=mock_inventory)


@pytest.fixture
def customer():
    return Mock(spec=Customer)


@pytest.fixture
def product():
    p = Mock(spec=Medicine)
    p.id = 101
    p.name = "Test Med"
    p.price = Money(Decimal("10.00"), Currency.USD)
    p.is_active = True
    return p


@pytest.fixture
def warehouse():
    w = Mock(spec=Warehouse)
    w.id = 55
    return w



def test_create_order(service, customer, product):
    items = [(product, 5)]
    order = service.create_order(customer, items)

    assert isinstance(order, Order)
    assert order.customer == customer
    assert len(order.items) == 1
    assert order.items[0].quantity == 5
    assert order.status == OrderStatus.NEW


def test_process_order_success(service, mock_inventory, customer, product, warehouse):
    order = service.create_order(customer, [(product, 10)])

    mock_inventory.get_stock_level.return_value = 20

    service.process_order(order, warehouse)

    assert order.status == OrderStatus.PAID
    assert order.warehouse_id == warehouse.id

    mock_inventory.reserve_stock.assert_called_once_with(warehouse, product.id, 10)


def test_process_order_out_of_stock(service, mock_inventory, customer, product, warehouse):
    order = service.create_order(customer, [(product, 10)])

    mock_inventory.get_stock_level.return_value = 5

    with pytest.raises(OutOfStockError, match="Requested 10, Available 5"):
        service.process_order(order, warehouse)

    assert order.status == OrderStatus.NEW
    mock_inventory.reserve_stock.assert_not_called()


def test_process_order_already_processed(service, mock_inventory, customer, product, warehouse):
    order = service.create_order(customer, [(product, 1)])
    order.status = OrderStatus.PAID

    with pytest.raises(SalesError, match="already processed"):
        service.process_order(order, warehouse)


def test_cancel_order_new(service, mock_inventory, customer, product, warehouse):
    order = service.create_order(customer, [(product, 1)])

    service.cancel_order(order, warehouse)

    assert order.status == OrderStatus.CANCELLED
    mock_inventory.receive_shipment.assert_not_called()


def test_cancel_order_paid_restocking(service, mock_inventory, customer, product, warehouse):
    order = service.create_order(customer, [(product, 5)])
    order.status = OrderStatus.PAID
    order.warehouse_id = warehouse.id
    order.id = "ORD-123"

    service.cancel_order(order, warehouse)

    assert order.status == OrderStatus.CANCELLED

    mock_inventory.receive_shipment.assert_called_once_with(
        warehouse=warehouse,
        product=product,
        quantity=5,
        batch_number="RET-123",
        expiry_date=ANY,
        min_shelf_life_days=30
    )


def test_cancel_order_shipped_fail(service, mock_inventory, customer, product, warehouse):
    order = service.create_order(customer, [(product, 1)])
    order.status = OrderStatus.SHIPPED

    with pytest.raises(SalesError, match="Cannot cancel shipped"):
        service.cancel_order(order, warehouse)