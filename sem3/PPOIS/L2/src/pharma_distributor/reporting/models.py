from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from src.pharma_distributor.common.enums import Currency


@dataclass(frozen=True)
class FinancialSummary:
    period_start: date
    period_end: date
    total_revenue: Decimal
    total_orders_count: int
    average_order_value: Decimal
    currency: Currency
    generated_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class BatchReportItem:
    batch_number: str
    expiry_date: date
    quantity: int
    days_until_expiry: int
    status: str


@dataclass(frozen=True)
class InventoryLineItem:
    product_id: int
    product_name: str
    sku: str
    total_quantity: int
    total_value: Decimal
    currency: Currency
    batches: List[BatchReportItem]


@dataclass(frozen=True)
class InventoryReport:
    warehouse_name: str
    warehouse_id: int
    total_items_count: int
    total_stock_value: Decimal
    currency: Currency
    generated_at: datetime = field(default_factory=datetime.now)
    lines: List[InventoryLineItem] = field(default_factory=list)


@dataclass(frozen=True)
class SalesPerformanceItem:
    product_name: str
    units_sold: int
    revenue_generated: Decimal