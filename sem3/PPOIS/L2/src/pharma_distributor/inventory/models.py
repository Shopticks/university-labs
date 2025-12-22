from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional
from uuid import uuid4

from pharma_distributor.common.models import Address, Volume
from pharma_distributor.common.enums import VolumeUnit
from pharma_distributor.catalog.models import BaseProduct
from pharma_distributor.exceptions import (
    InventoryError,
    WarehouseFullError,
    OutOfStockError
)


@dataclass
class StockBatch:
    """
    Represents a specific batch of a product stored in the warehouse.
    Tracks quantity, expiration date, and quarantine status.
    """
    id: str
    product_id: int
    batch_number: str
    quantity: int
    expiry_date: date
    unit_volume: Volume
    is_quarantined: bool = False

    def __post_init__(self):
        if self.quantity < 0:
            raise InventoryError(f"Batch {self.batch_number}: Quantity cannot be negative")

    @property
    def total_volume_m3(self) -> Decimal:
        """
        Calculates the total physical volume occupied by this batch in cubic meters.
        """
        return self.unit_volume.in_cubic_meters * Decimal(self.quantity)

    def decrease(self, amount: int) -> Decimal:
        """
        Reduces the quantity of the batch.

        Args:
            amount: The quantity to remove.

        Returns:
            Decimal: The volume (m3) freed up by this operation.

        Raises:
            InventoryError: If amount is negative.
            OutOfStockError: If the requested amount exceeds available quantity.
        """
        if amount < 0:
            raise InventoryError("Cannot decrease by negative amount")
        if amount > self.quantity:
            raise OutOfStockError(
                f"Batch {self.batch_number}: Requested {amount}, Available {self.quantity}"
            )

        self.quantity -= amount

        return self.unit_volume.in_cubic_meters * Decimal(amount)

    def increase(self, amount: int) -> Decimal:
        """
        Increases the quantity of the batch.

        Args:
            amount: The quantity to add.

        Returns:
            Decimal: The volume (m3) added by this operation.
        """
        if amount < 0:
            raise InventoryError("Cannot increase by negative amount")

        self.quantity += amount
        return self.unit_volume.in_cubic_meters * Decimal(amount)

    def is_expired(self, check_date: Optional[date] = None) -> bool:
        """
        Checks if the batch is expired relative to a given date.
        """
        target_date = check_date or date.today()
        return self.expiry_date < target_date


