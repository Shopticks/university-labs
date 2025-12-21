from enum import Enum, auto


class Currency(Enum):
    BYN = "BYN"
    USD = "USD"
    EUR = "EUR"


class WeightUnit(Enum):
    G = "g"
    KG = "kg"
    T = "t"


class Role(Enum):
    ADMIN = auto()
    MANAGER = auto()
    WAREHOUSE_WORKER = auto()
    USER = auto()


class OrderStatus(Enum):
    NEW = auto()
    PAID = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


class WarrantyStatus(Enum):
    NOT_PURCHASED = auto()
    VALID_WARRANTY = auto()
    WARRANTY_EXPIRED = auto()