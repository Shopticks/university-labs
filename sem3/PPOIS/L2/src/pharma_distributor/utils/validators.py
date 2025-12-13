from abc import ABC, abstractmethod
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.pharma_distributor.catalog.products import BaseProduct, ProductInfo
    from src.pharma_distributor.finance.price import Price

from src.pharma_distributor.exceptions import CatalogError, FinanceError


class BaseValidator(ABC):

    @abstractmethod
    def validate(self, *args, **kwargs):
        pass


class NonNegativeValidator(BaseValidator):
    def validate(self, value: Decimal):
        if value < 0:
            raise ValueError(f"Value need to be positive, got {value}")


class PriceValidator(BaseValidator):
    def validate(self, price: 'Price'):
        non_negative_validator = NonNegativeValidator()

        try:
            non_negative_validator.validate(price.get_amount())
        except ValueError as e:
            raise FinanceError(e)


class ProductInfoValidator(BaseValidator):
    def validate(self, info: 'ProductInfo'):
        if info.weight <= 0:
            raise CatalogError("ProductInfo weight must be positive")
        if not info.barcode:
            raise CatalogError("ProductInfo barcode cannot be empty")


class ProductValidator(BaseValidator):
    def validate(self, product: 'BaseProduct'):
        if product.product_id <= 0:
            raise CatalogError(f"Product ID must be positive, got {product.product_id}")
        if not product.name.strip():
            raise CatalogError("Product name cannot be empty")

        info_validator = ProductInfoValidator()
        info_validator.validate(product.info)

        price_validator = PriceValidator()
        price_validator.validate(product.price)