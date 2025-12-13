from enum import Enum
from decimal import Decimal


class DimensionUnit(Enum):
    MM = ("millimeter", Decimal("1"))
    CM = ("centimeter", Decimal("10"))
    M = ("meter", Decimal("1000"))


class WeightUnit(Enum):
    G = ("gram", Decimal("1"))
    KG = ("kilogram", Decimal("1000"))
    T = ("tonne", Decimal("1_000_000"))


class Currency(Enum):
    BYN = Decimal("1")
    USD = Decimal("2.92")
    EUR = Decimal("3.45")
    RUB = Decimal("0.0371")


class MedicalDeviceClass(Enum):
    CLASS1 = "Class I (Low Risk)"
    CLASS2A = "Class IIA (Medium Risk)"
    CLASS2B = "Class IIB (Medium-High Risk)"
    CLASS3 = "Class III (High Risk)"

