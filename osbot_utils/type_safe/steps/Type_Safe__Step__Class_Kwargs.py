import types

import functools
import inspect
from enum                       import EnumMeta
from typing                     import Dict, Any, Type, get_origin, Annotated, get_args
from osbot_utils.utils.Objects  import obj_is_type_union_compatible

IMMUTABLE_TYPES = (bool, int, float, complex, str, tuple, frozenset, bytes, types.NoneType, EnumMeta, type)

class Type_Safe__Step__Class_Kwargs:                                      # Cache for class-level keyword arguments and related information."""


    def get_cls_kwargs(self, cls: Type, include_base_classes: bool = True) -> Dict[str, Any]:

        kwargs = {}
        if not hasattr(cls, '__mro__'):
            return kwargs
        for base_cls in inspect.getmro(cls):
            if base_cls is object:                                                      # Skip the base 'object' class
                continue
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

            if hasattr(base_cls,'__annotations__'):  # can only do type safety checks if the class does not have annotations
                for var_name, var_type in base_cls.__annotations__.items():
                    if hasattr(base_cls, var_name) is False:                                # only add if it has not already been defined
                        if var_name in kwargs:
                            continue
                        var_value = cls.__default__value__(var_type)
                        kwargs[var_name] = var_value
                    else:
                        var_value = getattr(base_cls, var_name)
                        if var_value is not None:                                                                   # allow None assignments on ctor since that is a valid use case
                            if get_origin(var_type) is Annotated:
                                continue
                            if get_origin(var_type) is type:  # Special handling for Type[T]
                                if not isinstance(var_value, type):
                                    exception_message = f"variable '{var_name}' is defined as Type[T] but has value '{var_value}' which is not a type"
                                    raise ValueError(exception_message)
                                type_arg = get_args(var_type)[0]
                                if not issubclass(var_value, type_arg):
                                    exception_message = f"variable '{var_name}' is defined as {var_type} but value {var_value} is not a subclass of {type_arg}"
                                    raise ValueError(exception_message)
                            elif var_type and not isinstance(var_value, var_type):                                    # check type
                                exception_message = f"variable '{var_name}' is defined as type '{var_type}' but has value '{var_value}' of type '{type(var_value)}'"
                                raise ValueError(exception_message)
                            if var_type not in IMMUTABLE_TYPES and var_name.startswith('__') is False:              # if var_type is not one of the IMMUTABLE_TYPES or is an __ internal
                                #todo: fix type safety bug that I believe is caused here
                                if obj_is_type_union_compatible(var_type, IMMUTABLE_TYPES) is False:                # if var_type is not something like Optional[Union[int, str]]
                                    if type(var_type) not in IMMUTABLE_TYPES:
                                        exception_message = f"variable '{var_name}' is defined as type '{var_type}' which is not supported by Type_Safe, with only the following immutable types being supported: '{IMMUTABLE_TYPES}'"
                                        raise ValueError(exception_message)
            if include_base_classes is False:
                break
        return kwargs

# Create singleton instance
type_safe_step_class_kwargs = Type_Safe__Step__Class_Kwargs()