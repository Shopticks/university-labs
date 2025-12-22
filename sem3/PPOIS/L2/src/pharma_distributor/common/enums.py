from enum import Enum, auto


class Currency(Enum):
    """
    Supported currencies for financial transactions and pricing.
    """
    BYN = "BYN"
    USD = "USD"
    EUR = "EUR"


class VolumeUnit(Enum):
    """
    Units of measurement for physical volume.
    Used for warehouse capacity calculations and product packaging specs.
    """
    CUBIC_METER = "m^3"
    CUBIC_CENTIMETER = "cm^3"
    LITER = "l"
    MILLILITER = "ml"


class WeightUnit(Enum):
    """
    Units of measurement for weight/mass.
    """
    G = "g"
    KG = "kg"
    T = "t"


class Role(Enum):
    """
    User roles for authorization and access control.
    """
    ADMIN = auto()
    MANAGER = auto()
    WAREHOUSE_WORKER = auto()
    USER = auto()


class OrderStatus(Enum):
    """
    Lifecycle states of a sales order.
    """
    NEW = auto()
    PAID = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


class WarrantyStatus(Enum):
    """
    Status of a medical device's warranty coverage.
    """
    NOT_PURCHASED = auto()
    VALID_WARRANTY = auto()
    WARRANTY_EXPIRED = auto()


class VehicleStatus(Enum):
    """
    Operational status of a fleet vehicle.
    """
    IDLE = auto()
    ON_ROUTE = auto()
    MAINTENANCE = auto()
    DECOMMISSIONED = auto()


class DriverStatus(Enum):
    """
    Availability status of a driver.
    """
    AVAILABLE = auto()
    ON_TRIP = auto()
    OFF_DUTY = auto()


class RouteStatus(Enum):
    """
    Execution status of a logistics delivery route.
    """
    PLANNED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()