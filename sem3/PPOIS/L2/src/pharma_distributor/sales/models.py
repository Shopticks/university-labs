from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from src.pharma_distributor.catalog.models import BaseProduct
from src.pharma_distributor.common.enums import OrderStatus, Currency
from src.pharma_distributor.common.models import Address, ContactInfo
from src.pharma_distributor.exceptions import (
    InvalidOrderStatusError,
    ValidationError,
    CurrencyMismatchError
)
from src.pharma_distributor.finance.models import Money


@dataclass
class Customer:
    id: int
    name: str
    billing_address: Address
    shipping_address: Address
    contact: ContactInfo


@dataclass
class OrderItem:
    product: BaseProduct
    quantity: int
    unit_price: Money

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValidationError(f"Quantity must be positive, got {self.quantity}")

    def total(self) -> Money:
        return self.unit_price * self.quantity


@dataclass
class Order:
    id: str
    customer: Customer
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.NEW
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    warehouse_id: Optional[int] = None

    def calculate_total(self) -> Money:
        if not self.items:
            return Money(Decimal("0"), Currency.BYN)

        total = self.items[0].total()
        for item in self.items[1:]:
            total += item.total()

        return total

    def add_item(self, product: BaseProduct, quantity: int) -> None:
        if self.status != OrderStatus.NEW:
            raise InvalidOrderStatusError("Cannot add items to a confirmed or processed order")

        if not product.is_active:
            raise ValidationError(f"Product {product.name} is archived/inactive")

        if self.items:
            current_currency = self.items[0].unit_price.currency
            if product.price.currency != current_currency:
                raise CurrencyMismatchError(
                    f"Cannot mix currencies in one order. "
                    f"Order is {current_currency}, product is {product.price.currency}"
                )

        existing_item = next((i for i in self.items if i.product.id == product.id), None)
        if existing_item:
            existing_item.quantity += quantity
        else:
            self.items.append(OrderItem(
                product=product,
                quantity=quantity,
                unit_price=product.price
            ))

        self.updated_at = datetime.now()

    def confirm(self, warehouse_id: int) -> None:
        if self.status != OrderStatus.NEW:
            raise InvalidOrderStatusError(f"Cannot confirm order in status {self.status}")

        if not self.items:
            raise ValidationError("Cannot confirm empty order")

        self.status = OrderStatus.PAID
        self.warehouse_id = warehouse_id
        self.updated_at = datetime.now()

    def mark_as_paid(self) -> None:
        if self.status == OrderStatus.PAID:
            return

        if self.status != OrderStatus.NEW:
            raise InvalidOrderStatusError("Only NEW orders can be paid")

        self.status = OrderStatus.PAID
        self.updated_at = datetime.now()

    def ship(self) -> None:
        if self.status != OrderStatus.PAID:
            raise InvalidOrderStatusError("Cannot ship unpaid order")

        self.status = OrderStatus.SHIPPED
        self.updated_at = datetime.now()

    def deliver(self) -> None:
        if self.status != OrderStatus.SHIPPED:
            raise InvalidOrderStatusError("Cannot deliver order that hasn't been shipped")

        self.status = OrderStatus.DELIVERED
        self.updated_at = datetime.now()

    def cancel(self, reason: str = "") -> None:
        if self.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise InvalidOrderStatusError("Cannot cancel shipped or delivered order")

        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.now()