@dataclass
class Warehouse:
    """
    Aggregate Root representing a physical storage facility.
    Manages capacity, stock levels, and batch tracking.
    """
    id: int
    name: str
    address: Address
    capacity: Volume
    _current_load_m3: Decimal = field(default=Decimal("0.0"))
    _stock: Dict[int, List[StockBatch]] = field(default_factory=dict)

    @property
    def current_load(self) -> Volume:
        """
        The current volume occupied in the warehouse.
        """
        return Volume(self._current_load_m3, VolumeUnit.CUBIC_METER)

    @property
    def free_space(self) -> Volume:
        """
        The remaining available volume in the warehouse.
        """
        free_m3 = self.capacity.in_cubic_meters - self._current_load_m3
        return Volume(max(Decimal("0.0"), free_m3), VolumeUnit.CUBIC_METER)

    @property
    def stock_view(self) -> Dict[int, List[StockBatch]]:
        """
        Read-only view of the current stock.
        """
        return self._stock

    def get_total_quantity(self, product_id: int) -> int:
        """
        Calculates the total available quantity of a specific product.
        Excludes quarantined stock.

        Args:
            product_id: The ID of the product.

        Returns:
            int: The sum of non-quarantined items across all batches.
        """
        batches = self._stock.get(product_id, [])
        return sum(b.quantity for b in batches if not b.is_quarantined)

    def add_stock(self, product: BaseProduct, quantity: int, batch_number: str, expiry_date: date) -> None:
        """
        Adds products to the warehouse.
        Checks for capacity constraints and updates existing batches if matches are found.

        Args:
            product: The product entity being added.
            quantity: The number of units.
            batch_number: The manufacturer's batch number.
            expiry_date: The expiration date of the batch.

        Raises:
            WarehouseFullError: If adding the stock would exceed capacity.
            InventoryError: If quantity is invalid.
        """
        if quantity <= 0:
            raise InventoryError("Quantity must be positive")

        unit_vol = product.specs.packaging_volume
        total_vol_needed = unit_vol * quantity

        if total_vol_needed > self.free_space:
            raise WarehouseFullError(
                f"Warehouse {self.name} full. "
                f"Required: {total_vol_needed.in_cubic_meters:.4f} m3, "
                f"Free: {self.free_space.in_cubic_meters:.4f} m3"
            )

        if product.id not in self._stock:
            self._stock[product.id] = []

        existing_batch = next(
            (b for b in self._stock[product.id]
             if b.batch_number == batch_number
             and b.expiry_date == expiry_date
             and b.unit_volume == unit_vol),
            None
        )

        if existing_batch:
            added_vol = existing_batch.increase(quantity)
        else:
            new_batch = StockBatch(
                id=str(uuid4()),
                product_id=product.id,
                batch_number=batch_number,
                quantity=quantity,
                expiry_date=expiry_date,
                unit_volume=unit_vol
            )
            self._stock[product.id].append(new_batch)
            self._stock[product.id].sort(key=lambda b: b.expiry_date)
            added_vol = new_batch.total_volume_m3

        self._current_load_m3 += added_vol

    def reserve_stock(self, product_id: int, quantity: int) -> None:
        """
        Reserves and removes stock from the warehouse to fulfill an order.
        Uses a strategy to pick items (currently greedy/FEFO via sorted list).

        Args:
            product_id: The ID of the product.
            quantity: Amount to reserve.

        Raises:
            OutOfStockError: If insufficient non-quarantined stock exists.
        """
        if quantity <= 0:
            raise InventoryError("Quantity to reserve must be positive")

        available = self.get_total_quantity(product_id)
        if available < quantity:
            raise OutOfStockError(f"Product {product_id}: Requested {quantity}, Available {available}")

        batches = self._stock.get(product_id, [])
        remaining_to_take = quantity
        total_freed_vol_m3 = Decimal("0.0")

        for batch in batches:
            if batch.is_quarantined or batch.quantity == 0:
                continue

            take_from_batch = min(remaining_to_take, batch.quantity)

            freed_vol = batch.decrease(take_from_batch)
            total_freed_vol_m3 += freed_vol

            remaining_to_take -= take_from_batch

            if remaining_to_take == 0:
                break

        self._stock[product_id] = [b for b in batches if b.quantity > 0]

        self._update_load(-total_freed_vol_m3)

    def write_off_stock(self, product_id: int, batch_number: str, quantity: int, reason: str) -> None:
        """
        Removes stock manually (e.g., due to damage or expiry).
        """
        batches = self._stock.get(product_id, [])
        target_batch = next((b for b in batches if b.batch_number == batch_number), None)

        if not target_batch:
            raise InventoryError(f"Batch {batch_number} not found for product {product_id}")

        freed_vol = target_batch.decrease(quantity)
        self._update_load(-freed_vol)

        if target_batch.quantity == 0:
            batches.remove(target_batch)

    def set_batch_quarantine_status(self, product_id: int, batch_number: str, is_quarantined: bool) -> None:
        """
        Updates the quarantine status of a specific batch.
        Quarantined items are not available for reservation.
        """
        batches = self._stock.get(product_id, [])
        target_batch = next((b for b in batches if b.batch_number == batch_number), None)

        if not target_batch:
            raise InventoryError(f"Batch {batch_number} not found for product {product_id}")

        target_batch.is_quarantined = is_quarantined

    def _update_load(self, delta_m3: Decimal) -> None:
        """
        Internal helper to update the warehouse load safely.
        """
        self._current_load_m3 += delta_m3
        if self._current_load_m3 < 0:
            self._current_load_m3 = Decimal("0.0")


@dataclass
class Supplier:
    """
    Represents an external entity that supplies products.
    """
    id: int
    company_name: str
    contract_number: str
    is_active: bool = True