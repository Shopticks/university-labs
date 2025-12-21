from datetime import date
from typing import List, Optional

from src.pharma_distributor.catalog.models import (
    Medicine,
    MedicalDevice,
    BaseProduct,
    Category
)
from src.pharma_distributor.common.enums import WarrantyStatus
from src.pharma_distributor.finance.models import Money
from src.pharma_distributor.exceptions import ValidationError
from src.pharma_distributor.interfaces.base import IRepository


class CatalogService:
    def __init__(self, product_repository: IRepository[BaseProduct]):
        self.product_repo = product_repository

    def get_product_by_id(self, product_id: int) -> BaseProduct:
        product = self.product_repo.get(product_id)

        if not product:
            raise ValidationError(f"Product with ID {product_id} not found")

        return product

    def register_product(self, product: BaseProduct) -> None:
        self.product_repo.save(product)

    def update_price(self, product_id: int, new_price: Money) -> None:
        product = self.get_product_by_id(product_id)

        product.update_price(new_price)

        self.product_repo.save(product)

    def check_expiration(self, medicine: Medicine) -> bool:
        return medicine.is_expired()

    def get_expiring_medicines(self, days_threshold: int = 30) -> List[Medicine]:
        all_products = self.product_repo.list_all()
        expiring = []

        for product in all_products:
            if isinstance(product, Medicine):
                if 0 < product.days_until_expiry() <= days_threshold:
                    expiring.append(product)

        return expiring

    def apply_category_discount(self, category: Category, percentage: float) -> int:
        all_products = self.product_repo.list_all()
        updated_count = 0

        for product in all_products:
            if product.category.id == category.id:
                product.apply_discount(percentage)
                self.product_repo.save(product)
                updated_count += 1

        return updated_count

    def get_warranty_status(self, device: MedicalDevice) -> WarrantyStatus:
        return device.warranty_status()

    def schedule_maintenance(self, device: MedicalDevice) -> None:
        device.perform_maintenance()
        self.product_repo.save(device)