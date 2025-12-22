from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from pharma_distributor.common.enums import Role
from pharma_distributor.common.models import ContactInfo
from pharma_distributor.utils.generators import PasswordHelper
from pharma_distributor.exceptions import ValidationError, AuthenticationError


@dataclass
class Credentials:
    """
       Encapsulates user authentication data including password hash and security salt.
    """
    username: str
    password_hash: str
    salt: str
    last_password_change: datetime = field(default_factory=datetime.now)

    def verify_password(self, plain_password: str) -> bool:
        """
            Verifies if the provided plain text password matches the stored hash.

            Args:
                plain_password: The raw password provided by the user.

            Returns:
                bool: True if the password is correct, False otherwise.
        """
        expected_hash = PasswordHelper.hash_password(plain_password, self.salt)
        return self.password_hash == expected_hash

    def update_password(self, new_password: str) -> None:
        """
        Updates the stored credentials with a new password.
        Generates a new salt and hash, and updates the timestamp.

        Args:
            new_password: The new raw password string.

        Raises:
            ValidationError: If the password is shorter than 8 characters.
        """
        if len(new_password) < 8:
            raise ValidationError("Password is too short")

        self.salt = PasswordHelper.generate_salt()
        self.password_hash = PasswordHelper.hash_password(new_password, self.salt)
        self.last_password_change = datetime.now()


@dataclass
class User:
    """
    Represents a system user with specific role, contact details, and security credentials.
    Functions as an Aggregate Root for user-related operations.
    """
    id: int
    full_name: str
    role: Role
    contact: ContactInfo
    credentials: Credentials
    is_active: bool = True

    def deactivate(self) -> None:
        """
        Deactivates the user account, preventing future logins.
        """
        self.is_active = False


    def activate(self) -> None:
        """
        Activates the user account, allowing logins.
        """
        self.is_active = True

    def update_contact_info(
            self,
            new_email: Optional[str] = None,
            new_phone: Optional[str] = None,
            new_website: Optional[str] = None) -> None:
        """
        Updates the user's contact information. Only provided fields are updated.

        Args:
            new_email: The new email address (optional).
            new_phone: The new phone number (optional).
            new_website: The new website URL (optional).
        """
        current = self.contact
        self.contact = ContactInfo(
            email=new_email if new_email else current.email,
            phone=new_phone if new_phone else current.phone,
            website=new_website if new_website else current.website
        )

    def has_permission(self, required_role: Role) -> bool:
        """
        Checks if the user has the required permission level.
        Admins automatically have permissions for all roles.
        Inactive users have no permissions.

        Args:
            required_role: The role required to perform an action.

        Returns:
            bool: True if authorized, False otherwise.
        """
        if not self.is_active:
            return False
        if self.role == Role.ADMIN:
            return True
        return self.role == required_role

    def change_password(self, old_password: str, new_password: str) -> None:
        """
        Changes the user's password after verifying the old one.

        Args:
            old_password: The current password for verification.
            new_password: The new password to set.

        Raises:
            AuthenticationError: If the old password provided is incorrect.
            ValidationError: If the new password does not meet security requirements.
        """
        if not self.credentials.verify_password(old_password):
            raise AuthenticationError("Old password is correct")

        self.credentials.update_password(new_password)