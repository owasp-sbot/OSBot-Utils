from enum                                                             import Enum
from typing                                                           import Type
from osbot_utils.testing.__                                           import __
from osbot_utils.type_safe.Type_Safe__Base                            import Type_Safe__Base
from osbot_utils.type_safe.Type_Safe__Primitive                       import Type_Safe__Primitive
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List import Type_Safe__List
from osbot_utils.utils.Objects                                        import class_full_name, serialize_to_dict


class Type_Safe__Dict(Type_Safe__Base, dict):
    expected_key_type   : Type = None                                                                          # Class-level defaults
    expected_value_type : Type = None

    def __init__(self, expected_key_type=None, expected_value_type=None, initial_data=None, **kwargs):
        super().__init__()                                                                              # Initialize empty dict first


        if isinstance(expected_key_type, dict) and expected_value_type is None:                                 # Smart detection: if expected_key_type is a dict and expected_value_type is None, then the user is trying to pass initial data in the old style
            initial_data      = expected_key_type                                                               # They're using the pattern: Hash_Mapping({'key': 'value'})
            expected_key_type = None                                                                            # Move the dict to initial_data

        self.expected_key_type   = expected_key_type   or self.__class__.expected_key_type                      # Use provided types, or fall back to class-level attributes
        self.expected_value_type = expected_value_type or self.__class__.expected_value_type

        if self.expected_key_type is None or self.expected_value_type is None:                                  # Validate that we have types set (either from args or class)
            raise ValueError(f"{self.__class__.__name__} requires expected_key_type and expected_value_type")

        if initial_data is not None:                                                                            # Process initial data through our type-safe __setitem__
            if not isinstance(initial_data, dict):
                raise TypeError(f"Initial data must be a dict, got {type(initial_data).__name__}")
            for key, value in initial_data.items():
                self[key] = value                                                                               # Goes through __setitem__ with validation

        for key, value in kwargs.items():                                                                       # Also handle keyword arguments (e.g., Hash_Mapping(key1='val1', key2='val2'))
            self[key] = value

    def __contains__(self, key):
        if super().__contains__(key):                                       # First try direct lookup
            return True

        try:                                                                # Then try with type conversion
            converted_key = self.try_convert(key, self.expected_key_type)
            return super().__contains__(converted_key)
        except (ValueError, TypeError):
            return False

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

    # todo: this method needs to be refactored into smaller parts, it is getting to complex:
    #         the use of the inner method serialize_value
    #         the circular dependency on Type_Safe
    #         the inner for loops to handle nested dictionaries
    #         the enum edges cases (like the nested dictionaries case)
    #         .
    #         good news is that we have tons of tests and edge cases detection (so we should be able to do this
    #         refactoring with no side effects
    def json(self):                                                                     # Recursively serialize values, handling nested structures
        from osbot_utils.type_safe.Type_Safe import Type_Safe                           # needed here due to circular dependencies

        def serialize_value(v):
            if isinstance(v, Type_Safe):
                return v.json()
            elif isinstance(v, Type_Safe__Primitive):
                return v.__to_primitive__()
            elif isinstance(v, type):
                return class_full_name(v)
            elif isinstance(v, dict):
                return {                                                                            # Recursively handle nested dictionaries (with enum support)
                            (k2.value if isinstance(k2, Enum) else k2): serialize_value(v2)
                            for k2, v2 in v.items()
                        }
                #return {k2: serialize_value(v2) for k2, v2 in v.items()}                            # Recursively handle nested dictionaries
            elif isinstance(v, (list, tuple, set, frozenset)):
                serialized = [serialize_value(item) for item in v]                                  # Recursively handle sequences
                if isinstance(v, list):
                    return serialized
                elif isinstance(v, tuple):
                    return tuple(serialized)
                else:  # set
                    return set(serialized)
            else:
                return serialize_to_dict(v)                             # Use serialize_to_dict for unknown types (so that we don't return a non json object)


        result = {}
        for key, value in self.items():
            if isinstance(key, (type, Type)):                           # Handle Type objects as keys
                key = f"{key.__module__}.{key.__name__}"
            elif isinstance(key, Enum):                                 #  Handle Enum keys
                key = key.value
            elif isinstance(key, Type_Safe__Primitive):
                key = key.__to_primitive__()

            result[key] = serialize_value(value)                        # Use recursive serialization for values

        return result

    def get(self, key, default=None):       # this makes it consistent with the modified behaviour of __get__item
        try:
            return self[key]                # Use __getitem__ with conversion
        except KeyError:
            return default                  # Return default instead of raising

    def keys(self) -> Type_Safe__List:
        return Type_Safe__List(self.expected_key_type, super().keys())

    def obj(self) -> __:
        from osbot_utils.testing.__helpers import dict_to_obj
        return dict_to_obj(self.json())

    def values(self) -> Type_Safe__List:
        return Type_Safe__List(self.expected_value_type, super().values())

    def update(self, other=None, **kwargs):
        """Override update to ensure type safety through __setitem__"""
        # Handle dict-like object or iterable of key-value pairs
        if other is not None:
            if hasattr(other, 'items'):
                # Dict-like object
                for key, value in other.items():
                    self[key] = value  # Goes through __setitem__
            else:
                # Iterable of (key, value) pairs
                for key, value in other:
                    self[key] = value

        # Handle keyword arguments
        for key, value in kwargs.items():
            self[key] = value
