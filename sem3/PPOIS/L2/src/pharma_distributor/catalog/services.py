from typing import List

from pharma_distributor.catalog.models import (
    Medicine,
    MedicalDevice,
    BaseProduct,
    Category
)
from pharma_distributor.common.enums import WarrantyStatus
from pharma_distributor.exceptions import ValidationError
from pharma_distributor.finance.models import Money
from pharma_distributor.interfaces.base import IRepository


class CatalogService:
    """
    Domain service for managing the product catalog.
    Handles product lifecycle, pricing updates, and specialized logic for medicines and devices.
    """
    def __init__(self, product_repository: IRepository[BaseProduct]):
        """
        Args:
            product_repository: Data access interface for products.
        """
        self.product_repo = product_repository

    def get_product_by_id(self, product_id: int) -> BaseProduct:
        """
        Retrieves a product by its unique ID.

        Args:
            product_id: The ID of the product.

        Returns:
            BaseProduct: The found product entity.

        Raises:
            ValidationError: If the product does not exist.
        """
        product = self.product_repo.get(product_id)

        if not product:
            raise ValidationError(f"Product with ID {product_id} not found")

        return product

    def register_product(self, product: BaseProduct) -> None:
        """
        Persists a new product into the repository.

        Args:
            product: The initialized product entity to save.
        """
        self.product_repo.save(product)

    def update_price(self, product_id: int, new_price: Money) -> None:
        """
        Updates the price of an existing product.

        Args:
            product_id: The ID of the product to update.
            new_price: The new Money value to set.
        """
        product = self.get_product_by_id(product_id)

        product.update_price(new_price)

        self.product_repo.save(product)

    def check_expiration(self, medicine: Medicine) -> bool:
        """
        Checks if a specific medicine is expired.
        """
        return medicine.is_expired()

    def get_expiring_medicines(self, days_threshold: int = 30) -> List[Medicine]:
        """
        Retrieves a list of medicines that will expire within the given threshold.

        Args:
            days_threshold: Number of days to look ahead (default 30).

        Returns:
            List[Medicine]: A list of medicines expiring soon (or already expired).
        """
        all_products = self.product_repo.list_all()
        expiring = []

        for product in all_products:
            if isinstance(product, Medicine):
                if 0 < product.days_until_expiry() <= days_threshold:
                    expiring.append(product)

        return expiring

    def apply_category_discount(self, category: Category, percentage: float) -> int:
        """
        Applies a percentage discount to all products within a specific category.
        This operation persists changes to the repository immediately.

        Args:
            category: The target Category.
            percentage: The discount percentage to apply.

        Returns:
            int: The count of products updated.
        """
        all_products = self.product_repo.list_all()
        updated_count = 0

        for product in all_products:
            if product.category.id == category.id:
                product.apply_discount(percentage)
                self.product_repo.save(product)
                updated_count += 1

        return updated_count

    def get_warranty_status(self, device: MedicalDevice) -> WarrantyStatus:
        """
        Calculates the warranty status for a medical device.
        """
        return device.warranty_status()

    def schedule_maintenance(self, device: MedicalDevice) -> None:
        """
        Performs maintenance on a medical device and updates its service record.

        Args:
            device: The device undergoing maintenance.
        """
        device.perform_maintenance()
        self.product_repo.save(device)