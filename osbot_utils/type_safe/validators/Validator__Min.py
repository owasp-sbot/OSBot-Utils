from typing                                             import Any
from osbot_utils.type_safe.validators.Type_Safe__Validator import Type_Safe__Validator

class Validator__Min(Type_Safe__Validator):                     # Validates that a value is at least the specified minimum. Works with any type that supports the < operator (numbers, strings, lists, etc.)
    min_value: Any

    def __init__(self, min_value):
        super().__init__()
        self.min_value = min_value

    def validate(self, value: Any, field_name: str, target_type: type) -> None:
        super().validate(value=value, field_name=field_name, target_type=target_type)
        if value is None:                                                               # can't compare if value has been set to None
            return

        try:
            compare_value = value if isinstance(value, (int, float)) else len(value)

            if compare_value < self.min_value:
                if isinstance(value, (int, float)):
                    msg = f"{field_name} must be at least {self.min_value}, got {compare_value}"
                elif isinstance(value, str):
                    msg = f"{field_name} must have length at least {self.min_value}, got length {compare_value}"
                elif isinstance(value, (list, tuple)):
                    msg = f"{field_name} must have length at least {self.min_value}, got length {compare_value}"
                else:
                    msg = f"{field_name} must have size at least {self.min_value}, got size {compare_value}"
                raise ValueError(msg)
        except TypeError:
            raise ValueError(f"Cannot compare {field_name} of type {type(value)} with minimum value of type {type(self.min_value)}")

    def describe(self) -> str:
        if isinstance(self.min_value, (int, float)):
            return f"minimum value: {self.min_value}"
        else:
            return f"minimum length: {len(self.min_value)}"

Min = Validator__Min