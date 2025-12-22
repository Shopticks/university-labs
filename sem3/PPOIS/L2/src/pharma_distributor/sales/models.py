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
    """
    Represents a registered buyer in the system.
    Contains billing and shipping details required for order processing.
    """
    id: int
    name: str
    billing_address: Address
    shipping_address: Address
    contact: ContactInfo


@dataclass
class OrderItem:
    """
    Represents a specific line item within an order, linking a product
    to a requested quantity and price snapshot.
    """
    product: BaseProduct
    quantity: int
    unit_price: Money

    def __post_init__(self):
        """
        Validates that the ordered quantity is positive.
        """
        if self.quantity <= 0:
            raise ValidationError(f"Quantity must be positive, got {self.quantity}")

    def total(self) -> Money:
        """
        Calculates the total cost for this line item.

        Returns:
            Money: unit_price * quantity.
        """
        return self.unit_price * self.quantity


@dataclass
class Order:
    """
    Aggregate Root representing a sales transaction.
    Manages the lifecycle of the order (creation, payment, shipping)
    and ensures consistency of items (currency, availability).
    """
    id: str
    customer: Customer
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.NEW
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    warehouse_id: Optional[int] = None

    def calculate_total(self) -> Money:
        """
        Calculates the grand total of the order by summing all line items.

        Returns:
            Money: The sum of all items. Returns 0 BYN if order is empty.
        """
        if not self.items:
            return Money(Decimal("0"), Currency.BYN)

        total = self.items[0].total()
        for item in self.items[1:]:
            total += item.total()

        return total

    def add_item(self, product: BaseProduct, quantity: int) -> None:
        """
        Adds a product to the order.
        - Merges with existing item if product already exists in order.
        - Validates that product is active.
        - Ensures all items in the order use the same currency.

        Args:
            product: The product to add.
            quantity: The number of units.

        Raises:
            InvalidOrderStatusError: If order is not in NEW status.
            ValidationError: If product is inactive.
            CurrencyMismatchError: If product currency differs from existing items.
        """
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
        """
        Locks the order to a specific warehouse and transitions status to PAID.
        Usually called after stock reservation is successful.

        Args:
            warehouse_id: The ID of the fulfilling warehouse.

        Raises:
            InvalidOrderStatusError: If order is not NEW.
            ValidationError: If order is empty.
        """
        if self.status != OrderStatus.NEW:
            raise InvalidOrderStatusError(f"Cannot confirm order in status {self.status}")

        if not self.items:
            raise ValidationError("Cannot confirm empty order")

        self.status = OrderStatus.PAID
        self.warehouse_id = warehouse_id
        self.updated_at = datetime.now()

    def mark_as_paid(self) -> None:
        """
        Manually marks the order as PAID.
        Idempotent if already paid.

        Raises:
            InvalidOrderStatusError: If order is not NEW or PAID.
        """
        if self.status == OrderStatus.PAID:
            return

        if self.status != OrderStatus.NEW:
            raise InvalidOrderStatusError("Only NEW orders can be paid")

        self.status = OrderStatus.PAID
        self.updated_at = datetime.now()

    def ship(self) -> None:
        """
        Transitions order to SHIPPED status.
        Requires order to be PAID.
        """
        if self.status != OrderStatus.PAID:
            raise InvalidOrderStatusError("Cannot ship unpaid order")

        self.status = OrderStatus.SHIPPED
        self.updated_at = datetime.now()

    def deliver(self) -> None:
        """
        Transitions order to DELIVERED status.
        Requires order to be SHIPPED.
        """
        if self.status != OrderStatus.SHIPPED:
            raise InvalidOrderStatusError("Cannot deliver order that hasn't been shipped")

        self.status = OrderStatus.DELIVERED
        self.updated_at = datetime.now()

    def cancel(self, reason: str = "") -> None:
        """
        Cancels the order.
        Cannot cancel orders that have already left the warehouse.

        Args:
            reason: Optional reason for cancellation.
        """
        if self.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise InvalidOrderStatusError("Cannot cancel shipped or delivered order")

        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.now()