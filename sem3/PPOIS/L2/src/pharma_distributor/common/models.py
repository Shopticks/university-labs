from dataclasses import dataclass
from typing import Optional
from functools import total_ordering
from decimal import Decimal

from .enums import VolumeUnit
from src.pharma_distributor.exceptions import ValidationError
from src.pharma_distributor.utils.converters import VolumeConverter
from src.pharma_distributor.utils.validators import EmailValidator, PhoneValidator

@dataclass(frozen=True)
class Address:
    country: str
    city: str
    street: str
    zip_code: str


@dataclass(frozen=True)
class ContactInfo:
    email: str
    phone: str
    website: Optional[str] = None

    def __post_init__(self):
        email_validator = EmailValidator()
        phone_validator = PhoneValidator()

        email_validator.validate(self.email)
        phone_validator.validate(self.phone)


@total_ordering
@dataclass(frozen=True)
class Volume:
    amount: Decimal
    unit: VolumeUnit

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, 'amount', Decimal(str(self.amount)))

        if self.amount < 0:
            raise ValidationError("Volume cannot be negative")

    @property
    def in_cubic_meters(self) -> Decimal:
        return VolumeConverter.to_cubic_meters(self.amount, self.unit)

    def __add__(self, other: 'Volume') -> 'Volume':
        other_converted = VolumeConverter.convert(other.amount, other.unit, self.unit)
        return Volume(self.amount + other_converted, self.unit)

    def __mul__(self, multiplier: int) -> 'Volume':
        return Volume(self.amount * Decimal(multiplier), self.unit)

    def __lt__(self, other: 'Volume') -> bool:
        return self.in_cubic_meters < other.in_cubic_meters

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Volume):
            return NotImplemented
        return self.in_cubic_meters == other.in_cubic_meters