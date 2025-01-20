import types
from enum                                                       import EnumMeta
from typing                                                     import Any, Annotated
from osbot_utils.type_safe.shared.Type_Safe__Cache              import type_safe_cache
from osbot_utils.type_safe.shared.Type_Safe__Shared__Variables  import IMMUTABLE_TYPES
from osbot_utils.utils.Objects                                  import obj_is_type_union_compatible
from osbot_utils.type_safe.shared.Type_Safe__Raise_Exception    import type_safe_raise_exception


class Type_Safe__Validation:

    # todo: add cache support to this method
    def should_skip_type_check(self, var_type):                                                         # Determine if type checking should be skipped
        origin = type_safe_cache.get_origin(var_type)                                                   # Use cached get_origin
        return (origin is Annotated or
                origin is type        )

    def should_skip_var(self, var_name: str, var_value: Any) -> bool:                                   # Determines if variable should be skipped during MRO processing
        if var_name.startswith('__'):                                                                   # skip internal variables
            return True
        if isinstance(var_value, types.FunctionType):                                                   # skip instance functions
            return True
        if isinstance(var_value, classmethod):                                                          # skip class methods
            return True
        if isinstance(var_value, property):                                                             # skip property descriptors
            return True
        return False

    # todo: see if need to add cache support to this method     (it looks like this method is not called very often)
    def validate_type_immutability(self, var_name: str, var_type: Any) -> None:                         # Validates that type is immutable or in supported format
        if var_type not in IMMUTABLE_TYPES and var_name.startswith('__') is False:                      # if var_type is not one of the IMMUTABLE_TYPES or is an __ internal
            if obj_is_type_union_compatible(var_type, IMMUTABLE_TYPES) is False:                        # if var_type is not something like Optional[Union[int, str]]
                if var_type not in IMMUTABLE_TYPES or type(var_type) not in IMMUTABLE_TYPES:
                    if not isinstance(var_type, EnumMeta):
                        type_safe_raise_exception.immutable_type_error(var_name, var_type)

    def validate_variable_type(self, var_name, var_type, var_value):                                # Validate type compatibility
        if var_type and not isinstance(var_value, var_type):
            type_safe_raise_exception.type_mismatch_error(var_name, var_type, var_value)

type_safe_validation = Type_Safe__Validation()
