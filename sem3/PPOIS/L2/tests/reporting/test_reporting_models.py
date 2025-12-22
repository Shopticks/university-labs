from datetime import date, datetime
from decimal import Decimal

from pharma_distributor.common.enums import Currency
from pharma_distributor.reporting.models import (
    FinancialSummary,
    BatchReportItem,
    SalesPerformanceItem
)


def test_financial_summary_creation():
    summary = FinancialSummary(
        period_start=date(2023, 1, 1),
        period_end=date(2023, 1, 31),
        total_revenue=Decimal("1000.00"),
        total_orders_count=10,
        average_order_value=Decimal("100.00"),
        currency=Currency.BYN
    )

    assert summary.total_revenue == Decimal("1000.00")
    assert isinstance(summary.generated_at, datetime)


def test_batch_report_item_status():
    item = BatchReportItem(
        batch_number="B1",
        expiry_date=date(2025, 1, 1),
        quantity=50,
        days_until_expiry=100,
        status="OK"
    )
    assert item.status == "OK"
    assert item.quantity == 50


def test_sales_performance_sorting_helper():
    item = SalesPerformanceItem("Prod A", 10, Decimal("100.00"))
    assert item.product_name == "Prod A"
    assert item.revenue_generated == Decimal("100.00")