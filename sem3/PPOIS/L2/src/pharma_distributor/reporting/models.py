from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import List

from pharma_distributor.common.enums import Currency


@dataclass(frozen=True)
class FinancialSummary:
    """
    Data Transfer Object (DTO) capturing a snapshot of financial performance
    over a specific period.
    """
    period_start: date
    period_end: date
    total_revenue: Decimal
    total_orders_count: int
    average_order_value: Decimal
    currency: Currency
    generated_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class BatchReportItem:
    """
    Detailed status of a specific batch within an inventory report.
    Includes calculated status (e.g., 'EXPIRED', 'OK').
    """
    batch_number: str
    expiry_date: date
    quantity: int
    days_until_expiry: int
    status: str


@dataclass(frozen=True)
class InventoryLineItem:
    """
    Represents the aggregated stock for a single product in a warehouse report.
    Contains total quantity, total value, and a breakdown of individual batches.
    """
    product_id: int
    product_name: str
    sku: str
    total_quantity: int
    total_value: Decimal
    currency: Currency
    batches: List[BatchReportItem]


@dataclass(frozen=True)
class InventoryReport:
    """
    Comprehensive report of a warehouse's inventory status.
    Aggregates value and quantity across all stored products.
    """
    warehouse_name: str
    warehouse_id: int
    total_items_count: int
    total_stock_value: Decimal
    currency: Currency
    generated_at: datetime = field(default_factory=datetime.now)
    lines: List[InventoryLineItem] = field(default_factory=list)


@dataclass(frozen=True)
class SalesPerformanceItem:
    """
    DTO representing the sales performance of a single product.
    Used for ranking products by revenue or volume.
    """
    product_name: str
    units_sold: int
    revenue_generated: Decimal