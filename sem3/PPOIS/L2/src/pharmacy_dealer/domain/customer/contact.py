"""Contact information management for customers."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List

# Import validators from utils
from ...utils.validator import (
    validate_email_format,
    validate_phone_format,
    format_phone_display,
    normalize_email,
    normalize_phone
)


class ContactType(Enum):
    EMAIL = "email"
    PHONE = "phone"
    MOBILE = "mobile"
    ADDRESS = "address"
    MESSENGER = "messenger"


class ContactPreferences(Enum):
    EMAIL_ONLY = "email_only"
    SMS = "sms"
    PHONE_CALL = "phone_call"
    NO_MARKETING = "no_marketing"
    ALL_CHANNELS = "all_channels"


@dataclass
class Contact:
    """Contact information for a customer."""

    contact_id: str
    contact_type: ContactType
    value: str
    is_primary: bool = False
    is_verified: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    notes: str = ""

    def verify(self) -> bool:
        """
        Verify contact information based on type.

        Returns:
            bool: True if verification successful
        """
        if self.contact_type == ContactType.EMAIL:
            if validate_email_format(self.value):
                self.value = normalize_email(self.value)
                self.is_verified = True
                self.updated_at = datetime.now()
                return True
            return False

        elif self.contact_type in (ContactType.PHONE, ContactType.MOBILE):
            if validate_phone_format(self.value):
                self.value = normalize_phone(self.value)
                self.is_verified = True
                self.updated_at = datetime.now()
                return True
            return False
        else:
            # Other contact types are always valid
            self.is_verified = True
            return True

    def update_value(self, new_value: str) -> None:
        """
        Update contact value and mark as unverified.

        Args:
            new_value: New contact value
        """
        self.value = new_value
        self.is_verified = False
        self.updated_at = datetime.now()

    def mark_as_primary(self) -> None:
        """Mark this contact as primary."""
        self.is_primary = True
        self.updated_at = datetime.now()

    def get_display_value(self) -> str:
        """
        Get formatted display value.

        Returns:
            str: Formatted contact value
        """
        if self.contact_type in (ContactType.PHONE, ContactType.MOBILE):
            return format_phone_display(self.value)
        return self.value

    def is_expired(self, days: int = 365) -> bool:
        """
        Check if contact hasn't been updated in specified days.

        Args:
            days: Number of days to consider expired. Defaults to 365.

        Returns:
            bool: True if expired
        """
        check_date = self.updated_at or self.created_at
        return (datetime.now() - check_date).days > days
