from typing import List, Tuple

from src.pharma_distributor.catalog.models import BaseProduct
from src.pharma_distributor.exceptions import SalesError, OutOfStockError
from src.pharma_distributor.inventory.models import Warehouse
from src.pharma_distributor.inventory.services import InventoryManager
from src.pharma_distributor.sales.models import Order, Customer, OrderStatus
from src.pharma_distributor.utils.generators import IDGenerator


class SalesService:
    def __init__(self, inventory_manager: InventoryManager):
        self.inventory_manager = inventory_manager

    def create_order(self, customer: Customer, items: List[Tuple[BaseProduct, int]]) -> Order:
        order = Order(
            id=IDGenerator.generate_uuid(),
            customer=customer
        )

        for product, qty in items:
            order.add_item(product, qty)

        return order

    def process_order(self, order: Order, warehouse: Warehouse) -> None:
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
        previous_status = order.status

        if previous_status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise SalesError("Cannot cancel shipped or delivered order via simple cancellation")

        order.cancel()

        if previous_status == OrderStatus.PAID and order.warehouse_id:
            for item in order.items:
                pass