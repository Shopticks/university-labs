import random
import string
import time


class IDGenerator:
    """
    Utility for generating unique identifiers for system entities.
    """

    @staticmethod
    def generate_uuid() -> str:
        """
        Generates a pseudo-unique ID based on the current timestamp and a random suffix.
        Format: "ID-{timestamp}-{random}"
        """
        timestamp = int(time.time() * 1000)
        random_part = random.randint(1000, 9999)
        return f"ID-{timestamp}-{random_part}"

    @staticmethod
    def generate_sku(prefix: str) -> str:
        """
        Generates a Stock Keeping Unit (SKU) identifier.

        Args:
            prefix: A string prefix (e.g., category code).

        Returns:
            str: Format "{prefix}-{random_alphanumeric_suffix}"
        """
        chars = string.ascii_uppercase + string.digits
        suffix = ''.join(random.choice(chars) for _ in range(6))
        return f"{prefix}-{suffix}"


class PasswordHelper:
    """
    Utility for handling basic password security operations (hashing and salting).
    Note: This is a simulation and not suitable for production cryptographic security.
    """

    @staticmethod
    def generate_salt() -> str:
        """
        Generates a random salt string combining a timestamp and random characters.
        """
        timestamp = str(int(time.time()))
        chars = string.ascii_letters + string.digits
        random_suffix = ''.join(random.choice(chars) for _ in range(8))
        return f"{timestamp}_{random_suffix}"

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """
        Creates a simulated hash of the password combined with the salt.
        """
        combined = password + salt
        return f"hashed_{combined}"