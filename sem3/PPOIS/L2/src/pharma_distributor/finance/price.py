from decimal import Decimal
from dataclasses import dataclass, field

from src.pharma_distributor.common.units import Currency
from src.pharma_distributor.utils.validators import PriceValidator, NonNegativeValidator
from src.pharma_distributor.utils.converters import CurrencyConverter


@dataclass
class Price:
    _amount: Decimal = field(default_factory=Decimal)
    currency: Currency = Currency.BYN

    def __post_init__(self):
        price_validator = PriceValidator()
        price_validator.validate(self)

    def convert_to(self, target_currency: Currency) -> None:
        currency_converter = CurrencyConverter()
        new_amount = currency_converter.convert(
            self._amount, self.currency, target_currency
        )
        self.amount = new_amount
        self.currency = target_currency

    @property
    def amount(self) -> Decimal:
        return round(self._amount, 2)

    @amount.setter
    def amount(self, value: Decimal):
        non_negative_validator = NonNegativeValidator()
        non_negative_validator.validate(value)

        self._amount = value

    def __str__(self):
        return f"{self._amount} {self.currency.name}"
