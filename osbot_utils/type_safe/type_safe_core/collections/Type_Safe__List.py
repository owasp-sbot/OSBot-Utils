from enum                                       import Enum
from typing                                     import Type
from osbot_utils.utils.Objects                  import class_full_name, serialize_to_dict
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive
from osbot_utils.type_safe.Type_Safe__Base      import Type_Safe__Base, type_str



class Type_Safe__List(Type_Safe__Base, list):
    expected_type : Type

    def __init__(self, expected_type, *args):
        super().__init__(*args)
        self.expected_type = expected_type

    def __contains__(self, item):
        if super().__contains__(item):                                                                                          # First try direct lookup
            return True

        if type(self.expected_type) is type and issubclass(self.expected_type, Type_Safe__Primitive):                           # Handle Type_Safe__Primitive conversions
            try:
                converted_item = self.expected_type(item)
                return super().__contains__(converted_item)
            except (ValueError, TypeError):
                return False


        if hasattr(self.expected_type, '__bases__') and any(base.__name__ == 'Enum' for base in self.expected_type.__bases__):  # Handle Enums (reusing logic from append)
            if isinstance(item, str):
                if item in self.expected_type.__members__:
                    converted_item = self.expected_type[item]
                    return super().__contains__(converted_item)
                elif hasattr(self.expected_type, '_value2member_map_') and item in self.expected_type._value2member_map_:
                    converted_item = self.expected_type._value2member_map_[item]
                    return super().__contains__(converted_item)

        return False

    def __repr__(self):
        expected_type_name = type_str(self.expected_type)
        return f"list[{expected_type_name}] with {len(self)} elements"

    def __enter__(self): return self
    def __exit__ (self, type, value, traceback): pass

    def append(self, item):
        from osbot_utils.type_safe.Type_Safe        import Type_Safe                                                                    # to prevent circular imports

        if type(self.expected_type) is type and issubclass(self.expected_type, Type_Safe) and type(item) is dict:                       # Handle Type_Safe objects from dicts
            item = self.expected_type.from_json(item)
        elif type(self.expected_type) is type and issubclass(self.expected_type, Type_Safe__Primitive):                                 # Handle Type_Safe__Primitive conversions (str -> Safe_Str, etc.)
            if not isinstance(item, self.expected_type):
                try:
                    item = self.expected_type(item)
                except (ValueError, TypeError) as e:
                    # Re-raise with more context about what failed
                    raise TypeError(f"In Type_Safe__List: Could not convert {type(item).__name__} to {self.expected_type.__name__}: {e}") from None

        elif hasattr(self.expected_type, '__bases__') and any(base.__name__ == 'Enum' for base in self.expected_type.__bases__):        # Handle Enums

            if isinstance(self.expected_type, type) and issubclass(self.expected_type, Enum):
                if isinstance(item, str):
                    if item in self.expected_type.__members__:                                                                          # Try to convert string to enum
                        item = self.expected_type[item]
                    elif hasattr(self.expected_type, '_value2member_map_') and item in self.expected_type._value2member_map_:
                        item = self.expected_type._value2member_map_[item]

        try:                                                                                                                            # Now validate the (possibly converted) item
            self.is_instance_of_type(item, self.expected_type)
        except TypeError as e:
            raise TypeError(f"In Type_Safe__List: Invalid type for item: {e}") from None

        super().append(item)


    def json(self): # Convert the list to a JSON-serializable format.
        from osbot_utils.type_safe.Type_Safe import Type_Safe                           # Import here to avoid circular imports

        result = []
        for item in self:
            if isinstance(item, Type_Safe):
                result.append(item.json())
            elif isinstance(item, Type_Safe__Primitive):
                result.append(item.__to_primitive__())
            elif isinstance(item, (list, tuple, frozenset)):
                result.append([x.json() if isinstance(x, Type_Safe) else serialize_to_dict(x) for x in item])
                #result.append([x.json() if isinstance(x, Type_Safe) else x for x in item])      # BUG here
            elif isinstance(item, dict):
                result.append(serialize_to_dict(item))          # leverage serialize_to_dict since that method already knows how to handle
                #result.append({k: v.json() if isinstance(v, Type_Safe) else v for k, v in item.items()})
            elif isinstance(item, type):
                result.append(class_full_name(item))
            else:
                result.append(serialize_to_dict(item))          # also Use serialize_to_dict for unknown types (so that we don't return a non json object)
        return result