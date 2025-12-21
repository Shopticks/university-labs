from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.pharma_distributor.common.enums import Role
from src.pharma_distributor.common.models import ContactInfo
from src.pharma_distributor.utils.generators import PasswordHelper
from src.pharma_distributor.exceptions import ValidationError, AuthenticationError


@dataclass
class Credentials:
    username: str
    password_hash: str
    salt: str
    last_password_change: datetime = field(default_factory=datetime.now)

    def verify_password(self, plain_password: str) -> bool:
        expected_hash = PasswordHelper.hash_password(plain_password, self.salt)
        return self.password_hash == expected_hash

    def update_password(self, new_password: str) -> None:
        if len(new_password) < 8:
            raise ValidationError("Password is too short")

        self.salt = PasswordHelper.generate_salt()
        self.password_hash = PasswordHelper.hash_password(new_password, self.salt)
        self.last_password_change = datetime.now()


@dataclass
class User:
    id: int
    full_name: str
    role: Role
    contact: ContactInfo
    credentials: Credentials
    is_active: bool = True

    def deactivate(self) -> None:
        self.is_active = False


    def activate(self) -> None:
        self.is_active = True

    def update_contact_info(
            self,
            new_email: Optional[str] = None,
            new_phone: Optional[str] = None,
            new_website: Optional[str] = None) -> None:

        current = self.contact
        self.contact = ContactInfo(
            email=new_email if new_email else current.email,
            phone=new_phone if new_phone else current.phone,
            website=new_website if new_website else current.website
        )

    def has_permission(self, required_role: Role) -> bool:
        if not self.is_active:
            return False
        if self.role == Role.ADMIN:
            return True
        return self.role == required_role

    def change_password(self, old_password: str, new_password: str) -> None:
        if not self.credentials.verify_password(old_password):
            raise AuthenticationError("Old password is correct")

        self.credentials.update_password(new_password)