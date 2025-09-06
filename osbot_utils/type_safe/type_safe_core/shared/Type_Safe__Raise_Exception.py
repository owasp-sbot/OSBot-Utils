from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Shared__Variables import IMMUTABLE_TYPES


class Type_Safe__Raise_Exception:

    def type_mismatch_error__on_instance(self, _self, var_name: str, expected_type: type, actual_type: type) -> None:                               # Raises formatted error for type validation failures
        exception_message = f"On {_self.__class__.__name__}, invalid type for attribute '{var_name}'. Expected '{expected_type}' but got '{actual_type}'"
        raise ValueError(exception_message) from None

    def type_mismatch_error__on_type(self, cls, var_name: str, expected_type: type, actual_type: type) -> None:                               # Raises formatted error for type validation failures
        exception_message = f"On {cls.__name__}, invalid type for attribute '{var_name}'. Expected '{expected_type}' but got '{actual_type}'"
        raise ValueError(exception_message) from None

    def immutable_type_error(self, var_name, var_type):
        exception_message = f"variable '{var_name}' is defined as type '{var_type}' which is not supported by Type_Safe, with only the following immutable types being supported: '{IMMUTABLE_TYPES}' and the following subclasses (int, float, str)"
        raise ValueError(exception_message) from None

type_safe_raise_exception = Type_Safe__Raise_Exception()