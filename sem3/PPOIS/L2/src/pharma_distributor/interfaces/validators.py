from abc import ABC, abstractmethod
from typing import TypeVar, Generic


T = TypeVar('T')


class BaseValidator(ABC, Generic[T]):
    """
    Abstract base class for creating reusable validation logic.
    Follows the Strategy pattern for validation.
    """

    @abstractmethod
    def validate(self, value: T) -> None:
        """
        Validates the provided value.

        Args:
            value: The value to check.

        Raises:
            ValidationError: If the value does not meet the criteria.
        """
        ...