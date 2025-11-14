"""Customer class with needed information."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


from .contact import Contact


class CustomerType(Enum):
    INDIVIDUAL = "individual"
    CORPORATE = "corporate"


class CustomerStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"


@dataclass
class Customer:
    customer_id: str
    name: str
    customer_type: CustomerType
    status: CustomerStatus = CustomerStatus.ACTIVE
    contacts: List[Contact] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def add_contact(self, contact: Contact) -> None:
        """Add a contact to the customer.

        Args:
            contact (Contact): Contact object to be added.
        """
        if not self.contacts:
            contact.mark_as_primary()
        self.contacts.append(contact)
