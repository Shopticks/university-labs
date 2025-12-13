from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any


class IConverter(ABC):
    """Abstract converter class"""

    @abstractmethod
    def convert(self, value: Decimal, from_unit: Any, to_unit: Any) -> Decimal:
        """Convert value between dimensions"""
        ...


class ICurrencyConverter(IConverter, ABC):
    """Abstract currency converter"""

    @abstractmethod
    def get_exchange_rate(self, from_currency: Any, to_currency: Any) -> Decimal:
        """Get exchange rate"""
        ...

    @abstractmethod
    def convert(self, value: Decimal, from_unit: Any, to_unit: Any) -> Decimal:
        ...


class IDimensionConverter(IConverter, ABC):
    """Abstract size converter"""

    @abstractmethod
    def get_dimensions_rate(self, from_dimension: Any, to_dimension: Any) -> Decimal:
        """Get dimensions rate"""
        ...

    @abstractmethod
    def convert(self, volume: Decimal, from_unit: Any, to_unit: Any) -> Decimal:
        ...