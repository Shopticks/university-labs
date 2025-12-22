from datetime import date, timedelta
from typing import List, Optional

from pharma_distributor.catalog.models import BaseProduct, Medicine
from pharma_distributor.exceptions import ValidationError
from pharma_distributor.inventory.models import Warehouse, StockBatch


class InventoryManager:
    """
    Domain service orchestrating inventory operations that involve complex business logic,
    validations, or multiple entities.
    """

    def receive_shipment(
            self,
            warehouse: Warehouse,
            product: BaseProduct,
            quantity: int,
            batch_number: str,
            expiry_date: Optional[date] = None,
            min_shelf_life_days: int = 180
    ) -> None:
        """
        Processes an incoming shipment of goods into the warehouse.
        Performs validation checks for product activity, expiration dates,
        and minimum shelf life requirements for medicines.

        Args:
            warehouse: The destination warehouse.
            product: The product being received.
            quantity: The quantity received.
            batch_number: The batch identifier.
            expiry_date: The expiration date (mandatory for medicines).
            min_shelf_life_days: Minimum required days before expiry for acceptance (default 180).

        Raises:
            ValidationError: If product is inactive, expired, or has insufficient shelf life.
        """
        if not product.is_active:
            raise ValidationError(f"Cannot accept inactive product: {product.name}")

        if isinstance(product, Medicine):
            if not expiry_date:
                raise ValidationError(f"Expiry date is mandatory for medicine: {product.name}")

            today = date.today()
            if expiry_date <= today:
                raise ValidationError(f"Cannot accept expired goods. Expired on: {expiry_date}")

            remaining_days = (expiry_date - today).days
            if remaining_days < min_shelf_life_days:
                raise ValidationError(
                    f"Remaining shelf life ({remaining_days} days) is less than "
                    f"required minimum ({min_shelf_life_days} days)"
                )
        else:
            if expiry_date and expiry_date <= date.today():
                raise ValidationError(f"Cannot accept expired goods. Expired on: {expiry_date}")

            if not expiry_date:
                # Basic requirement for traceability in this system
                raise ValidationError("Expiry date is required for batch tracking logic")

        warehouse.add_stock(product, quantity, batch_number, expiry_date)

    def reserve_stock(self, warehouse: Warehouse, product_id: int, quantity: int) -> None:
        """
        Delegates stock reservation to the warehouse entity.
        """
        warehouse.reserve_stock(product_id, quantity)

    def get_stock_level(self, warehouse: Warehouse, product_id: int) -> int:
        """
        Queries the warehouse for available stock of a product.
        """
        return warehouse.get_total_quantity(product_id)

    def set_batch_quarantine_status(
            self,
            warehouse: Warehouse,
            product_id: int,
            batch_number: str,
            is_quarantined: bool,
            reason: str = ""
    ) -> None:
        """
        Updates quarantine status for a batch in a specific warehouse.
        """
        warehouse.set_batch_quarantine_status(product_id, batch_number, is_quarantined)

    def write_off_stock(
            self,
            warehouse: Warehouse,
            product_id: int,
            batch_number: str,
            quantity: int,
            reason: str
    ) -> None:
        """
        Delegates stock write-off to the warehouse entity.
        """
        warehouse.write_off_stock(product_id, batch_number, quantity, reason)

    def check_expiring_goods(self, warehouse: Warehouse, threshold_days: int = 30) -> List[StockBatch]:
        """
        Scans the warehouse for batches that are approaching their expiration date.

        Args:
            warehouse: The warehouse to inspect.
            threshold_days: The number of days from today to check for expiration.

        Returns:
            List[StockBatch]: A list of batches expiring within the threshold.
        """
        expiring_batches = []
        check_date = date.today() + timedelta(days=threshold_days)

        for product_batches in warehouse.stock_view.values():
            for batch in product_batches:
                if batch.quantity > 0 and batch.expiry_date <= check_date:
                    expiring_batches.append(batch)

        return expiring_batches