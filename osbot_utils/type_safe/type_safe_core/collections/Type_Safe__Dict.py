from typing                                                           import Type

from osbot_utils.testing.__ import __
from osbot_utils.type_safe.Type_Safe__Base                            import Type_Safe__Base
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List import Type_Safe__List
from osbot_utils.utils.Objects import dict_to_obj


class Type_Safe__Dict(Type_Safe__Base, dict):
    def __init__(self, expected_key_type, expected_value_type, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.expected_key_type   = expected_key_type
        self.expected_value_type = expected_value_type

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)                                     # First try direct lookup
        except KeyError:
            converted_key = self.try_convert(key, self.expected_key_type)       # Try converting the key
            return super().__getitem__(converted_key)                           # and compare again

    def __setitem__(self, key, value):                                          # Check type-safety before allowing assignment.
        key   = self.try_convert(key  , self.expected_key_type  )
        value = self.try_convert(value, self.expected_value_type)
        self.is_instance_of_type(key  , self.expected_key_type)
        self.is_instance_of_type(value, self.expected_value_type)
        super().__setitem__(key, value)

    def __enter__(self): return self
    def __exit__ (self, type, value, traceback): pass

    def json(self):
        from osbot_utils.type_safe.Type_Safe import Type_Safe

        def serialize_value(v):
            """Recursively serialize values, handling nested structures"""
            if isinstance(v, Type_Safe):
                return v.json()
            elif isinstance(v, Type_Safe__Primitive):
                return v.__to_primitive__()
            elif isinstance(v, dict):
                # Recursively handle nested dictionaries
                return {k2: serialize_value(v2) for k2, v2 in v.items()}
            elif isinstance(v, (list, tuple, set)):
                # Recursively handle sequences
                serialized = [serialize_value(item) for item in v]
                if isinstance(v, list):
                    return serialized
                elif isinstance(v, tuple):
                    return tuple(serialized)
                else:  # set
                    return set(serialized)
            else:
                return v

        result = {}
        for key, value in self.items():
            # Handle Type objects as keys
            if isinstance(key, (type, Type)):
                key = f"{key.__module__}.{key.__name__}"
            elif isinstance(key, Type_Safe__Primitive):
                key = key.__to_primitive__()

            # Use recursive serialization for values
            result[key] = serialize_value(value)

        return result

    def get(self, key, default=None):       # this makes it consistent with the modified behaviour of __get__item
        try:
            return self[key]                # Use __getitem__ with conversion
        except KeyError:
            return default                  # Return default instead of raising

    def keys(self) -> Type_Safe__List:
        return Type_Safe__List(self.expected_key_type, super().keys())

    def obj(self) -> __:
        return dict_to_obj(self.json())

    def values(self) -> Type_Safe__List:
        return Type_Safe__List(self.expected_value_type, super().values())