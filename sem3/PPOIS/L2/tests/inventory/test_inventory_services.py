from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import Mock

import pytest

from pharma_distributor.catalog.models import Medicine, ProductSpecification
from pharma_distributor.common.enums import VolumeUnit, Currency
from pharma_distributor.common.models import Volume
from pharma_distributor.exceptions import ValidationError
from pharma_distributor.finance.models import Money
from pharma_distributor.inventory.models import Warehouse, StockBatch
from pharma_distributor.inventory.services import InventoryManager


@pytest.fixture
def manager():
    return InventoryManager()


@pytest.fixture
def mock_warehouse():
    wh = Mock(spec=Warehouse)
    wh.stock_view = {}
    return wh


@pytest.fixture
def valid_medicine():
    specs = ProductSpecification("M", "C", "S", Volume(Decimal("1"), VolumeUnit.LITER))
    return Medicine(
        id=1, name="Med", price=Money(Decimal("10"), Currency.USD),
        category=Mock(), specs=specs, dosage="D", active_substance="A",
        is_prescription_required=False,
        expiry_date=date.today() + timedelta(days=365),
        is_active=True
    )



def test_receive_shipment_success(manager, mock_warehouse, valid_medicine):
    expiry = date.today() + timedelta(days=200)

    manager.receive_shipment(
        warehouse=mock_warehouse,
        product=valid_medicine,
        quantity=100,
        batch_number="B1",
        expiry_date=expiry
    )

    mock_warehouse.add_stock.assert_called_once_with(valid_medicine, 100, "B1", expiry)


def test_receive_shipment_inactive_product(manager, mock_warehouse, valid_medicine):
    valid_medicine.is_active = False

    with pytest.raises(ValidationError, match="inactive product"):
        manager.receive_shipment(mock_warehouse, valid_medicine, 10, "B1", date.today())


def test_receive_shipment_medicine_no_expiry(manager, mock_warehouse, valid_medicine):
    with pytest.raises(ValidationError, match="Expiry date is mandatory"):
        manager.receive_shipment(mock_warehouse, valid_medicine, 10, "B1", expiry_date=None)


def test_receive_shipment_expired(manager, mock_warehouse, valid_medicine):
    past_date = date.today() - timedelta(days=1)

    with pytest.raises(ValidationError, match="Cannot accept expired"):
        manager.receive_shipment(mock_warehouse, valid_medicine, 10, "B1", expiry_date=past_date)


def test_receive_shipment_short_shelf_life(manager, mock_warehouse, valid_medicine):
    short_expiry = date.today() + timedelta(days=100)

    with pytest.raises(ValidationError, match="Remaining shelf life"):
        manager.receive_shipment(
            mock_warehouse, valid_medicine, 10, "B1",
            expiry_date=short_expiry,
            min_shelf_life_days=180
        )


def test_check_expiring_goods(manager, mock_warehouse):
    today = date.today()

    batch_ok = Mock(spec=StockBatch, quantity=10, expiry_date=today + timedelta(days=100))
    batch_expiring = Mock(spec=StockBatch, quantity=10, expiry_date=today + timedelta(days=10))
    batch_empty = Mock(spec=StockBatch, quantity=0, expiry_date=today + timedelta(days=5))

    mock_warehouse.stock_view = {
        1: [batch_ok, batch_expiring, batch_empty]
    }

    result = manager.check_expiring_goods(mock_warehouse, threshold_days=30)

    assert len(result) == 1
    assert result[0] == batch_expiring


def test_manager_delegation(manager, mock_warehouse):
    manager.reserve_stock(mock_warehouse, 1, 10)
    mock_warehouse.reserve_stock.assert_called_once_with(1, 10)

    manager.get_stock_level(mock_warehouse, 1)
    mock_warehouse.get_total_quantity.assert_called_once_with(1)

    manager.set_batch_quarantine_status(mock_warehouse, 1, "B1", True)
    mock_warehouse.set_batch_quarantine_status.assert_called_once_with(1, "B1", True)