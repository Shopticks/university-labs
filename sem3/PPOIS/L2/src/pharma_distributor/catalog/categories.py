from dataclasses import dataclass, field
from typing import List, Optional

from src.pharma_distributor.catalog.products import BaseProduct
from src.pharma_distributor.exceptions import CategoryError


@dataclass
class Category:
    category_id: int
    name: str
    info: str
    parent_category: Optional['Category'] = None
    products: List['BaseProduct'] = field(default_factory=list)
    subcategories: List['Category'] = field(default_factory=list)

    def get_info(self):
        return f"ID: {self.category_id}, Name: {self.name}, Products: {len(self.products)}"

    def add_product(self, product: 'BaseProduct') -> None:
        self.products.append(product)

    def add_subcategory(self, subcategory: 'Category') -> None:
        self.subcategories.append(subcategory)

    def remove_product(self, product: 'BaseProduct') -> None:
        if product in self.products:
            self.products.remove(product)
        else:
            raise CategoryError("The category does not contain this product")

    def remove_subcategory(self, subcategory: 'Category'):
        if subcategory in self.subcategories:
            self.subcategories.remove(subcategory)
        else:
            raise CategoryError("The category does not contain this subcategory")

    def get_all_products(self) -> List['BaseProduct']:
        all_products = self.products[:]
        for sub in self.subcategories:
            all_products.extend(sub.get_all_products())
        return all_products

    def set_info(self, description: str):
        self.info = description.strip()

    def __repr__(self):
        return f"Category(name='{self.name}', id={self.category_id})"