from datetime import date, timedelta, datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest

from pharma_distributor.catalog.models import BaseProduct
from pharma_distributor.catalog.services import CatalogService
from pharma_distributor.common.enums import Currency
from pharma_distributor.exceptions import ReporterError
from pharma_distributor.finance.models import Money
from pharma_distributor.inventory.models import Warehouse, StockBatch
from pharma_distributor.reporting.services import ReportGenerator
from pharma_distributor.sales.models import Order, OrderStatus
from pharma_distributor.utils.converters import CurrencyConverter


@pytest.fixture
def mock_catalog():
    return Mock(spec=CatalogService)


@pytest.fixture
def mock_converter():
    converter = Mock(spec=CurrencyConverter)
    converter.convert.side_effect = lambda amount, f, t: amount
    return converter


@pytest.fixture
def generator(mock_catalog, mock_converter):
    return ReportGenerator(mock_catalog, mock_converter)


@pytest.fixture
def sample_orders():
    o1 = Mock(spec=Order)
    o1.status = OrderStatus.PAID
    o1.created_at = datetime(2023, 1, 15)
    o1.calculate_total.return_value = Money(Decimal("100.00"), Currency.BYN)

    o2 = Mock(spec=Order)
    o2.status = OrderStatus.SHIPPED
    o2.created_at = datetime(2023, 1, 20)
    o2.calculate_total.return_value = Money(Decimal("200.00"), Currency.BYN)

    o3 = Mock(spec=Order)
    o3.status = OrderStatus.NEW
    o3.created_at = datetime(2023, 1, 10)
    o3.calculate_total.return_value = Money(Decimal("500.00"), Currency.BYN)

    o4 = Mock(spec=Order)
    o4.status = OrderStatus.PAID
    o4.created_at = datetime(2022, 12, 31)
    o4.calculate_total.return_value = Money(Decimal("100.00"), Currency.BYN)

    return [o1, o2, o3, o4]



def test_financial_report_aggregation(generator, sample_orders):
    start = date(2023, 1, 1)
    end = date(2023, 1, 31)

    report = generator.generate_financial_report(sample_orders, start, end, Currency.BYN)

    assert report.total_revenue == Decimal("300.00")
    assert report.total_orders_count == 2
    assert report.average_order_value == Decimal("150.00")  # 300 / 2


def test_financial_report_currency_conversion(generator, mock_converter):
    o1 = Mock(spec=Order)
    o1.status = OrderStatus.PAID
    o1.created_at = datetime(2023, 1, 15)
    o1.calculate_total.return_value = Money(Decimal("100.00"), Currency.USD)

    mock_converter.convert.side_effect = None
    mock_converter.convert.return_value = Decimal("320.00")

    report = generator.generate_financial_report([o1], date(2023, 1, 1), date(2023, 1, 31), Currency.BYN)

    assert report.total_revenue == Decimal("320.00")
    mock_converter.convert.assert_called_with(Decimal("100.00"), Currency.USD, Currency.BYN)


def test_financial_report_empty(generator):
    report = generator.generate_financial_report([], date(2023, 1, 1), date(2023, 1, 1))
    assert report.total_revenue == Decimal("0.00")
    assert report.average_order_value == Decimal("0.00")



def test_warehouse_report_generation(generator, mock_catalog, mock_converter):
    warehouse = Mock(spec=Warehouse)
    warehouse.name = "Test WH"
    warehouse.id = 1

    b1 = Mock(spec=StockBatch)
    b1.quantity = 10
    b1.expiry_date = date.today() + timedelta(days=100)
    b1.is_quarantined = False
    b1.batch_number = "B1"

    b2 = Mock(spec=StockBatch)
    b2.quantity = 5
    b2.expiry_date = date.today() - timedelta(days=1)
    b2.is_quarantined = False
    b2.batch_number = "B2"

    warehouse.stock_view = {
        101: [b1, b2]
    }

    product = Mock(spec=BaseProduct)
    product.id = 101
    product.name = "Pills"
    product.price = Money(Decimal("10.00"), Currency.USD)
    mock_catalog.get_product_by_id.return_value = product

    mock_converter.convert.side_effect = None
    mock_converter.convert.return_value = Decimal("300.00")

    report = generator.generate_warehouse_report(warehouse)

    assert report.warehouse_name == "Test WH"
    assert report.total_items_count == 15
    assert report.total_stock_value == Decimal("300.00")

    assert len(report.lines) == 1
    line = report.lines[0]
    assert line.product_name == "Pills"
    assert len(line.batches) == 2

    statuses = {b.batch_number: b.status for b in line.batches}
    assert statuses["B1"] == "OK"
    assert statuses["B2"] == "EXPIRED"


def test_warehouse_report_missing_product(generator, mock_catalog):
    warehouse = Mock(spec=Warehouse)
    warehouse.stock_view = {999: []}

    mock_catalog.get_product_by_id.side_effect = Exception("DB Error")

    with pytest.raises(ReporterError):
        generator.generate_warehouse_report(warehouse)



def test_sales_performance_ranking(generator):
    item_a = Mock()
    item_a.product.name = "Prod A"
    item_a.quantity = 2
    item_a.total.return_value = Money(Decimal("20.00"), Currency.USD)

    item_b = Mock()
    item_b.product.name = "Prod B"
    item_b.quantity = 1
    item_b.total.return_value = Money(Decimal("100.00"), Currency.USD)

    o1 = Mock(spec=Order)
    o1.status = OrderStatus.PAID
    o1.items = [item_a, item_b]

    o2 = Mock(spec=Order)
    o2.status = OrderStatus.CANCELLED
    o2.items = [item_b]

    results = generator.generate_sales_performance([o1, o2])

    assert len(results) == 2
    assert results[0].product_name == "Prod B"
    assert results[0].revenue_generated == Decimal("100.00")

    assert results[1].product_name == "Prod A"
    assert results[1].revenue_generated == Decimal("20.00")