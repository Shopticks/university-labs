import pytest
from unittest.mock import Mock
from datetime import date, timedelta
from decimal import Decimal

from pharma_distributor.catalog.services import CatalogService
from pharma_distributor.catalog.models import Medicine, MedicalDevice, Category
from pharma_distributor.finance.models import Money
from pharma_distributor.common.enums import Currency
from pharma_distributor.exceptions import ValidationError



@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def service(mock_repo):
    return CatalogService(product_repository=mock_repo)


@pytest.fixture
def category_a():
    return Category(id=1, name="Cat A", description="A")


@pytest.fixture
def category_b():
    return Category(id=2, name="Cat B", description="B")


@pytest.fixture
def medicine_expiring_soon(category_a):
    return Medicine(
        id=1, name="Med A", price=Money(Decimal("10"), Currency.USD),
        category=category_a, specs=Mock(), dosage="10mg", active_substance="X",
        is_prescription_required=False,
        expiry_date=date.today() + timedelta(days=10)
    )


@pytest.fixture
def medicine_safe(category_a):
    return Medicine(
        id=2, name="Med B", price=Money(Decimal("20"), Currency.USD),
        category=category_a, specs=Mock(), dosage="20mg", active_substance="Y",
        is_prescription_required=False,
        expiry_date=date.today() + timedelta(days=100)
    )


@pytest.fixture
def device_item(category_b):
    return MedicalDevice(
        id=3, name="Dev C", price=Money(Decimal("500"), Currency.USD),
        category=category_b, specs=Mock(), warranty_months=12, serial_number="123",
        service_interval_months=6
    )



def test_get_product_by_id_success(service, mock_repo, medicine_safe):
    mock_repo.get.return_value = medicine_safe

    result = service.get_product_by_id(2)

    assert result == medicine_safe
    mock_repo.get.assert_called_once_with(2)


def test_get_product_by_id_not_found(service, mock_repo):
    mock_repo.get.return_value = None

    with pytest.raises(ValidationError, match="not found"):
        service.get_product_by_id(999)


def test_register_product(service, mock_repo, medicine_safe):
    service.register_product(medicine_safe)
    mock_repo.save.assert_called_once_with(medicine_safe)


def test_update_price(service, mock_repo, medicine_safe):
    mock_repo.get.return_value = medicine_safe
    new_price = Money(Decimal("25.00"), Currency.USD)

    service.update_price(2, new_price)

    assert medicine_safe.price == new_price
    mock_repo.save.assert_called_once_with(medicine_safe)


def test_get_expiring_medicines(service, mock_repo, medicine_expiring_soon, medicine_safe, device_item):
    mock_repo.list_all.return_value = [medicine_expiring_soon, medicine_safe, device_item]

    result = service.get_expiring_medicines(days_threshold=30)

    assert len(result) == 1
    assert result[0].id == 1


def test_apply_category_discount(service, mock_repo, category_a, category_b, medicine_safe, device_item):
    mock_repo.list_all.return_value = [medicine_safe, device_item]

    count = service.apply_category_discount(category_a, 50.0)

    assert count == 1
    assert medicine_safe.price.amount == Decimal("10.00")
    assert device_item.price.amount == Decimal("500.00")

    mock_repo.save.assert_any_call(medicine_safe)


def test_schedule_maintenance(service, mock_repo, device_item):
    device_item.last_service_date = None

    service.schedule_maintenance(device_item)

    assert device_item.last_service_date == date.today()
    mock_repo.save.assert_called_once_with(device_item)