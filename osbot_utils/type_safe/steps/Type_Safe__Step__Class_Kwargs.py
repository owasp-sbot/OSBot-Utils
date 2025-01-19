import types

import functools
import inspect
from enum                                                       import EnumMeta
from typing                                                     import Dict, Any, Type, get_origin, Annotated, get_args
from osbot_utils.type_safe.steps.Type_Safe__Step__Default_Value import type_safe_step_default_value
from osbot_utils.utils.Objects                                  import obj_is_type_union_compatible

IMMUTABLE_TYPES = (bool, int, float, complex, str, tuple, frozenset, bytes, types.NoneType, EnumMeta, type)

class Type_Safe__Step__Class_Kwargs:                                      # Cache for class-level keyword arguments and related information."""

    def get_mro_classes(self, cls):
        return inspect.getmro(cls)

    def get_cls_kwargs(self, cls: Type, include_base_classes: bool = True) -> Dict[str, Any]:
        kwargs = {}
        if not hasattr(cls, '__mro__'):
            return kwargs

        for base_cls in self.get_mro_classes(cls):
            self.process_mro_class(base_cls, kwargs)
            self.process_annotations(cls, base_cls, kwargs)
            if include_base_classes is False:
                break

        return kwargs

    def base_cls_annotations(self, base_cls):
        return base_cls.__annotations__.items()

    def process_annotation(self, cls, base_cls, kwargs, var_name, var_type):
        if hasattr(base_cls, var_name) is False:                                # only add if it has not already been defined
            if var_name in kwargs:
                return
            var_value = type_safe_step_default_value.default_value(cls, var_type)
            kwargs[var_name] = var_value
        else:
            var_value = getattr(base_cls, var_name)
            if var_value is not None:                                                                   # allow None assignments on ctor since that is a valid use case
                if get_origin(var_type) is Annotated:
                    return
                if get_origin(var_type) is type:  # Special handling for Type[T]
                    pass
                elif var_type and not isinstance(var_value, var_type):                                    # check type
                    self.raise_type_mismatch_error(var_name, var_type, var_value)

                self.validate_type_immutability(var_name, var_type)

    def process_annotations(self, cls, base_cls, kwargs):
        if hasattr(base_cls,'__annotations__'):                                                         # can only do type safety checks if the class does not have annotations
            for var_name, var_type in self.base_cls_annotations(base_cls):
                self.process_annotation(cls, base_cls, kwargs, var_name, var_type)

    def process_mro_class(self, base_cls, kwargs):
        if base_cls is object:                                                                          # Skip the base 'object' class
            return
        for k, v in vars(base_cls).items():
            # todo: refactor this logic since it is weird to start with a if not..., and then if ... continue (all these should be if ... continue )
            if not k.startswith('__') and not isinstance(v, types.FunctionType):    # remove instance functions
                if isinstance(v, classmethod):                                      # also remove class methods
                    continue
                if type(v) is functools._lru_cache_wrapper:                         # todo, find better way to handle edge cases like this one (which happens when the @cache decorator is used in a instance method that uses Kwargs_To_Self)
                    continue
                if isinstance(v, property):                                         # skip property descriptors since they should not be handled here
                    continue
                if (k in kwargs) is False:                                          # do not set the value is it has already been set
                    kwargs[k] = v

    def raise_type_mismatch_error(self, var_name: str, expected_type: Any,actual_value: Any) -> None:  # Raises formatted error for type validation failures
        exception_message = f"variable '{var_name}' is defined as type '{expected_type}' but has value '{actual_value}' of type '{type(actual_value)}'"
        raise ValueError(exception_message)

    def raise_immutable_type_error(self, var_name, var_type):
        exception_message = f"variable '{var_name}' is defined as type '{var_type}' which is not supported by Type_Safe, with only the following immutable types being supported: '{IMMUTABLE_TYPES}'"
        raise ValueError(exception_message)

    def validate_type_immutability(self, var_name: str, var_type: Any) -> None:                         # Validates that type is immutable or in supported format
        if var_type not in IMMUTABLE_TYPES and var_name.startswith('__') is False:                          # if var_type is not one of the IMMUTABLE_TYPES or is an __ internal
            if obj_is_type_union_compatible(var_type, IMMUTABLE_TYPES) is False:                            # if var_type is not something like Optional[Union[int, str]]
                if var_type not in IMMUTABLE_TYPES or type(var_type) not in IMMUTABLE_TYPES:
                    if not isinstance(var_type, EnumMeta):
                        self.raise_immutable_type_error(var_name, var_type)

# Create singleton instance
type_safe_step_class_kwargs = Type_Safe__Step__Class_Kwargs()