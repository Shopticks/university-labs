from dataclasses import dataclass
from typing import Optional
from functools import total_ordering
from decimal import Decimal

from .enums import VolumeUnit
from pharma_distributor.exceptions import ValidationError
from pharma_distributor.utils.converters import VolumeConverter
from pharma_distributor.utils.validators import EmailValidator, PhoneValidator

@dataclass(frozen=True)
class Address:
    """
    Value Object representing a physical location.
    Immutable.
    """
    country: str
    city: str
    street: str
    zip_code: str


@dataclass(frozen=True)
class ContactInfo:
    """
    Value Object containing contact details.
    Validates email and phone formats upon initialization.
    """
    email: str
    phone: str
    website: Optional[str] = None

    def __post_init__(self):
        """
        Validates the format of email and phone number.
        Raises ValidationError if formats are invalid.
        """
        email_validator = EmailValidator()
        phone_validator = PhoneValidator()

        email_validator.validate(self.email)
        phone_validator.validate(self.phone)


@total_ordering
@dataclass(frozen=True)
class Volume:
    """
    Value Object representing physical volume with a specific unit.
    Supports arithmetic operations and automatic unit conversion for comparisons.
    """
    amount: Decimal
    unit: VolumeUnit

    def __post_init__(self):
        """
        Ensures amount is a Decimal and strictly non-negative.
        """
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, 'amount', Decimal(str(self.amount)))

        if self.amount < 0:
            raise ValidationError("Volume cannot be negative")

    @property
    def in_cubic_meters(self) -> Decimal:
        """
        Returns the volume amount normalized to cubic meters.
        Used primarily for standardized comparisons.
        """
        return VolumeConverter().to_cubic_meters(self.amount, self.unit)

    def __add__(self, other: 'Volume') -> 'Volume':
        """
        Adds two Volume objects.
        Converts the 'other' volume to 'this' volume's unit before adding.

        Returns:
            Volume: A new Volume object in the unit of the left-hand operand.
        """
        other_converted = VolumeConverter().convert(other.amount, other.unit, self.unit)
        return Volume(self.amount + other_converted, self.unit)

    def __mul__(self, multiplier: int) -> 'Volume':
        """
        Multiplies the volume by a scalar.

        Returns:
            Volume: A new Volume object with scaled amount.
        """
        return Volume(self.amount * Decimal(multiplier), self.unit)

    def __lt__(self, other: 'Volume') -> bool:
        """
        Compares two volumes based on their normalized cubic meter value.
        """
        return self.in_cubic_meters < other.in_cubic_meters

    def __eq__(self, other: object) -> bool:
        """
        Checks equality based on normalized cubic meter value.
        """
        if not isinstance(other, Volume):
            return NotImplemented
        return self.in_cubic_meters == other.in_cubic_meters