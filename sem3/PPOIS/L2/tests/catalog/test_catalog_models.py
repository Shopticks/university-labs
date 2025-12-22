import pytest
from datetime import date, timedelta
from decimal import Decimal

from pharma_distributor.catalog.models import (
    Category,
    Medicine,
    MedicalDevice,
    ProductSpecification
)
from pharma_distributor.common.enums import Currency, WarrantyStatus, VolumeUnit
from pharma_distributor.common.models import Volume
from pharma_distributor.finance.models import Money
from pharma_distributor.exceptions import ValidationError



@pytest.fixture
def sample_category():
    return Category(id=1, name="General", description="General items")


@pytest.fixture
def sample_specs():
    return ProductSpecification(
        manufacturer="Acme Corp",
        country_of_origin="USA",
        storage_conditions="Cool dry place",
        packaging_volume=Volume(Decimal("0.1"), VolumeUnit.CUBIC_METER)
    )


@pytest.fixture
def sample_price():
    return Money(Decimal("100.00"), Currency.USD)


@pytest.fixture
def medicine(sample_category, sample_specs, sample_price):
    return Medicine(
        id=1,
        name="PainKiller",
        price=sample_price,
        category=sample_category,
        specs=sample_specs,
        dosage="500mg",
        active_substance="Paracetamol",
        is_prescription_required=False,
        expiry_date=date.today() + timedelta(days=365)
    )


@pytest.fixture
def device(sample_category, sample_specs, sample_price):
    return MedicalDevice(
        id=2,
        name="X-Ray Machine",
        price=sample_price,
        category=sample_category,
        specs=sample_specs,
        warranty_months=12,
        serial_number="SN-12345",
        service_interval_months=6,
        purchase_date=date.today() - timedelta(days=30)
    )



def test_category_is_root():
    root_cat = Category(id=1, name="Root", description="Top")
    child_cat = Category(id=2, name="Child", description="Sub", parent_id=1)

    assert root_cat.is_root() is True
    assert child_cat.is_root() is False


def test_category_update_details():
    cat = Category(id=1, name="Old", description="Old desc")
    cat.update_details("New", "New desc")

    assert cat.name == "New"
    assert cat.description == "New desc"


def test_category_update_empty_name():
    cat = Category(id=1, name="Old", description="Old desc")
    with pytest.raises(ValidationError):
        cat.update_details("", "Desc")



def test_apply_discount(medicine):
    medicine.apply_discount(20.0)
    assert medicine.price.amount == Decimal("80.00")


def test_apply_discount_invalid(medicine):
    with pytest.raises(ValidationError):
        medicine.apply_discount(110.0)

    with pytest.raises(ValidationError):
        medicine.apply_discount(-5.0)


def test_archive_restore(medicine):
    assert medicine.is_active is True
    medicine.archive()
    assert medicine.is_active is False
    medicine.restore()
    assert medicine.is_active is True



def test_medicine_expiration(medicine):
    assert medicine.is_expired() is False
    assert medicine.days_until_expiry() > 0

    medicine.expiry_date = date.today() - timedelta(days=1)
    assert medicine.is_expired() is True
    assert medicine.days_until_expiry() < 0


def test_medicine_display_info(medicine):
    info = medicine.get_display_info()
    assert "PainKiller" in info
    assert "500mg" in info



def test_device_warranty_status_valid(device):
    assert device.warranty_status() == WarrantyStatus.VALID_WARRANTY


def test_device_warranty_status_expired(device):
    device.purchase_date = date.today() - timedelta(days=400)
    assert device.warranty_status() == WarrantyStatus.WARRANTY_EXPIRED


def test_device_warranty_not_purchased(device):
    device.purchase_date = None
    assert device.warranty_status() == WarrantyStatus.NOT_PURCHASED


def test_device_maintenance_needed(device):
    device.last_service_date = None
    assert device.needs_maintenance() is True

    device.last_service_date = date.today() - timedelta(days=1)
    assert device.needs_maintenance() is False

    device.last_service_date = date.today() - timedelta(days=210)
    assert device.needs_maintenance() is True


def test_device_perform_maintenance(device):
    device.last_service_date = date.today() - timedelta(days=200)
    device.perform_maintenance()
    assert device.last_service_date == date.today()