from decimal import Decimal
from pharma_distributor.common.enums import Currency, WeightUnit, VolumeUnit
from pharma_distributor.interfaces.converters import BaseConverter


class CurrencyConverter(BaseConverter):
    """
    Service for converting monetary amounts between supported currencies.
    Uses a hardcoded exchange rate table for demonstration purposes.
    """
    RATES = {
        (Currency.USD, Currency.BYN): Decimal("3.20"),
        (Currency.EUR, Currency.BYN): Decimal("3.50"),
    }

    def convert(self, amount: Decimal, from_c: Currency, to_c: Currency) -> Decimal:
        """
        Converts an amount from one currency to another.

        Args:
            amount: The monetary amount.
            from_c: The source currency.
            to_c: The target currency.

        Returns:
            Decimal: The converted amount.

        Raises:
            NotImplementedError: If the currency pair is not supported in the rate table.
        """
        if from_c == to_c:
            return amount

        pair = (from_c, to_c)
        if pair in self.RATES:
            return amount * self.RATES[pair]

        reverse_pair = (to_c, from_c)
        if reverse_pair in self.RATES:
            return amount / self.RATES[reverse_pair]

        raise NotImplementedError(f"Conversion {from_c} -> {to_c} not supported")


class VolumeConverter(BaseConverter):
    """
    Service for converting physical volume measurements.
    Standardizes all units to Cubic Meters (m^3) as the intermediate base unit.
    """
    _TO_M3 = {
        VolumeUnit.CUBIC_METER: Decimal("1.0"),
        VolumeUnit.LITER: Decimal("0.001"),
        VolumeUnit.CUBIC_CENTIMETER: Decimal("0.000001"),
        VolumeUnit.MILLILITER: Decimal("0.000001"),
    }

    def to_cubic_meters(self, amount: Decimal, unit: VolumeUnit) -> Decimal:
        """
        Normalizes a volume amount to cubic meters.

        Args:
            amount: The value to convert.
            unit: The source unit.

        Returns:
            Decimal: The value in cubic meters.
        """
        if unit not in self._TO_M3:
            raise NotImplementedError(f"Conversion for {unit} not implemented")

        return amount * self._TO_M3[unit]

    def convert(self, amount: Decimal, from_unit: VolumeUnit, to_unit: VolumeUnit) -> Decimal:
        """
        Converts volume between any two supported units.
        """
        if from_unit == to_unit:
            return amount

        in_m3 = self.to_cubic_meters(amount, from_unit)

        factor = self._TO_M3[to_unit]
        return in_m3 / factor