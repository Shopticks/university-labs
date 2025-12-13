from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from src.pharma_distributor.common.units import DimensionUnit, WeightUnit
from src.pharma_distributor.utils.converters import DimensionConverter
from src.pharma_distributor.utils.validators import NonNegativeValidator


@dataclass
class Dimension:
    _length: Decimal
    _width: Decimal
    _height: Decimal
    unit: DimensionUnit = DimensionUnit.MM

    def __post_init__(self):
        non_negative_validator = NonNegativeValidator()
        non_negative_validator.validate(self._length)
        non_negative_validator.validate(self._width)
        non_negative_validator.validate(self._height)

    def volume(self, out_unit: Optional[DimensionUnit] = None) -> Decimal:
        volume_mm3 = self._length * self._width * self._height
        if out_unit:
            factor = out_unit.value[1] ** 3
            return volume_mm3 / factor
        return volume_mm3

    def convert_to(self, new_unit: DimensionUnit) -> None:
        dim_converter = DimensionConverter()
        new_length = dim_converter.convert(self._length, self.unit, new_unit)
        new_width = dim_converter.convert(self._width, self.unit, new_unit)
        new_height = dim_converter.convert(self._height, self.unit, new_unit)
        self._length = new_length
        self._width = new_width
        self._height = new_height
        self.unit = new_unit

    @property
    def length(self):
        return round(self._length, 2)

    @length.setter
    def length(self, value: Decimal):
        non_negative_validator = NonNegativeValidator()
        non_negative_validator.validate(value)

        self._length = value

    @property
    def width(self):
        return round(self._width, 2)

    @width.setter
    def width(self, value: Decimal):
        non_negative_validator = NonNegativeValidator()
        non_negative_validator.validate(value)

        self._width = value

    @property
    def height(self):
        return round(self._height, 2)

    @height.setter
    def height(self, value: Decimal):
        non_negative_validator = NonNegativeValidator()
        non_negative_validator.validate(value)

        self._height = value


    def __str__(self):
        return f"{self._length}x{self._width}x{self._height} {self.unit.value[0]}"


@dataclass
class Weight:
    _value: Decimal
    unit: WeightUnit = WeightUnit.G

    @property
    def weight(self):
        return round(self._value, 2)

    @weight.setter
    def weight(self, value: Decimal):
        non_negative_validator = NonNegativeValidator()
        non_negative_validator.validate(value)

        self._value = value

    def __str__(self):
        return f"{self._value} {self.unit.value[0]}"


@dataclass
class Cargo:
    dimension: Dimension
    weight: Weight
    description: str = field(default_factory=str)

    def get_volume(self) -> Decimal:
        return self.dimension.volume()

    def get_weight_in_grams(self) -> Decimal:
        return self.weight

    def __repr__(self):
        return f"Cargo(volume={self.get_volume()}, \
                weight={self.get_weight_in_grams()}, \
                desc='{self.description[:20]}...')"