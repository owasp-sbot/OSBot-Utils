from typing                                     import Optional, Union
from osbot_utils.helpers.safe_float.Safe_Float  import Safe_Float
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive


class Safe_Int(Type_Safe__Primitive, int):            # Base class for type-safe integers with validation rules

    min_value      : Optional[int] = None    # Minimum allowed value (inclusive)
    max_value      : Optional[int] = None    # Maximum allowed value (inclusive)
    allow_none     : bool          = True    # Whether None is allowed as input
    allow_bool     : bool          = False   # Whether bool is allowed as input
    allow_str      : bool          = True    # Whether string conversion is allowed
    strict_type    : bool          = False   # If True, only accept int type (no conversions)

    def __new__(cls, value: Optional[Union[int, str]] = None) -> 'Safe_Int':
        # Handle None input
        if value is None:
            if cls.allow_none:
                return super().__new__(cls, 0)  # Default to 0 for None
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
        if cls.min_value is not None and value < cls.min_value:
            raise ValueError(f"{cls.__name__} must be >= {cls.min_value}, got {value}")

        if cls.max_value is not None and value > cls.max_value:
            raise ValueError(f"{cls.__name__} must be <= {cls.max_value}, got {value}")

        return super().__new__(cls, value)

    # Arithmetic operations that maintain type safety
    def __add__(self, other):
        result = super().__add__(other)
        try:
            return self.__class__(result)
        except (ValueError, TypeError):
            return result  # Return plain int if validation fails

    def __sub__(self, other):
        result = super().__sub__(other)
        try:
            return self.__class__(result)
        except (ValueError, TypeError):
            return result

    def __mul__(self, other):
        result = super().__mul__(other)
        try:
            return self.__class__(result)
        except (ValueError, TypeError):
            return result

    def __truediv__(self, other):
        result = super().__truediv__(other)
        return Safe_Float(result)