from decimal import Decimal
from src.pharma_distributor.common.enums import Currency, WeightUnit, VolumeUnit
from src.pharma_distributor.interfaces.converters import IConverter


class CurrencyConverter(IConverter):
    RATES = {
        (Currency.USD, Currency.BYN): Decimal("3.20"),
        (Currency.EUR, Currency.BYN): Decimal("3.50"),
    }

    def convert(self, amount: Decimal, from_c: Currency, to_c: Currency) -> Decimal:
        if from_c == to_c:
            return amount

        pair = (from_c, to_c)
        if pair in self.RATES:
            return amount * self.RATES[pair]

        reverse_pair = (to_c, from_c)
        if reverse_pair in self.RATES:
            return amount / self.RATES[reverse_pair]

        raise NotImplementedError(f"Conversion {from_c} -> {to_c} not supported")


class VolumeConverter(IConverter):
    _TO_M3 = {
        VolumeUnit.CUBIC_METER: Decimal("1.0"),
        VolumeUnit.LITER: Decimal("0.001"),
        VolumeUnit.CUBIC_CENTIMETER: Decimal("0.000001"),
        VolumeUnit.MILLILITER: Decimal("0.000001"),
    }

    def to_cubic_meters(self, amount: Decimal, unit: VolumeUnit) -> Decimal:
        if unit not in self._TO_M3:
            raise NotImplementedError(f"Conversion for {unit} not implemented")

        return amount * self._TO_M3[unit]

    def convert(self, amount: Decimal, from_unit: VolumeUnit, to_unit: VolumeUnit) -> Decimal:
        if from_unit == to_unit:
            return amount

        in_m3 = self.to_cubic_meters(amount, from_unit)

        factor = self._TO_M3[to_unit]
        return in_m3 / factor