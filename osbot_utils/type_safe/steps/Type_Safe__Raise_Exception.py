from typing import Any

from osbot_utils.type_safe.steps.Type_Safe__Validation import IMMUTABLE_TYPES


class Type_Safe__Raise_Exception:

    def type_mismatch_error(self, var_name: str, expected_type: Any, actual_value: Any) -> None:  # Raises formatted error for type validation failures
        exception_message = f"variable '{var_name}' is defined as type '{expected_type}' but has value '{actual_value}' of type '{type(actual_value)}'"
        raise ValueError(exception_message)

    def immutable_type_error(self, var_name, var_type):
        exception_message = f"variable '{var_name}' is defined as type '{var_type}' which is not supported by Type_Safe, with only the following immutable types being supported: '{IMMUTABLE_TYPES}'"
        raise ValueError(exception_message)

type_safe_raise_exception = Type_Safe__Raise_Exception()