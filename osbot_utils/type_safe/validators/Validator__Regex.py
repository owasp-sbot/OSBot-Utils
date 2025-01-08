from typing                                             import Any
from osbot_utils.type_safe.validators.Type_Safe__Validator import Type_Safe__Validator

class Validator__Regex(Type_Safe__Validator):            # Validates that a string matches the specified regex pattern.
    pattern    : str
    description: str

    def __init__(self, pattern, description=None):
        self.pattern     = pattern
        self.description = description

    def validate(self, value: Any, field_name: str, target_type:type) -> None:
        import re
        if value is None:
            return
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string, got {type(value)}")
        if not re.match(self.pattern, value):
            raise ValueError(f"{field_name} must match pattern {self.pattern}")

    def describe(self) -> str:
        if self.description:
            return self.description
        return f"must match pattern: {self.pattern}"

Regex = Validator__Regex