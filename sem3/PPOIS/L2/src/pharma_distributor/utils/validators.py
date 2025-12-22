import re
from typing import Any
from pharma_distributor.exceptions import ValidationError
from pharma_distributor.interfaces.validators import BaseValidator


class EmailValidator(BaseValidator[str]):
    """
    Validates email addresses using a standard regex pattern.
    """
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def validate(self, value: str) -> None:
        """
        Args:
            value: The email string to check.

        Raises:
            ValidationError: If the email format is invalid.
        """
        if not re.match(self.EMAIL_REGEX, value):
            raise ValidationError(f"Invalid email format: {value}")


class PhoneValidator(BaseValidator[str]):
    """
    Validates international phone numbers.
    Allows optional leading '+' followed by 10-15 digits.
    """
    PHONE_REGEX = r"^\+?[1-9]\d{1,14}$"

    def validate(self, value: Any) -> None:
        """
        Args:
            value: The phone number string.

        Raises:
            ValidationError: If the phone format is invalid.
        """
        if not re.match(self.PHONE_REGEX, value):
            raise ValidationError(f"Invalid phone format: {value}")


class TaxIdValidator(BaseValidator[str]):
    """
    Validates corporate Tax Identification Numbers (TIN).
    Enforces numeric digits and specific length constraints (10 or 12).
    """
    def validate(self, value: Any) -> None:
        """
        Args:
            value: The Tax ID string.

        Raises:
            ValidationError: If non-digits are present or length is incorrect.
        """
        if not value.isdigit():
            raise ValidationError("Tax ID must contain only digits")

        if len(value) not in (10, 12):
            raise ValidationError("Tax ID must be 10 or 12 digits long")