
import sys
import inspect
import typing

from osbot_utils.utils.Objects              import default_value
from osbot_utils.type_safe.Type_Safe__List  import Type_Safe__List
from osbot_utils.type_safe.Type_Safe__Dict  import Type_Safe__Dict


# Backport implementations of get_origin and get_args for Python 3.7        # todo: refactor into separate class (focused on past python version compatibility)
if sys.version_info < (3, 8):                                           # pragma: no cover
    def get_origin(tp):
        if isinstance(tp, typing._GenericAlias):
            return tp.__origin__
        elif tp is typing.Generic:
            return typing.Generic
        else:
            return None

    def get_args(tp):
        if isinstance(tp, typing._GenericAlias):
            return tp.__args__
        else:
            return ()
else:
    from typing import get_origin, get_args, ForwardRef, Any
    from osbot_utils.helpers.python_compatibility.python_3_8 import Annotated


class Type_Safe__Step__Default_Value:

    def default_value(self, _cls, var_type):


        if get_origin(var_type) is type:                        # Special handling for Type[T]  # todo: reuse the get_origin value
            type_args = get_args(var_type)
            if type_args:
                if isinstance(type_args[0], ForwardRef):
                    forward_name = type_args[0].__forward_arg__
                    for base_cls in inspect.getmro(_cls):
                        if base_cls.__name__ == forward_name:
                            return _cls                                                      # note: in this case we return the cls, and not the base_cls (which makes sense since this happens when the cls class uses base_cls as base, which has a ForwardRef to base_cls )
                return type_args[0]                             # Return the actual type as the default value

        if var_type is typing.Set:                              # todo: refactor the dict, set and list logic, since they are 90% the same
            return set()
        if get_origin(var_type) is set:
            return set()                                        # todo: add Type_Safe__Set

        if var_type is typing.Dict:
            return {}

        if get_origin(var_type) is dict:                        # e.g. Dict[key_type, value_type]
            key_type, value_type = get_args(var_type)
            if isinstance(key_type, ForwardRef):                # Handle forward references on key_type ---
                forward_name = key_type.__forward_arg__
                if forward_name == _cls.__name__:
                    key_type = _cls
            if isinstance(value_type, ForwardRef):              # Handle forward references on value_type ---
                forward_name = value_type.__forward_arg__
                if forward_name == _cls.__name__:
                    value_type = _cls
            return Type_Safe__Dict(expected_key_type=key_type, expected_value_type=value_type)

        if var_type is typing.List:
            return []                                           # handle case when List was used with no type information provided

        if get_origin(var_type) is list:                        # if we have list defined as list[type]
            item_type = get_args(var_type)[0]                   #    get the type that was defined
            if isinstance(item_type, ForwardRef):               # handle the case when the type is a forward reference
                forward_name = item_type.__forward_arg__
                if forward_name == _cls.__name__:                #    if the forward reference is to the current class (simple name check)
                    item_type = _cls                             #       set the item_type to the current class
            return Type_Safe__List(expected_type=item_type)     #    and used it as expected_type in Type_Safe__List
        else:
            return default_value(var_type)                      # for all other cases call default_value, which will try to create a default instance


type_safe_step_default_value = Type_Safe__Step__Default_Value()