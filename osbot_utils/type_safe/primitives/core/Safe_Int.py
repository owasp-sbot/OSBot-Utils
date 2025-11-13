from typing                                                 import Optional, Union
from osbot_utils.type_safe.Type_Safe__Primitive             import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Float       import Safe_Float


class Safe_Int(Type_Safe__Primitive, int):            # Base class for type-safe integers with validation rules

    min_value      : Optional[int] = None    # Minimum allowed value (inclusive)
    max_value      : Optional[int] = None    # Maximum allowed value (inclusive)
    allow_none     : bool          = True    # Whether None is allowed as input
    allow_bool     : bool          = False   # Whether bool is allowed as input
    allow_str      : bool          = True    # Whether string conversion is allowed
    strict_type    : bool          = False   # If True, only accept int type (no conversions)
    clamp_to_range : bool          = False   # Will use the min_value and max_value in over/under flows


    def __new__(cls, value: Optional[Union[int, str]] = None) -> 'Safe_Int':
        # Handle None input
        if value is None:
            if cls.allow_none:
                # Determine appropriate default value
                if cls.min_value is not None and cls.min_value > 0:
                    default_value = cls.__default__value__()                        # Let this method or subclass decide
                else:
                    default_value = 0                 # Otherwise use 0
                return super().__new__(cls, default_value)
            else:
                raise ValueError(f"{cls.__name__} does not allow None values")

        # Strict type checking
        if cls.strict_type and not isinstance(value, int):
            raise TypeError(f"{cls.__name__} requires int type, got {type(value).__name__}")

        # Type conversion
        if isinstance(value, str):
            if not cls.allow_str:
                raise TypeError(f"{cls.__name__} does not allow string conversion")
            try:
                value = int(value)
            except ValueError:
                raise ValueError(f"Cannot convert '{value}' to integer")

        elif isinstance(value, bool):
            if not cls.allow_bool:
                raise TypeError(f"{cls.__name__} does not allow boolean values")
            value = int(value)

        elif not isinstance(value, int):
            raise TypeError(f"{cls.__name__} requires an integer value, got {type(value).__name__}")

        # Range validation
        if cls.clamp_to_range and value is not None:
            if cls.min_value is not None and value < cls.min_value:
                value = cls.min_value
            if cls.max_value is not None and value > cls.max_value:
                value = cls.max_value
        else:
            if cls.min_value is not None and value < cls.min_value:
                raise ValueError(f"{cls.__name__} must be >= {cls.min_value}, got {value}") from None

            if cls.max_value is not None and value > cls.max_value:
                raise ValueError(f"{cls.__name__} must be <= {cls.max_value}, got {value}") from None

        return super().__new__(cls, value)

    @classmethod
    def __default__value__(cls):
        return cls.min_value                         # Use min_value if it's positive

    # Arithmetic operations that maintain type safety
    # In Safe_Int class
    def __add__(self, other):
        result = super().__add__(other)
        if result is NotImplemented:
            return result  # Let Python handle the reverse operation
        return self.__class__(result)

    def __sub__(self, other):
        result = super().__sub__(other)
        if result is NotImplemented:
            return result
        return self.__class__(result)

    def __mul__(self, other):
        result = super().__mul__(other)
        if result is NotImplemented:
            return result
        return self.__class__(result)

    def __truediv__(self, other):
        result = super().__truediv__(other)
        return Safe_Float(result)

    def __floordiv__(self, other):                              # Floor division (//)
        result = super().__floordiv__(other)
        if result is NotImplemented:
            return result
        return self.__class__(result)

    # Add augmented assignment operators to maintain type safety
    def __iadd__(self, other):
        result = int(self) + other
        if result is NotImplemented:
            return result
        return self.__class__(result)

    def __isub__(self, other):
        result = int(self) - other
        if result is NotImplemented:
            return result
        return self.__class__(result)

    def __imul__(self, other):
        result = int(self) * other
        if result is NotImplemented:
            return result
        return self.__class__(result)

    def __itruediv__(self, other):
        """In-place true division (/=)"""
        result = int(self) / other
        return Safe_Float(result)  # Division returns float

    def __ifloordiv__(self, other):
        """In-place floor division (//=)"""
        result = int(self) // other
        return self.__class__(result)  # Goes through validation

    def __imod__(self, other):
        """In-place modulo (%=)"""
        result = int(self) % other
        return self.__class__(result)  # Goes through validation

    def __radd__(self, other):
        """Reverse addition"""
        result = super().__radd__(other)
        if result is NotImplemented:
            return result
        return self.__class__(result)

    def __rsub__(self, other):
        """Reverse subtraction"""
        result = super().__rsub__(other)
        if result is NotImplemented:
            return result
        return self.__class__(result)

    def __rmul__(self, other):
        """Reverse multiplication"""
        result = super().__rmul__(other)
        if result is NotImplemented:
            return result
        return self.__class__(result)

    def __rfloordiv__(self, other):                     # Reverse floor division
        result = super().__rfloordiv__(other)
        if result is NotImplemented:
            return result
        return self.__class__(result)

    def __mod__(self, other):                           # Modulo (%)
        result = super().__mod__(other)
        if result is NotImplemented:
            return result
        return self.__class__(result)

    def __rmod__(self, other):                          # Reverse modulo
        result = super().__rmod__(other)
        if result is NotImplemented:
            return result
        return self.__class__(result)