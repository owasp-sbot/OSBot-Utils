from typing import get_origin, get_args, Union, Optional, Any, ForwardRef

EXACT_TYPE_MATCH = (int, float, str, bytes, bool, complex)

class Type_Safe__Base:
    def is_instance_of_type(self, item, expected_type):
        if expected_type is Any:
            return True
        if isinstance(expected_type, ForwardRef):               # todo: add support for ForwardRef
            return True
        origin = get_origin(expected_type)
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

        elif origin is list and args:                                                    # Expected type is List[...]
            (item_type,) = args
            if not isinstance(item, list):
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
        else:
            if isinstance(item, origin):
                return True
            else:
                expected_type_name = type_str(expected_type)
                actual_type_name = type_str(type(item))
                raise TypeError(f"Expected '{expected_type_name}', but got '{actual_type_name}'")

# todo: see if we should/can move this to the Objects.py file
def type_str(tp):
    origin = get_origin(tp)
    if origin is None:
        if hasattr(tp, '__name__'):
            return tp.__name__
        else:
            return str(tp)
    else:
        args = get_args(tp)
        args_str = ', '.join(type_str(arg) for arg in args)
        return f"{origin.__name__}[{args_str}]"

def get_object_type_str(obj):
    if isinstance(obj, dict):
        if not obj:
            return "Dict[Empty]"
        key_types      = set(type(k).__name__ for k in obj.keys())
        value_types    = set(type(v).__name__ for v in obj.values())
        key_type_str   = ', '.join(sorted(key_types))
        value_type_str = ', '.join(sorted(value_types))
        return f"Dict[{key_type_str}, {value_type_str}]"
    elif isinstance(obj, list):
        if not obj:
            return "List[Empty]"
        elem_types = set(type(e).__name__ for e in obj)
        elem_type_str = ', '.join(sorted(elem_types))
        return f"List[{elem_type_str}]"
    else:
        return type(obj).__name__