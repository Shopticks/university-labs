from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Union

from src.pharma_distributor.common.units import DimensionUnit, WeightUnit, Currency
from src.pharma_distributor.exceptions import ConversionError


class BaseConverter(ABC):
    @abstractmethod
    def convert(self, value: Decimal,
                unit_from: Union[DimensionUnit, WeightUnit, Currency],
                unit_to: Union[DimensionUnit, WeightUnit, Currency]
                ) -> Decimal:
        pass


class DimensionConverter(BaseConverter):
    def convert(self, value: Decimal, unit_from: DimensionUnit, unit_to: DimensionUnit) -> Decimal:
        try:
            base_value = value * unit_from.value[1]
            result = base_value / unit_to.value[1]
            return result
        except Exception as e:
            raise ConversionError(f"Failed to convert dimension: {e}")


class WeightConverter(BaseConverter):
    def convert(self, value: Decimal, unit_from: WeightUnit, unit_to: WeightUnit) -> Decimal:
        try:
            base_value = value * unit_from.value[1]
            result = base_value / unit_to.value[1]
            return result
        except Exception as e:
            raise ConversionError(f"Failed to convert weight: {e}")


class CurrencyConverter(BaseConverter):
    def convert(self, value: Decimal, unit_from: Currency, unit_to: Currency) -> Decimal:
        try:
            base_value = value * unit_from.value
            result = base_value / unit_to.value
            return result
        except Exception as e:
            raise ConversionError(f"Failed to convert currency: {e}")