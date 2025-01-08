from typing                                             import Any
from osbot_utils.type_safe.validators.Type_Safe__Validator import Type_Safe__Validator


class Validator__Max(Type_Safe__Validator):                             #    Validates that a numeric value is at most the specified maximum."""
    max_value: float

    def __init__(self, max_value):
        self.max_value = max_value

    def validate(self, value: Any, field_name: str, target_type: type) -> None:
        super().validate(value=value, field_name=field_name, target_type=target_type)
        if value is None:
            return
        compare_value = value if isinstance(value, (int, float)) else len(value)
        if compare_value > self.max_value:
            if not isinstance(value, (int, float)):
                msg = f"{field_name} must be at most {self.max_value}, got {compare_value}"
            elif isinstance(value, (list, tuple)):
                msg = f"{field_name} must be at most {self.max_value}, got length {compare_value}"
            else:
                msg = f"{field_name} must be at most {self.max_value}, got size {compare_value}"
            raise ValueError(msg)

    def describe(self) -> str:
        return f"maximum value: {self.max_value}"

Max = Validator__Max