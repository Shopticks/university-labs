"""Utility functions for validation and common operations."""

import re
from typing import Optional, Tuple
from datetime import datetime, date
import hashlib

# Import validation exception
from ..exceptions import ValidationError


# ============= EMAIL VALIDATION =============

def normalize_email(email: str) -> str:
    """
    Normalize email address.

    Args:
        email: Email address

    Returns:
        str: Normalized email
    """
    return email.strip().lower()


def validate_email_format(email: str) -> bool:
    """
    Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        bool: True if valid format
    """
    if not email:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


# ============= PHONE VALIDATION =============

def normalize_phone(phone: str) -> str:
    """
    Normalize phone number.

    Args:
        phone: Phone number

    Returns:
        str: Normalized phone (digits only)
    """
    return re.sub(r'\D', '', phone)


def validate_phone_format(phone: str) -> bool:
    """
    Validate phone number format.

    Args:
        phone: Phone number to validate

    Returns:
        bool: True if valid format
    """
    if not phone:
        return False

    digits = normalize_phone(phone)
    return len(digits) == 12


def format_phone_display(phone: str) -> str:
    """
    Format phone number for display.

    Args:
        phone: Phone number

    Returns:
        str: Formatted phone number
    """
    digits = normalize_phone(phone)

    return f"+{phone[0:3]} ({phone[3:5]}) {phone[5:8]}-{phone[8:10]}-{phone[10:]}"


# ============= PASSWORD VALIDATION =============

def validate_password_strength(password: str, min_length: int = 8) -> Tuple[bool, str]:
    """
    Validate password strength.

    Args:
        password: Password to validate
        min_length: Minimum password length

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"

    return True, ""


def hash_password(password: str) -> str:
    """
    Hash password.

    Args:
        password: Password to hash

    Returns:
        str: Hashed password
    """

    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify password against hash.

    Args:
        password: Plain password
        hashed: Hashed password

    Returns:
        bool: True if password matches
    """
    return hash_password(password) == hashed


# ============= DATE/TIME UTILITIES =============

def calculate_age(birth_date: date) -> int:
    """
    Calculate age from birth date.

    Args:
        birth_date: Date of birth

    Returns:
        int: Age in years
    """
    today = date.today()
    return today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def days_between(date1: datetime, date2: datetime) -> int:
    """
    Calculate days between two dates.

    Args:
        date1: First date
        date2: Second date

    Returns:
        int: Number of days
    """
    return abs((date2 - date1).days)