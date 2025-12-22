from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional
from abc import ABC, abstractmethod

from src.pharma_distributor.common.enums import WarrantyStatus
from src.pharma_distributor.common.models import Volume
from src.pharma_distributor.finance.models import Money
from src.pharma_distributor.exceptions import ValidationError


@dataclass
class Category:
    id: int
    name: str
    description: str
    parent_id: Optional[int] = None

    def is_root(self) -> bool:
        return self.parent_id is None

    def update_details(self, name: str, description: str) -> None:
        if not name:
            raise ValidationError("Category name cannot be empty")
        self.name = name
        self.description = description


@dataclass
class ProductSpecification:
    manufacturer: str
    country_of_origin: str
    storage_conditions: str
    packaging_volume: Volume

    def __post_init__(self):
        if not self.manufacturer:
            raise ValidationError("Manufacturer is required")


@dataclass(kw_only=True)
class BaseProduct(ABC):
    id: int
    name: str
    price: Money
    category: Category
    specs: ProductSpecification
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    def update_price(self, new_price: Money) -> None:
        self.price = new_price

    def apply_discount(self, percentage: float) -> None:
        if not (0 < percentage < 100):
            raise ValidationError("Discount percentage must be between 0 and 100")

        factor = Decimal("1") - (Decimal(str(percentage)) / Decimal("100"))
        new_amount = self.price.amount * factor
        self.price = Money(new_amount.quantize(Decimal("0.01")), self.price.currency)

    def archive(self) -> None:
        self.is_active = False

    def restore(self) -> None:
        self.is_active = True

    @abstractmethod
    def get_display_info(self) -> str:
        ...


@dataclass(kw_only=True)
class Medicine(BaseProduct):
    dosage: str
    active_substance: str
    is_prescription_required: bool
    expiry_date: date

    def is_expired(self, on_date: Optional[date] = None) -> bool:
        check_date = on_date or date.today()
        return self.expiry_date < check_date

    def days_until_expiry(self) -> int:
        delta = self.expiry_date - date.today()
        return delta.days

    def requires_prescription_check(self) -> bool:
        return self.is_prescription_required

    def get_display_info(self) -> str:
        return f'Medicine "{self.name}" ({self.dosage}) - Exp: {self.expiry_date}'


@dataclass(kw_only=True)
class MedicalDevice(BaseProduct):
    warranty_months: int
    serial_number: str
    service_interval_months: int
    last_service_date: Optional[date] = None
    purchase_date: Optional[date] = None

    def warranty_status(self) -> WarrantyStatus:
        if not self.purchase_date:
            return WarrantyStatus.NOT_PURCHASED

        if not self.is_under_warranty():
            return WarrantyStatus.WARRANTY_EXPIRED

        return WarrantyStatus.VALID_WARRANTY

    def is_under_warranty(self) -> bool:
        if not self.purchase_date:
            return False

        warranty_end = self.purchase_date + timedelta(days=30 * self.warranty_months)
        return date.today() <= warranty_end

    def needs_maintenance(self) -> bool:
        if not self.last_service_date:
            return True

        next_service = self.last_service_date + timedelta(days=30 * self.service_interval_months)
        return date.today() >= next_service

    def perform_maintenance(self) -> None:
        self.last_service_date = date.today()

    def get_display_info(self) -> str:
        return f"{self.name} (SN: {self.serial_number})"