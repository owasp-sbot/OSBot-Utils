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
    allow_inf      : bool            = False
    strict_type    : bool            = False
    decimal_places : Optional[int]   = None

    # Precision handling options
    use_decimal    : bool            = True                              # ensure that we are using Decimals under the hood, so that 0.1 + 0.2 is indeed 0.3
    epsilon        : float           = 1e-9
    round_output   : bool            = True
    clamp_to_range : bool            = False

    def __new__(cls, value: Optional[Union[float, int, str]] = None) -> 'Safe_Float':
        if value is None:
            if cls.allow_none:
                return super().__new__(cls, 0.0)
            else:
                raise ValueError(f"{cls.__name__} does not allow None values")

        # Handle Decimal input specially to preserve precision
        preserve_decimal = isinstance(value, Decimal) and cls.use_decimal

        if isinstance(value, Decimal):
            # For Decimal input when use_decimal=True, keep precision
            if not cls.use_decimal:
                value = float(value)  # Convert to float if not using Decimal
            # else: keep as Decimal for now
        elif isinstance(value, str):
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

        # Get numeric value for range checking
        check_value = float(value) if isinstance(value, Decimal) else value

        # Range validation BEFORE rounding (unless clamping)
        if not cls.clamp_to_range:
            if cls.min_value is not None and check_value < cls.min_value:
                raise ValueError(f"{cls.__name__} must be >= {cls.min_value}, got {check_value}")
            if cls.max_value is not None and check_value > cls.max_value:
                raise ValueError(f"{cls.__name__} must be <= {cls.max_value}, got {check_value}")

        # Apply rounding while preserving type
        if isinstance(value, Decimal) and cls.decimal_places is not None:
            value = value.quantize(Decimal(f'0.{"0" * cls.decimal_places}'), rounding=ROUND_HALF_UP)
        elif not isinstance(value, Decimal) and cls.round_output and cls.decimal_places is not None:
            value = cls.__clean_float(value, cls.decimal_places)

        # Convert to float at the very end
        if isinstance(value, Decimal):
            value = float(value)

        # Check for special values after conversion
        if math.isinf(value):
            raise ValueError(f"{cls.__name__} does not allow infinite values")
        if math.isnan(value):
            raise ValueError(f"{cls.__name__} does not allow NaN values")

        # Handle clamping AFTER everything else
        if cls.clamp_to_range:
            if cls.min_value is not None and value < cls.min_value:
                value = cls.min_value
            if cls.max_value is not None and value > cls.max_value:
                value = cls.max_value

        return super().__new__(cls, value)

    def __add__(self, other):
        if self.use_decimal:
            self_decimal = Decimal(str(float(self)))
            other_decimal = Decimal(str(float(other))) if not isinstance(other, Decimal) else other
            result = self_decimal + other_decimal

            if self.decimal_places is not None:
                quantize_str = '0.' + '0' * self.decimal_places
                result = result.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
        else:
            result = float(self) + float(other)
            if self.round_output and self.decimal_places is not None:
                if not (math.isinf(result) or math.isnan(result)):
                    result = self.__clean_float(result, self.decimal_places)

        # Add overflow check here
        check_value = float(result) if isinstance(result, Decimal) else result
        if math.isinf(check_value):
            raise OverflowError(f"Addition resulted in inf")
        if math.isnan(check_value):
            raise OverflowError(f"Addition resulted in nan")

        try:
            return self.__class__(result)
        except (ValueError, TypeError):
            if isinstance(result, Decimal):
                result = float(result)
            return result

    def __sub__(self, other):
        if self.use_decimal:
            self_decimal = Decimal(str(float(self)))
            other_decimal = Decimal(str(float(other))) if not isinstance(other, Decimal) else other
            result = self_decimal - other_decimal

            if self.decimal_places is not None:
                quantize_str = '0.' + '0' * self.decimal_places
                result = result.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
        else:
            result = float(self) - float(other)
            if self.round_output and self.decimal_places is not None:
                if not (math.isinf(result) or math.isnan(result)):
                    result = self.__clean_float(result, self.decimal_places)

        # Add overflow check here
        check_value = float(result) if isinstance(result, Decimal) else result
        if math.isinf(check_value):
            raise OverflowError(f"Subtraction resulted in inf")
        if math.isnan(check_value):
            raise OverflowError(f"Subtraction resulted in nan")

        try:
            return self.__class__(result)
        except (ValueError, TypeError):
            if isinstance(result, Decimal):
                result = float(result)
            return result

    def __rsub__(self, other):
        if self.use_decimal:
            self_decimal = Decimal(str(float(self)))
            other_decimal = Decimal(str(float(other))) if not isinstance(other, Decimal) else other
            result = other_decimal - self_decimal

            if self.decimal_places is not None:
                quantize_str = '0.' + '0' * self.decimal_places
                result = result.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
        else:
            result = float(other) - float(self)
            if self.round_output and self.decimal_places is not None:
                if not (math.isinf(result) or math.isnan(result)):
                    result = self.__clean_float(result, self.decimal_places)

        # Add overflow check here
        check_value = float(result) if isinstance(result, Decimal) else result
        if math.isinf(check_value):
            raise OverflowError(f"Subtraction resulted in inf")
        if math.isnan(check_value):
            raise OverflowError(f"Subtraction resulted in nan")

        try:
            return self.__class__(result)
        except (ValueError, TypeError):
            if isinstance(result, Decimal):
                result = float(result)
            return result

    def __radd__(self, other):
        return self.__add__(other)  # Addition is commutative

    def __str__(self):
        if self.decimal_places is not None:
            return f"{float(self):.{self.decimal_places}f}"
        return super().__str__()

    def __mul__(self, other):
        if self.use_decimal:
            self_decimal = Decimal(str(float(self)))
            other_decimal = Decimal(str(float(other))) if not isinstance(other, Decimal) else other
            result = self_decimal * other_decimal

            if self.decimal_places is not None:
                quantize_str = '0.' + '0' * self.decimal_places
                result = result.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
        else:
            result = float(self) * float(other)
            if self.round_output and self.decimal_places is not None:
                if not (math.isinf(result) or math.isnan(result)):
                    result = self.__clean_float(result, self.decimal_places)

        # Check for overflow BEFORE trying to create instance
        check_value = float(result) if isinstance(result, Decimal) else result
        if math.isinf(check_value) and self.allow_inf is False:
            raise OverflowError(f"Multiplication resulted in inf")
        if math.isnan(check_value) and self.allow_none is False:
            raise OverflowError(f"Multiplication resulted in nan")

        try:
            return self.__class__(result)
        except (ValueError, TypeError):
            if isinstance(result, Decimal):
                result = float(result)
            return result

    def __truediv__(self, other):
        if float(other) == 0:
            raise ZeroDivisionError(f"{self.__class__.__name__} division by zero")

        if self.use_decimal:
            self_decimal = Decimal(str(float(self)))
            other_decimal = Decimal(str(float(other))) if not isinstance(other, Decimal) else other
            result = self_decimal / other_decimal

            if self.decimal_places is not None:
                quantize_str = '0.' + '0' * self.decimal_places
                result = result.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
        else:
            result = float(self) / float(other)
            if self.round_output and self.decimal_places is not None:
                if not (math.isinf(result) or math.isnan(result)):
                    result = self.__clean_float(result, self.decimal_places)

        # Check for overflow/underflow - handle both Decimal and float
        check_value = float(result) if isinstance(result, Decimal) else result
        if math.isinf(check_value):
            raise OverflowError(f"Division resulted in inf")
        if math.isnan(check_value):
            raise OverflowError(f"Division resulted in nan")

        try:
            return self.__class__(result)
        except (ValueError, TypeError):
            if isinstance(result, Decimal):
                result = float(result)
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


    def __eq__(self, other):
        """Equality with epsilon tolerance"""
        if isinstance(other, (int, float)):
            return abs(float(self) - float(other)) < self.epsilon
        return super().__eq__(other)

    def __rmul__(self, other):
        return self.__mul__(other)  # Multiplication is commutative

    def __rtruediv__(self, other):
        if float(self) == 0:
            raise ZeroDivisionError(f"{self.__class__.__name__} division by zero")

        if self.use_decimal:
            self_decimal = Decimal(str(float(self)))
            other_decimal = Decimal(str(float(other))) if not isinstance(other, Decimal) else other
            result = other_decimal / self_decimal

            if self.decimal_places is not None:
                quantize_str = '0.' + '0' * self.decimal_places
                result = result.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
        else:
            result = float(other) / float(self)
            if self.round_output and self.decimal_places is not None:
                if not (math.isinf(result) or math.isnan(result)):
                    result = self.__clean_float(result, self.decimal_places)

        if isinstance(result, float) and (math.isinf(result) or math.isnan(result)):
            raise OverflowError(f"Division resulted in {result}")

        try:
            return self.__class__(result)
        except (ValueError, TypeError):
            if isinstance(result, Decimal):
                result = float(result)
            return result