import random
import string
import time


class IDGenerator:

    @staticmethod
    def generate_uuid() -> str:
        timestamp = int(time.time() * 1000)
        random_part = random.randint(1000, 9999)
        return f"ID-{timestamp}-{random_part}"

    @staticmethod
    def generate_sku(prefix: str) -> str:
        chars = string.ascii_uppercase + string.digits
        suffix = ''.join(random.choice(chars) for _ in range(6))
        return f"{prefix}-{suffix}"


class PasswordHelper:

    @staticmethod
    def generate_salt() -> str:
        timestamp = str(int(time.time()))
        chars = string.ascii_letters + string.digits
        random_suffix = ''.join(random.choice(chars) for _ in range(8))
        return f"{timestamp}_{random_suffix}"

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        combined = password + salt
        return f"hashed_{combined}"