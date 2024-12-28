from osbot_utils.helpers.python_compatibility.python_3_8 import Annotated
from typing                                              import Any

class Type_Safe__Validator:                                                                 # Base class for all Type_Safe validators.

    def validate(self, value: Any, field_name: str, target_type: type) -> None:                                # Validate a value against this validator's rules.
        if value and type(value) != target_type:
            raise ValueError(f"{field_name} must be of type {target_type}, got {type(value)}")

    def describe(self) -> str:                                                              # Return a human-readable description of this validator's rules.
        pass


Validate = Annotated
