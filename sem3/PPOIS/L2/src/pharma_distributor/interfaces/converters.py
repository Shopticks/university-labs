from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any


class BaseConverter(ABC):
    """
    Abstract interface for generic unit conversion logic.
    """

    @abstractmethod
    def convert(self, value: Decimal, from_unit: Any, to_unit: Any) -> Decimal:
        """
        Converts a numeric value from one unit to another.

        Args:
            value: The numeric amount to convert.
            from_unit: The source unit.
            to_unit: The target unit.

        Returns:
            Decimal: The converted value.
        """
        ...


class BaseCurrencyConverter(BaseConverter, ABC):
    """
    Abstract interface specifically for currency conversion operations.
    """

    @abstractmethod
    def get_exchange_rate(self, from_currency: Any, to_currency: Any) -> Decimal:
        """
        Retrieves the current exchange rate between two currencies.

        Args:
            from_currency: The base currency.
            to_currency: The target currency.

        Returns:
            Decimal: The exchange rate multiplier.
        """
        ...

    @abstractmethod
    def convert(self, value: Decimal, from_unit: Any, to_unit: Any) -> Decimal:
        """
        Converts a monetary amount between currencies using current rates.
        """
        ...


class BaseDimensionConverter(BaseConverter, ABC):
    """
    Abstract interface for physical dimension conversions (e.g., volume, size).
    """

    @abstractmethod
    def get_dimensions_rate(self, from_dimension: Any, to_dimension: Any) -> Decimal:
        """
        Retrieves the conversion factor between two physical dimensions.
        """
        ...

    @abstractmethod
    def convert(self, volume: Decimal, from_unit: Any, to_unit: Any) -> Decimal:
        """
        Converts a volume/size measurement between units.
        """
        ...