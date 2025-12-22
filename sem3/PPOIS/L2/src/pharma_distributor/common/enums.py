from enum import Enum, auto


class Currency(Enum):
    BYN = "BYN"
    USD = "USD"
    EUR = "EUR"


class VolumeUnit(Enum):
    CUBIC_METER = "m^3"
    CUBIC_CENTIMETER = "cm^3"
    LITER = "l"
    MILLILITER = "ml"


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


class VehicleStatus(Enum):
    IDLE = auto()
    ON_ROUTE = auto()
    MAINTENANCE = auto()
    DECOMMISSIONED = auto()


class DriverStatus(Enum):
    AVAILABLE = auto()
    ON_TRIP = auto()
    OFF_DUTY = auto()


class RouteStatus(Enum):
    PLANNED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()