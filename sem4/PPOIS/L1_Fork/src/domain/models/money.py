from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Money:
    """
    Сlass for presentation and work with money.

    Args:
        amount (Decimal): An amount of money.
    
    Raises:
        ValueError: Occurs when attempting to subtract if the result is negative.
    """
    amount: Decimal

    def __add__(self, other: 'Money') -> 'Money':
        """Adds two sums of money.

        Args:
            other (Money): Another Money object for addition.

        Returns:
            Money: New Money object with the sum of two values.
        """
        return Money(self.amount + other.amount)

    def __sub__(self, other: 'Money') -> 'Money':
        """Subtracts one amount of money from another.

        Args:
            other (Money): Another Money object for substraction.

        Raises:
            ValueError: If the result of the subtraction is negative.

        Returns:
            Money: New Money object with the subtraction of values.
        """
        if self.amount < other.amount:
            raise ValueError("Resulting money cannot be negative")
        return Money(self.amount - other.amount)

    # === Comparison functions ===

    def __ge__(self, other: 'Money') -> bool:
        return self.amount >= other.amount
    
    def __gt__(self, other: 'Money') -> bool:
        return self.amount > other.amount
    
    def __le__(self, other: 'Money') -> bool:
        return self.amount <= other.amount

    def __lt__(self, other: 'Money') -> bool:
        return self.amount < other.amount
    
    def __str__(self) -> str:
        """Money object user-friendly view"""
        return f"{self.amount:.2f} BYN"
    
    def __repr__(self):
        """Money object representation"""
        return f"Money(amount={self.amount})"