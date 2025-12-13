from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from datetime import timedelta

from src.pharma_distributor.common.units import MedicalDeviceClass
from src.pharma_distributor.exceptions import CatalogError
from src.pharma_distributor.finance.price import Price
from src.pharma_distributor.utils.validators import ProductValidator, PriceValidator
from .details import ProductInfo
from .categories import Category


@dataclass
class BaseProduct(ABC):
    product_id: int
    name: str
    price: Price
    category: Category
    info: ProductInfo
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        validator = ProductValidator()
        validator.validate(self)

    @abstractmethod
    def get_details(self) -> str:
        """:return: A string value with the main characteristics of the object"""
        pass

    def update_price(self, new_price: Price) -> None:
        """
        Updates the price
        :param new_price: New price value
        """
        validator = PriceValidator()
        validator.validate(new_price)
        self.price = new_price
        self.updated_at = datetime.now()

    def __repr__(self):
        return f"BaseProduct(id={self.product_id}, name='{self.name}')"


@dataclass
class Medicine(BaseProduct):
    manufacturer: str = ""
    composition: str = ""
    dosage: str = ""
    prescription_required: bool = False
    expiry_date: Optional[date] = None
    batch_number: str = ""

    def get_details(self) -> str:
        return (f"Medicine: {self.name}, "
                f"Manufacturer: {self.manufacturer}, "
                f"Dosage: {self.dosage}, "
                f"Exp: {self.expiry_date}")

    def is_expired(self) -> bool:
        if self.expiry_date:
            return self.expiry_date < date.today()
        return False

    # def validate(self):
    #     super().validate()
    #     if not self.manufacturer.strip():
    #         raise CatalogError("Medicine manufacturer cannot be empty")
    #     if self.expiry_date and self.expiry_date < date.today():
    #         raise CatalogError("Medicine is already expired")


@dataclass
class MedicalDevice(BaseProduct):
    model: str = ""
    serial_number: str = ""
    certified_by: str = ""
    usage_instructions: str = ""
    warranty_period: int = 5 # Month
    category_type: MedicalDeviceClass = field(default_factory=MedicalDeviceClass.CLASS3)

    def get_details(self) -> str:
        return f"MedicalDevice: {self.name}, Model: {self.model}, Serial: {self.serial_number}"

    def is_under_warranty(self) -> bool:
        warranty_end = self.created_at + timedelta(days=30 * self.warranty_period)
        return datetime.now() < warranty_end

    # def validate(self):
    #     super().validate()
    #     if not self.model.strip():
    #         raise CatalogError("Medical device model cannot be empty")
    #     if self.warranty_period < 0:
    #         raise CatalogError("Warranty period cannot be negative")
