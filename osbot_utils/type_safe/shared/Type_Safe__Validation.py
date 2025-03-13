import collections
import inspect
import types
import typing
from enum                                                           import EnumMeta
from typing                                                         import Any, Annotated, Optional, get_args, get_origin, ForwardRef, Type, Dict, _GenericAlias
from osbot_utils.type_safe.shared.Type_Safe__Annotations            import type_safe_annotations
from osbot_utils.type_safe.shared.Type_Safe__Cache                  import type_safe_cache
from osbot_utils.type_safe.shared.Type_Safe__Shared__Variables      import IMMUTABLE_TYPES
from osbot_utils.type_safe.shared.Type_Safe__Raise_Exception        import type_safe_raise_exception

class Type_Safe__Validation:

    def are_types_compatible_for_assigment(self, source_type, target_type):
        import types
        import typing

        if isinstance(target_type, str):                                    # If the "target_type" is a forward reference (string), handle it here.
            if target_type == source_type.__name__:                         # Simple check: does the string match the actual class name
                return True
        if source_type is target_type:
            return True
        if source_type is int and target_type is float:
            return True
        if target_type in source_type.__mro__:                              # this means that the source_type has the target_type has of its base types
            return True
        if target_type is callable:                                         # handle case where callable was used as the target type
            if source_type is types.MethodType:                             #     and a method or function was used as the source type
                return True
            if source_type is types.FunctionType:
                return True
            if source_type is staticmethod:
                return True
        if target_type is typing.Any:
            return True
        return False

    def are_types_magic_mock(self, source_type, target_type):
        from unittest.mock import MagicMock
        if isinstance(source_type, MagicMock):
            return True
        if isinstance(target_type, MagicMock):
            return True
        if source_type is MagicMock:
            return True
        if target_type is MagicMock:
            return True
        # if class_full_name(source_type) == 'unittest.mock.MagicMock':
        #     return True
        # if class_full_name(target_type) == 'unittest.mock.MagicMock':
        #     return True
        return False

    def obj_is_type_union_compatible(self, var_type, compatible_types):
        from typing import Union

        origin = get_origin(var_type)
        if isinstance(var_type, _GenericAlias) and origin is type:              # Add handling for Type[T]
            return type in compatible_types                                     # Allow if 'type' is in compatible types
        if origin is Union:                                                     # For Union types, including Optionals
            args = get_args(var_type)                                           # Get the argument types
            for arg in args:                                                    # Iterate through each argument in the Union
                if not (arg in compatible_types or arg is type(None)):          # Check if the argument is either in the compatible_types or is type(None)
                    return False                                                # If any arg doesn't meet the criteria, return False immediately
            return True                                                         # If all args are compatible, return True
        return var_type in compatible_types or var_type is type(None)           # Check for direct compatibility or type(None) for non-Union types


    def check_if__type_matches__obj_annotation__for_union_and_annotated(self, target   : Any    ,    # Target object to check
                                                                             attr_name : str    ,    # Attribute name
                                                                             value     : Any    )\
                                                                     -> Optional[bool]:          # Returns None if no match

        from osbot_utils.helpers.python_compatibility.python_3_8 import Annotated
        from typing                                              import Union, get_origin, get_args

        value_type           = type(value)
        attribute_annotation = type_safe_annotations.obj_attribute_annotation(target, attr_name)
        origin               = get_origin(attribute_annotation)

        if origin is Union:
            return self.check_if__type_matches__union_type(attribute_annotation, value_type)

        if origin is Annotated:
            return self.check_if__type_matches__annotated_type(attribute_annotation, value)

        return None

    def check_if__value_is__special_generic_alias(self, value):
        from typing import _SpecialGenericAlias                                     # todo see if there is a better way to do this since typing is showing as not having _SpecialGenericAlias (this is to handle case like List, Dict, etc...)
        return value is not None and type(value) is not _SpecialGenericAlias

    def check_if__type_matches__union_type(self, annotation : Any,                                      # Union type annotation
                                                 value_type : Type
                                           )               -> bool:                                     # True if type matches
        from typing import get_args
        args = get_args(annotation)
        return value_type in args

    def check_if__type_matches__annotated_type(self, annotation : Any,                                  # Annotated type annotation
                                                     value      : Any                                   # Value to check
                                               )               -> bool:                                 # True if type matches
        from typing import get_args, get_origin
        from typing import List, Dict, Tuple

        args        = get_args(annotation)
        base_type   = args[0]                                                        # First argument is base type
        base_origin = get_origin(base_type)

        if base_origin is None:                                                      # Handle non-container types
            return isinstance(value, base_type)

        if base_origin in (list, List):                                             # Handle List types
            return self.check_if__type_matches__list_type(value, base_type)

        if base_origin in (tuple, Tuple):                                           # Handle Tuple types
            return self.check_if__type_matches__tuple_type(value, base_type)

        if base_origin in (dict, Dict):                                             # Handle Dict types
            return self.check_if__type_matches_dict_type(value, base_type)

        return False

    def check_if__type_matches__list_type(self, value     : Any,                                    # Value to check
                                                base_type : Any                                     # List base type
                                          )              -> bool:                                   # True if valid list type
        if not isinstance(value, list):
            return False

        item_type = get_args(base_type)[0]
        return all(isinstance(item, item_type) for item in value)

    def check_if__type_matches__tuple_type(self, value     : Any,                                    # Value to check
                                                 base_type : Any                                     # Tuple base type
                                           )               -> bool:                                  # True if valid tuple type
        if not isinstance(value, tuple):
            return False

        item_types = get_args(base_type)
        return len(value) == len(item_types) and all(
            isinstance(item, item_type)
            for item, item_type in zip(value, item_types)
        )

    def check_if__type_matches_dict_type(self, value    : Any,  # Value to check
                                               base_type : Any  # Dict base type
                                         )              -> bool:                                   # True if valid dict type
        if not isinstance(value, dict):
            return False

        key_type, value_type = get_args(base_type)
        return all(isinstance(k, key_type) and isinstance(v, value_type)
                  for k, v in value.items())                                                        # if it is not a Union or Annotated types just return None (to give an indication to the caller that the comparison was not made)

    def check_if__type_matches__obj_annotation__for_attr(self, target, attr_name, value) -> Optional[bool]:
        annotations = type_safe_cache.get_obj_annotations(target)
        attr_type   = annotations.get(attr_name)
        if attr_type:
            origin_attr_type = get_origin(attr_type)                                    # to handle when type definition contains a generic

            if origin_attr_type is collections.abc.Callable:                            # Handle Callable types
                return self.is_callable_compatible(value, attr_type)                    # ISSUE: THIS IS NEVER CALLED

            if origin_attr_type is set:
                if type(value) is list:
                    return True                                                         # if the attribute is a set and the value is a list, then they are compatible
            if origin_attr_type is type:                                                # Add handling for Type[T]
                type_args = get_args(attr_type)
                if type_args:
                    type_arg = get_args(attr_type)[0]                                       # Get T from Type[T]
                    if type_arg == value:
                        return True
                    if isinstance(type_arg, (str, ForwardRef)):                             # Handle forward reference
                        type_arg = target.__class__                                         # If it's a forward reference, the target class should be the containing class
                    return isinstance(value, type) and issubclass(value, type_arg)          # Check that value is a type and is subclass of type_arg
                else:
                    return isinstance(value, type)

            if origin_attr_type is Annotated:                                           # if the type is Annotated
                args             = get_args(attr_type)
                origin_attr_type = args[0]

            elif origin_attr_type is typing.Union:
                args = get_args(attr_type)
                if len(args)==2 and args[1] is type(None):          # todo: find a better way to do this, since this is handling an edge case when origin_attr_type is Optional (which is an shorthand for Union[X, None] )
                    attr_type = args[0]
                    origin_attr_type = get_origin(attr_type)

            if origin_attr_type:
                attr_type = origin_attr_type
            value_type = type(value)
            if type_safe_validation.are_types_compatible_for_assigment(source_type=value_type, target_type=attr_type):
                return True
            if type_safe_validation.are_types_magic_mock(source_type=value_type, target_type=attr_type):
                return True
            return value_type is attr_type
        return None

    def is_callable_compatible(self, value, expected_type) -> bool:
        if not callable(value):
            return False

        expected_args = get_args(expected_type)
        if not expected_args:                                                                                   # Callable without type hints
            return True

        if len(expected_args) != 2:                                                                             # Should have args and return type
            return False

        expected_param_types = expected_args[0]                                                                 # First element is tuple of parameter types
        expected_return_type = expected_args[1]                                                                 # Second element is return type


        try:                                                                                                    # Get the signature of the actual value
            sig = inspect.signature(value)
        except ValueError:                                                                                      # Some built-in functions don't support introspection
            return True

        actual_params = list(sig.parameters.values())                                                           # Get actual parameters

        if len(actual_params) != len(expected_param_types):                                                     # Check number of parameters matches
            return False

        for actual_param, expected_param_type in zip(actual_params, expected_param_types):                      # Check each parameter type
            if actual_param.annotation != inspect.Parameter.empty:
                if not self.are_types_compatible_for_assigment(actual_param.annotation, expected_param_type):
                    return False                                                                                # todo: check if we shouldn't raise an exception here, since this is the only place where we actually know the types that don't match in the method signature

        if sig.return_annotation != inspect.Parameter.empty:                                                    # Check return type
            if not self.are_types_compatible_for_assigment(sig.return_annotation, expected_return_type):
                return False                                                                                    # todo: check if we shouldn't raise an exception here, since this is the only place where we actually know the types that don't match in the method return type

        return True

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

    def validate_if_value_has_been_set(self, _self, annotations, name, value):
        if hasattr(_self, name) and annotations.get(name) :     # don't allow previously set variables to be set to None
            if getattr(_self, name) is not None:                         # unless it is already set to None
                raise ValueError(f"Can't set None, to a variable that is already set. Invalid type for attribute '{name}'. Expected '{_self.__annotations__.get(name)}' but got '{type(value)}'")

    def validate_if__types_are_compatible_for_assigment(self, name, current_type, expected_type):
        if not type_safe_validation.are_types_compatible_for_assigment(current_type, expected_type):
            type_safe_raise_exception.type_mismatch_error(name, expected_type, current_type)

    def validate_type_compatibility(self, target      : Any             ,             # Target object to validate
                                          annotations : Dict[str, Any]  ,             # Type annotations
                                          name        : str             ,             # Attribute name
                                          value       : Any                           # Value to validate
                                   )                 -> None:                                           # Raises ValueError if invalid

        direct_type_match = type_safe_validation.check_if__type_matches__obj_annotation__for_attr(target, name, value)
        union_type_match  = type_safe_validation.check_if__type_matches__obj_annotation__for_union_and_annotated(target, name, value)

        is_invalid = (direct_type_match is False and union_type_match is None ) or \
                     (direct_type_match is None  and union_type_match is False) or \
                     (direct_type_match is False and union_type_match is False)

        if is_invalid:
            expected_type = annotations.get(name)
            if type(value) is type:
                actual_type = value
            else:
                actual_type = type(value)
            raise ValueError(f"Invalid type for attribute '{name}'. Expected '{expected_type}' but got '{actual_type}'")

    # todo: see if need to add cache support to this method     (it looks like this method is not called very often)
    def validate_type_immutability(self, var_name: str, var_type: Any) -> None:                         # Validates that type is immutable or in supported format
        if var_type not in IMMUTABLE_TYPES and var_name.startswith('__') is False:                      # if var_type is not one of the IMMUTABLE_TYPES or is an __ internal
            if self.obj_is_type_union_compatible(var_type, IMMUTABLE_TYPES) is False:                        # if var_type is not something like Optional[Union[int, str]]
                if var_type not in IMMUTABLE_TYPES or type(var_type) not in IMMUTABLE_TYPES:
                    if not isinstance(var_type, EnumMeta):
                        if not issubclass(var_type, str):
                            type_safe_raise_exception.immutable_type_error(var_name, var_type)

    def validate_variable_type(self, var_name, var_type, var_value):                                # Validate type compatibility
        if type(var_type) is type and not isinstance(var_value, var_type):
            type_safe_raise_exception.type_mismatch_error(var_name, var_type, type(var_value))

type_safe_validation = Type_Safe__Validation()
