from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any


class IValidator(ABC):

    @abstractmethod
    def validate(self, value: Any) -> None:
        ...


class IPriceValidator(IValidator, ABC):

    @abstractmethod
    def validate_amount(self, amount: Decimal) -> None:
        ...

    @abstractmethod
    def validate_currency(self, currency: Any) -> None:
        ...


class IProductValidator(IValidator, ABC):

    @abstractmethod
    def validate_basic_info(self, product: Any) -> None:
        ...

    @abstractmethod
    def validate_details(self, product: Any) -> None:
        ...