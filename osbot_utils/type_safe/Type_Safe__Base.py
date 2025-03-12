import types
from typing                                         import get_args, Union, Optional, Any, ForwardRef
from osbot_utils.helpers.Obj_Id                     import Obj_Id
from osbot_utils.type_safe.shared.Type_Safe__Cache  import type_safe_cache

EXACT_TYPE_MATCH = (int, float, str, bytes, bool, complex)

class Type_Safe__Base:
    def is_instance_of_type(self, item, expected_type):
        if expected_type is Any:
            return True
        if isinstance(expected_type, ForwardRef):               # todo: add support for ForwardRef
            return True
        origin = type_safe_cache.get_origin(expected_type)
        args   = get_args(expected_type)
        if origin is None:
            if expected_type in EXACT_TYPE_MATCH:
                if type(item) is expected_type:
                    return True
                else:
                    expected_type_name = type_str(expected_type)
                    actual_type_name = type_str(type(item))
                    raise TypeError(f"Expected '{expected_type_name}', but got '{actual_type_name}'")
            else:
                if isinstance(item, expected_type):                                 # Non-parameterized type
                    return True
                else:
                    expected_type_name = type_str(expected_type)
                    actual_type_name   = type_str(type(item))
                    raise TypeError(f"Expected '{expected_type_name}', but got '{actual_type_name}'")

        elif origin in (list, set) and args:                                                    # Expected type is List[...]
            (item_type,) = args
            if not isinstance(item, (list,set)):
                expected_type_name = type_str(expected_type)
                actual_type_name   = type_str(type(item))
                raise TypeError(f"Expected '{expected_type_name}', but got '{actual_type_name}'")
            for idx, elem in enumerate(item):
                try:
                    self.is_instance_of_type(elem, item_type)
                except TypeError as e:
                    raise TypeError(f"In list at index {idx}: {e}")
            return True
        elif origin is dict and args:                                                    # Expected type is Dict[...]
            key_type, value_type = args
            if not isinstance(item, dict):
                expected_type_name = type_str(expected_type)
                actual_type_name   = type_str(type(item))
                raise TypeError(f"Expected '{expected_type_name}', but got '{actual_type_name}'")
            for k, v in item.items():
                try:
                    self.is_instance_of_type(k, key_type)
                except TypeError as e:
                    raise TypeError(f"In dict key '{k}': {e}")
                try:
                    self.is_instance_of_type(v, value_type)
                except TypeError as e:
                    raise TypeError(f"In dict value for key '{k}': {e}")
            return True
        elif origin is tuple:
            if not isinstance(item, tuple):
                expected_type_name = type_str(expected_type)
                actual_type_name = type_str(type(item))
                raise TypeError(f"Expected '{expected_type_name}', but got '{actual_type_name}'")
            if len(args) != len(item):
                raise TypeError(f"Expected tuple of length {len(args)}, but got {len(item)}")
            for idx, (elem, elem_type) in enumerate(zip(item, args)):
                if elem_type is Obj_Id:                                     # todo: refactor this out, and figure out better way to handle this kind of de-serialisation
                    elem = elem_type(elem)
                try:
                    self.is_instance_of_type(elem, elem_type)
                except TypeError as e:
                    raise TypeError(f"In tuple at index {idx}: {e}")
            return True
        elif origin is Union or expected_type is Optional:                                                   # Expected type is Union[...]
            for arg in args:
                try:
                    self.is_instance_of_type(item, arg)
                    return True
                except TypeError:
                    continue
            expected_type_name = type_str(expected_type)
            actual_type_name   = type_str(type(item))
            raise TypeError(f"Expected '{expected_type_name}', but got '{actual_type_name}'")
        elif origin is type:                                            # Expected type is Type[T]
            if type(item) is str:
                item = deserialize_type__using_value(item)
            if not isinstance(item, type):                              # First check if item is actually a type
                expected_type_name = type_str(expected_type)
                actual_type_name   = type_str(type(item))
                raise TypeError(f"Expected {expected_type_name}, but got instance: {actual_type_name}")

            args = get_args(expected_type)
            if args:                                                    # Check if there are type arguments
                type_arg = args[0]                                      # Then check if item is a subclass of T
                if not issubclass(item, type_arg):
                    raise TypeError(f"Expected subclass of {type_str(type_arg)}, got {type_str(item)}")
            return True                                                 # If no args, any type is valid
        else:
            if isinstance(item, origin):
                return True
            else:
                expected_type_name = type_str(expected_type)
                actual_type_name = type_str(type(item))
                raise TypeError(f"Expected '{expected_type_name}', but got '{actual_type_name}'")

    # def json(self):
    #     pass

# todo: see if we should/can move this to the Objects.py file
def type_str(tp):
    origin = type_safe_cache.get_origin(tp)
    if origin is None:
        if hasattr(tp, '__name__'):
            return tp.__name__
        else:
            return str(tp)
    else:
        args = get_args(tp)
        args_str = ', '.join(type_str(arg) for arg in args)
        return f"{origin.__name__}[{args_str}]"

# todo: this is duplicated from Type_Safe__Step__From_Json (review and figure out how to do this more centrally)
def deserialize_type__using_value(value):         # TODO: Check the security implications of this deserialisation
    from osbot_utils.type_safe.Type_Safe import Type_Safe
    if value:
        try:
            module_name, type_name = value.rsplit('.', 1)
            if module_name == 'builtins' and type_name == 'NoneType':                       # Special case for NoneType (which serialises as builtins.* , but it actually in types.* )
                value = types.NoneType
            else:
                module = __import__(module_name, fromlist=[type_name])
                value = getattr(module, type_name)
                if isinstance(value, type) is False:
                    raise ValueError(f"Security alert, in deserialize_type__using_value only classes are allowed")
                # todo: figure out a way to do this
                # if issubclass(value, (Type_Safe, str, int))  is False:
                #     raise ValueError(f"Security alert, in deserialize_type__using_value only class of type Type_Safe, str, int are allowed")
        except (ValueError, ImportError, AttributeError) as e:
            raise ValueError(f"Could not reconstruct type from '{value}': {str(e)}")
    return value