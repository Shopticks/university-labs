from datetime import date
from decimal import Decimal
from typing import List, Dict

from src.pharma_distributor.utils.converters import CurrencyConverter
from src.pharma_distributor.catalog.services import CatalogService
from src.pharma_distributor.common.enums import Currency
from src.pharma_distributor.inventory.models import Warehouse
from src.pharma_distributor.reporting.models import (
    FinancialSummary,
    InventoryReport,
    InventoryLineItem,
    BatchReportItem,
    SalesPerformanceItem
)
from src.pharma_distributor.sales.models import Order, OrderStatus
from src.pharma_distributor.exceptions import ReporterError


class ReportGenerator:
    """
    Domain service responsible for aggregating data from various modules (Sales, Inventory, Catalog)
    to produce analytical reports.
    """

    def __init__(self, catalog_service: CatalogService, currency_converter: CurrencyConverter = None):
        """
        Args:
            catalog_service: Service to retrieve product details (names, prices).
            currency_converter: Service to normalize monetary values to a reporting currency.
        """
        self.catalog_service = catalog_service
        self.currency_converter = currency_converter or CurrencyConverter()

    def generate_financial_report(
            self,
            orders: List[Order],
            start: date,
            end: date,
            target_currency: Currency = Currency.BYN
    ) -> FinancialSummary:
        """
        Calculates total revenue and order statistics for a given period.
        Only considers completed orders (PAID, SHIPPED, DELIVERED).
        """
        relevant_orders = [
            o for o in orders
            if start <= o.created_at.date() <= end
               and o.status in (OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED)
        ]

        total_revenue = Decimal("0.00")
        count = len(relevant_orders)

        for order in relevant_orders:
            order_total = order.calculate_total()

            try:
                converted_amount = self.currency_converter.convert(
                    order_total.amount,
                    order_total.currency,
                    target_currency
                )
                total_revenue += converted_amount
            except Exception:
                continue

        avg_value = (total_revenue / count) if count > 0 else Decimal("0.00")

        return FinancialSummary(
            period_start=start,
            period_end=end,
            total_revenue=total_revenue,
            total_orders_count=count,
            average_order_value=avg_value,
            currency=target_currency
        )

    def generate_warehouse_report(self, warehouse: Warehouse) -> InventoryReport:
        """
        Generates a detailed inventory report for a specific warehouse.
        Includes valuation of stock (converted to base currency) and batch status checks (expiry).
        """
        report_lines = []
        total_value_accumulator = Decimal("0.00")
        report_currency = Currency.BYN

        for product_id, batches in warehouse.stock_view.items():

            try:
                product = self.catalog_service.get_product_by_id(product_id)
            except Exception as e:
                raise ReporterError(e)

            product_total_qty = 0
            product_total_value = Decimal("0.00")
            batch_items = []

            for batch in batches:
                if batch.quantity <= 0:
                    continue

                days_left = (batch.expiry_date - date.today()).days
                status = "OK"
                if batch.is_quarantined:
                    status = "QUARANTINED"
                elif days_left < 0:
                    status = "EXPIRED"
                elif days_left < 30:
                    status = "EXPIRING_SOON"

                batch_items.append(BatchReportItem(
                    batch_number=batch.batch_number,
                    expiry_date=batch.expiry_date,
                    quantity=batch.quantity,
                    days_until_expiry=days_left,
                    status=status
                ))

                product_total_qty += batch.quantity

                batch_value = product.price.amount * batch.quantity
                product_total_value += batch_value

            if product_total_qty > 0:
                try:
                    converted_val = self.currency_converter.convert(
                        product_total_value,
                        product.price.currency,
                        report_currency
                    )
                    total_value_accumulator += converted_val
                except Exception as e:
                    raise ReporterError(e)

                report_lines.append(InventoryLineItem(
                    product_id=product.id,
                    product_name=product.name,
                    sku=f"SKU-{product.id}",
                    total_quantity=product_total_qty,
                    total_value=product_total_value,
                    currency=product.price.currency,
                    batches=batch_items
                ))

        return InventoryReport(
            warehouse_name=warehouse.name,
            warehouse_id=warehouse.id,
            total_items_count=sum(line.total_quantity for line in report_lines),
            total_stock_value=total_value_accumulator,
            currency=report_currency,
            lines=report_lines
        )

    def generate_sales_performance(self, orders: List[Order]) -> List[SalesPerformanceItem]:
        """
        Analyzes sales data to rank products by performance.
        """
        product_stats: Dict[str, Dict] = {}

        for order in orders:
            if order.status == OrderStatus.CANCELLED:
                continue

            for item in order.items:
                p_name = item.product.name
                if p_name not in product_stats:
                    product_stats[p_name] = {"qty": 0, "revenue": Decimal("0.00")}

                product_stats[p_name]["qty"] += item.quantity
                product_stats[p_name]["revenue"] += item.total().amount

        results = []
        for name, stats in product_stats.items():
            results.append(SalesPerformanceItem(
                product_name=name,
                units_sold=stats["qty"],
                revenue_generated=stats["revenue"]
            ))

        results.sort(key=lambda x: x.revenue_generated, reverse=True)
        return results