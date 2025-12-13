from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class IValidator(Protocol):
    """Протокол для валидаторов"""

    def validate(self, value: Any) -> None:
        """Валидация значения, выбрасывает исключение при ошибке"""
        ...


class IPriceValidator(ABC):
    """Абстрактный валидатор для цен"""

    @abstractmethod
    def validate_amount(self, amount: Decimal) -> None:
        """Валидация суммы"""
        ...

    @abstractmethod
    def validate_currency(self, currency: Any) -> None:
        """Валидация валюты"""
        ...


class PriceValidator(IPriceValidator):
    def validate(self, value: Any) -> None:
        pass

    def validate_amount(self, amount: Decimal) -> None:
        pass

    def validate_currency(self, currency: Any) -> None:
        pass


a = PriceValidator()

print(isinstance(a, IValidator))