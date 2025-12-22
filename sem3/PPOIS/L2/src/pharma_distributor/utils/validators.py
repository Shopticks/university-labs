import re
from typing import Any
from src.pharma_distributor.exceptions import ValidationError
from src.pharma_distributor.interfaces.validators import BaseValidator


class EmailValidator(BaseValidator[str]):
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def validate(self, value: str) -> None:
        if not re.match(self.EMAIL_REGEX, value):
            raise ValidationError(f"Invalid email format: {value}")


class PhoneValidator(BaseValidator[str]):
    PHONE_REGEX = r"^\+?[1-9]\d{1,14}$"

    def validate(self, value: Any) -> None:
        if not re.match(self.PHONE_REGEX, value):
            raise ValidationError(f"Invalid phone format: {value}")


class TaxIdValidator(BaseValidator[str]):
    def validate(self, value: Any) -> None:
        if not value.isdigit():
            raise ValidationError("Tax ID must contain only digits")

        if len(value) not in (10, 12):
            raise ValidationError("Tax ID must be 10 or 12 digits long")