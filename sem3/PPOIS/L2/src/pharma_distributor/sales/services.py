from typing import List, Tuple
from datetime import date, timedelta

from src.pharma_distributor.catalog.models import BaseProduct
from src.pharma_distributor.exceptions import SalesError, OutOfStockError
from src.pharma_distributor.inventory.models import Warehouse
from src.pharma_distributor.inventory.services import InventoryManager
from src.pharma_distributor.sales.models import Order, Customer, OrderStatus
from src.pharma_distributor.utils.generators import IDGenerator


class SalesService:
    """
    Domain service handling the lifecycle of sales orders.
    Coordinates between the Order entity and Inventory management.
    """

    def __init__(self, inventory_manager: InventoryManager):
        """
        Args:
            inventory_manager: Service to handle stock checks and reservations.
        """
        self.inventory_manager = inventory_manager

    def create_order(self, customer: Customer, items: List[Tuple[BaseProduct, int]]) -> Order:
        """
        Initializes a new order for a customer.
        """
        order = Order(
            id=IDGenerator.generate_uuid(),
            customer=customer
        )

        for product, qty in items:
            order.add_item(product, qty)

        return order

    def process_order(self, order: Order, warehouse: Warehouse) -> None:
        """
        Validates stock, reserves items in inventory, and confirms the order.
        """
        if order.status != OrderStatus.NEW:
            raise SalesError(f"Order {order.id} is already processed")

        for item in order.items:
            available = self.inventory_manager.get_stock_level(warehouse, item.product.id)
            if available < item.quantity:
                raise OutOfStockError(
                    f"Product {item.product.name}: Requested {item.quantity}, Available {available}"
                )

        try:
            for item in order.items:
                self.inventory_manager.reserve_stock(
                    warehouse, item.product.id, item.quantity
                )
        except Exception as e:
            raise SalesError(f"Failed to reserve stock: {str(e)}")

        order.confirm(warehouse.id)
        order.mark_as_paid()

    def cancel_order(self, order: Order, warehouse: Warehouse) -> None:
        """
        Cancels an order and attempts to release reserved stock.

        Raises:
            SalesError: If can not receive shipment
        """
        previous_status = order.status

        if previous_status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise SalesError("Cannot cancel shipped or delivered order via simple cancellation")

        order.cancel()

        if previous_status == OrderStatus.PAID and order.warehouse_id:
            restock_date = date.today()
            safe_expiry = restock_date + timedelta(days=365)

            batch_suffix = order.id.split('-')[-1] if '-' in order.id else 'RET'

            for item in order.items:
                try:
                    self.inventory_manager.receive_shipment(
                        warehouse=warehouse,
                        product=item.product,
                        quantity=item.quantity,
                        batch_number=f"RET-{batch_suffix}",
                        expiry_date=safe_expiry,
                        min_shelf_life_days=30
                    )
                except Exception as e:
                    raise SalesError(e)