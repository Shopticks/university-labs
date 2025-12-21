from dataclasses import dataclass
from typing import Optional

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