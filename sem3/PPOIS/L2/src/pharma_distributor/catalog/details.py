from dataclasses import dataclass

from src.pharma_distributor.logistics.cargo import Weight, Dimension


@dataclass
class ProductInfo:
    barcode: str
    weight: Weight
    dimensions: Dimension
    packaging_type: str
    country_of_origin: str
    storage_conditions: str = "Room temperature"