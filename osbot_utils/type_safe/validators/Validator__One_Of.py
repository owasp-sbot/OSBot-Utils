from typing                                             import Any
from osbot_utils.type_safe.validators.Type_Safe__Validator import Type_Safe__Validator


class Validator__One_Of(Type_Safe__Validator):                  # Validates that a value is one of a set of allowed values."""
    allowed: list

    def __init__(self, allowed):
        self.allowed = allowed

    def validate(self, value: Any, field_name: str, target_type:type) -> None:
        if value not in self.allowed:
            raise ValueError(f"{field_name} must be one of {self.allowed}, got {value}")

    def describe(self) -> str:
        return f"must be one of: {self.allowed}"

One_Of = Validator__One_Of