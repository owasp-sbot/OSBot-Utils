import math
from decimal                                    import Decimal, ROUND_HALF_UP, InvalidOperation
from typing                                     import Optional, Union
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive


class Safe_Float(Type_Safe__Primitive, float):                             # Base class for type-safe floats with validation rules

    min_value      : Optional[float] = None
    max_value      : Optional[float] = None
    allow_none     : bool            = True
    allow_bool     : bool            = False
    allow_str      : bool            = True
    allow_int      : bool            = True
    strict_type    : bool            = False
    decimal_places : Optional[int]   = None

    # Precision handling options
    use_decimal    : bool            = False
    epsilon        : float           = 1e-9
    round_output   : bool            = True
    clamp_to_range : bool            = False

    def __new__(cls, value: Optional[Union[float, int, str]] = None) -> 'Safe_Float':
        if value is None:
            if cls.allow_none:
                return super().__new__(cls, 0.0)
            else:
                raise ValueError(f"{cls.__name__} does not allow None values")

        # Store original value for range checking
        original_value = value

        # Convert to float
        if isinstance(value, str):
            if not cls.allow_str:
                raise TypeError(f"{cls.__name__} does not allow string conversion")
            try:
                if cls.use_decimal:
                    value = Decimal(value)
                else:
                    value = float(value)
            except (ValueError, InvalidOperation):
                raise ValueError(f"Cannot convert '{value}' to float")
        elif isinstance(value, bool):
            if not cls.allow_bool:
                raise TypeError(f"{cls.__name__} does not allow boolean values")
            value = float(value)
        elif isinstance(value, int):
            if not cls.allow_int:
                raise TypeError(f"{cls.__name__} does not allow integer conversion")
            if cls.use_decimal:
                value = Decimal(value)
            else:
                value = float(value)
        elif isinstance(value, float):
            if math.isinf(value):
                raise ValueError(f"{cls.__name__} does not allow infinite values")
            if math.isnan(value):
                raise ValueError(f"{cls.__name__} does not allow NaN values")

            if cls.use_decimal:
                value = Decimal(str(value))
        elif not isinstance(value, (float, Decimal)):
            raise TypeError(f"{cls.__name__} requires a float value, got {type(value).__name__}")

        # Get numeric value for range checking (before rounding)
        check_value = float(value) if isinstance(value, Decimal) else value

        # Range validation BEFORE rounding (unless clamping)
        if not cls.clamp_to_range:
            if cls.min_value is not None and check_value < cls.min_value:
                raise ValueError(f"{cls.__name__} must be >= {cls.min_value}, got {check_value}")
            if cls.max_value is not None and check_value > cls.max_value:
                raise ValueError(f"{cls.__name__} must be <= {cls.max_value}, got {check_value}")

        # NOW do rounding
        if isinstance(value, Decimal) and cls.decimal_places is not None:
            value = value.quantize(Decimal(f'0.{"0" * cls.decimal_places}'), rounding=ROUND_HALF_UP)

        if isinstance(value, Decimal):
            value = float(value)

        # Check again for special values
        if math.isinf(value):
            raise ValueError(f"{cls.__name__} does not allow infinite values")
        if math.isnan(value):
            raise ValueError(f"{cls.__name__} does not allow NaN values")

        # Clean up floating point errors (only if not already handled by Decimal)
        if cls.round_output and cls.decimal_places is not None and not cls.use_decimal:
            value = cls.__clean_float(value, cls.decimal_places)

        # Handle clamping AFTER rounding
        if cls.clamp_to_range:
            if cls.min_value is not None and value < cls.min_value:
                value = cls.min_value
            if cls.max_value is not None and value > cls.max_value:
                value = cls.max_value

        return super().__new__(cls, value)

    def __truediv__(self, other):
        # Simple and safe - no special handling for infinity
        if float(other) == 0:
            raise ZeroDivisionError(f"{self.__class__.__name__} division by zero")

        if self.use_decimal:
            result = float(Decimal(str(float(self))) / Decimal(str(float(other))))
        else:
            result = float(self) / float(other)

        # Check for overflow/underflow
        if math.isinf(result) or math.isnan(result):
            raise OverflowError(f"Division resulted in {result}")

        if self.round_output and self.decimal_places is not None:
            result = self.__clean_float(result, self.decimal_places)

        try:
            return self.__class__(result)
        except (ValueError, TypeError):
            return result

    @classmethod
    def __clean_float(cls, value: float, decimal_places: int) -> float:             # Clean up floating point representation errors
        rounded = round(value, decimal_places + 2)                                  # First, round to eliminate tiny errors

        # Check if very close to a clean decimal
        str_val = f"{rounded:.{decimal_places + 2}f}"
        if str_val.endswith('999999') or str_val.endswith('000001'):
            # Use Decimal for exact rounding
            d = Decimal(str(value))
            return float(d.quantize(Decimal(f'0.{"0" * decimal_places}'), rounding=ROUND_HALF_UP))

        return round(value, decimal_places) if decimal_places else value

    def __mul__(self, other):
        if self.use_decimal:
            result = float(Decimal(str(float(self))) * Decimal(str(float(other))))
        else:
            result = float(self) * float(other)

        if self.round_output and self.decimal_places is not None:
            if not (math.isinf(result) or math.isnan(result)):
                result = self.__clean_float(result, self.decimal_places)

        try:
            return self.__class__(result)
        except (ValueError, TypeError):
            return result

    def __eq__(self, other):
        """Equality with epsilon tolerance"""
        if isinstance(other, (int, float)):
            return abs(float(self) - float(other)) < self.epsilon
        return super().__eq__(other)