from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional
from abc import ABC, abstractmethod

from pharma_distributor.common.enums import WarrantyStatus
from pharma_distributor.common.models import Volume
from pharma_distributor.finance.models import Money
from pharma_distributor.exceptions import ValidationError


@dataclass
class Category:
    """
    Represents a product category in a hierarchical structure.
    Used to group products for reporting and bulk operations (e.g., discounts).
    """
    id: int
    name: str
    description: str
    parent_id: Optional[int] = None

    def is_root(self) -> bool:
        """
        Checks if this category is a top-level category (has no parent).

        Returns:
            bool: True if it is a root category, False otherwise.
        """
        return self.parent_id is None

    def update_details(self, name: str, description: str) -> None:
        """
        Updates the category's mutable details.

        Args:
            name: The new name for the category.
            description: The new description.

        Raises:
            ValidationError: If the provided name is empty.
        """
        if not name:
            raise ValidationError("Category name cannot be empty")
        self.name = name
        self.description = description


@dataclass
class ProductSpecification:
    """
    Value Object containing physical and logistical specifications of a product.
    """
    manufacturer: str
    country_of_origin: str
    storage_conditions: str
    packaging_volume: Volume

    def __post_init__(self):
        if not self.manufacturer:
            raise ValidationError("Manufacturer is required")


@dataclass(kw_only=True)
class BaseProduct(ABC):
    """
    Abstract base class representing a generic product in the catalog.
    Contains common attributes like price, name, and lifecycle status.
    """
    id: int
    name: str
    price: Money
    category: Category
    specs: ProductSpecification
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    def update_price(self, new_price: Money) -> None:
        """
        Updates the product's base selling price.

        Args:
            new_price: The new Money object representing the price.
        """
        self.price = new_price

    def apply_discount(self, percentage: float) -> None:
        """
        Applies a percentage discount to the current price.
        The price is updated permanently on the object.

        Args:
            percentage: The discount percentage (0 to 100).

        Raises:
            ValidationError: If the percentage is not between 0 and 100.
        """
        if not (0 < percentage < 100):
            raise ValidationError("Discount percentage must be between 0 and 100")

        factor = Decimal("1") - (Decimal(str(percentage)) / Decimal("100"))
        new_amount = self.price.amount * factor
        self.price = Money(new_amount.quantize(Decimal("0.01")), self.price.currency)

    def archive(self) -> None:
        """
        Marks the product as inactive (soft delete).
        Inactive products cannot be ordered or received.
        """
        self.is_active = False

    def restore(self) -> None:
        """
        Restores a previously archived product to active status.
        """
        self.is_active = True

    @abstractmethod
    def get_display_info(self) -> str:
        """
        Returns a human-readable summary string for the product.
        Must be implemented by subclasses.
        """
        ...


@dataclass(kw_only=True)
class Medicine(BaseProduct):
    """
    Represents a pharmaceutical product.
    Includes logic for expiration dates and prescription requirements.
    """
    dosage: str
    active_substance: str
    is_prescription_required: bool
    expiry_date: date

    def is_expired(self, on_date: Optional[date] = None) -> bool:
        """
        Checks if the medicine is expired relative to a specific date.

        Args:
            on_date: The date to check against. Defaults to today.

        Returns:
            bool: True if the expiry date is strictly before the check date.
        """
        check_date = on_date or date.today()
        return self.expiry_date < check_date

    def days_until_expiry(self) -> int:
        """
        Calculates the number of days remaining until expiration.
        Can return a negative number if already expired.
        """
        delta = self.expiry_date - date.today()
        return delta.days

    def requires_prescription_check(self) -> bool:
        """
        Indicates if the sale of this medicine requires verifying a prescription.
        """
        return self.is_prescription_required

    def get_display_info(self) -> str:
        return f'Medicine "{self.name}" ({self.dosage}) - Exp: {self.expiry_date}'


@dataclass(kw_only=True)
class MedicalDevice(BaseProduct):
    """
    Represents medical equipment or devices.
    Includes logic for warranty tracking and maintenance scheduling.
    """
    warranty_months: int
    serial_number: str
    service_interval_months: int
    last_service_date: Optional[date] = None
    purchase_date: Optional[date] = None

    def warranty_status(self) -> WarrantyStatus:
        """
        Determines the current warranty status based on purchase date and warranty duration.

        Returns:
            WarrantyStatus: One of NOT_PURCHASED, VALID_WARRANTY, or WARRANTY_EXPIRED.
        """
        if not self.purchase_date:
            return WarrantyStatus.NOT_PURCHASED

        if not self.is_under_warranty():
            return WarrantyStatus.WARRANTY_EXPIRED

        return WarrantyStatus.VALID_WARRANTY

    def is_under_warranty(self) -> bool:
        """
        Internal check to see if the warranty period is currently active.
        """
        if not self.purchase_date:
            return False

        warranty_end = self.purchase_date + timedelta(days=30 * self.warranty_months)
        return date.today() <= warranty_end

    def needs_maintenance(self) -> bool:
        """
        Checks if the device is due for maintenance based on the service interval.

        Returns:
            bool: True if maintenance is due or has never been performed.
        """
        if not self.last_service_date:
            return True

        next_service = self.last_service_date + timedelta(days=30 * self.service_interval_months)
        return date.today() >= next_service

    def perform_maintenance(self) -> None:
        """
        Records that maintenance was performed today.
        """
        self.last_service_date = date.today()

    def get_display_info(self) -> str:
        """
        Get information about medical device.
        """
        return f"{self.name} (SN: {self.serial_number})"