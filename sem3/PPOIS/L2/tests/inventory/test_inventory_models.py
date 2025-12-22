from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from pharma_distributor.catalog.models import Medicine, ProductSpecification, Category
from pharma_distributor.common.enums import VolumeUnit, Currency
from pharma_distributor.common.models import Address, Volume
from pharma_distributor.exceptions import (
    OutOfStockError,
    WarehouseFullError
)
from pharma_distributor.finance.models import Money
from pharma_distributor.inventory.models import StockBatch, Warehouse



@pytest.fixture
def unit_volume():
    return Volume(Decimal("0.1"), VolumeUnit.CUBIC_METER)


@pytest.fixture
def product_specs(unit_volume):
    return ProductSpecification(
        manufacturer="Test Pharma",
        country_of_origin="DE",
        storage_conditions="Dry",
        packaging_volume=unit_volume
    )


@pytest.fixture
def product(product_specs):
    return Medicine(
        id=1,
        name="Aspirin",
        price=Money(Decimal("10.00"), Currency.USD),
        category=Category(id=1, name="Meds", description=""),
        specs=product_specs,
        dosage="100mg",
        active_substance="Acid",
        is_prescription_required=False,
        expiry_date=date.today() + timedelta(days=365)
    )


@pytest.fixture
def batch(product, unit_volume):
    return StockBatch(
        id=str(uuid4()),
        product_id=product.id,
        batch_number="BATCH-001",
        quantity=10,
        expiry_date=date.today() + timedelta(days=100),
        unit_volume=unit_volume
    )


@pytest.fixture
def warehouse():
    addr = Address("Country", "City", "Street", "00000")
    capacity = Volume(Decimal("100.0"), VolumeUnit.CUBIC_METER)
    return Warehouse(id=1, name="Main Warehouse", address=addr, capacity=capacity)



def test_batch_volume_calculation(batch):
    assert batch.total_volume_m3 == Decimal("1.0")


def test_batch_decrease(batch):
    freed_vol = batch.decrease(3)

    assert batch.quantity == 7
    assert freed_vol == Decimal("0.3")


def test_batch_decrease_out_of_stock(batch):
    with pytest.raises(OutOfStockError):
        batch.decrease(11)


def test_batch_increase(batch):
    added_vol = batch.increase(5)

    assert batch.quantity == 15
    assert added_vol == Decimal("0.5")


def test_batch_is_expired(batch):
    assert batch.is_expired() is False

    batch.expiry_date = date.today() - timedelta(days=1)
    assert batch.is_expired() is True



def test_warehouse_add_stock_success(warehouse, product):
    warehouse.add_stock(product, 10, "B1", date.today())

    assert warehouse.current_load.amount == Decimal("1.0")
    assert warehouse.get_total_quantity(product.id) == 10
    assert len(warehouse.stock_view[product.id]) == 1


def test_warehouse_add_stock_merge_batches(warehouse, product):
    expiry = date.today()
    warehouse.add_stock(product, 10, "B1", expiry)
    warehouse.add_stock(product, 5, "B1", expiry)

    assert warehouse.get_total_quantity(product.id) == 15
    assert len(warehouse.stock_view[product.id]) == 1

def test_warehouse_full_error(warehouse, product):
    with pytest.raises(WarehouseFullError):
        warehouse.add_stock(product, 1001, "B1", date.today())


def test_warehouse_reserve_stock_simple(warehouse, product):
    warehouse.add_stock(product, 10, "B1", date.today())

    warehouse.reserve_stock(product.id, 4)

    assert warehouse.get_total_quantity(product.id) == 6
    assert warehouse.current_load.amount == Decimal("0.6")


def test_warehouse_reserve_stock_multiple_batches(warehouse, product):
    warehouse.add_stock(product, 10, "B_SOON", date.today() + timedelta(days=1))
    warehouse.add_stock(product, 10, "B_LATER", date.today() + timedelta(days=365))

    warehouse.reserve_stock(product.id, 15)

    assert warehouse.get_total_quantity(product.id) == 5

    batches = warehouse.stock_view[product.id]
    assert len(batches) == 1
    assert batches[0].batch_number == "B_LATER"
    assert batches[0].quantity == 5


def test_warehouse_reserve_skips_quarantine(warehouse, product):
    warehouse.add_stock(product, 10, "B1", date.today())
    warehouse.set_batch_quarantine_status(product.id, "B1", True)

    assert warehouse.get_total_quantity(product.id) == 0

    with pytest.raises(OutOfStockError):
        warehouse.reserve_stock(product.id, 1)


def test_warehouse_write_off(warehouse, product):
    warehouse.add_stock(product, 10, "B1", date.today())

    warehouse.write_off_stock(product.id, "B1", 3, "Damaged")

    assert warehouse.get_total_quantity(product.id) == 7
    assert warehouse.current_load.amount == Decimal("0.7")