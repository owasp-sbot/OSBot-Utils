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

    def _validate_and_convert_item(self, item):     # Validate and convert an item to the expected type."
        from osbot_utils.type_safe.Type_Safe import Type_Safe

        if type(self.expected_type) is type and issubclass(self.expected_type, Type_Safe) and type(item) is dict:
            item = self.expected_type.from_json(item)
        elif type(self.expected_type) is type and issubclass(self.expected_type, Type_Safe__Primitive):
            if not isinstance(item, self.expected_type):
                try:
                    item = self.expected_type(item)
                except (ValueError, TypeError) as e:
                    raise TypeError(f"In Type_Safe__List: Could not convert {type(item).__name__} to {self.expected_type.__name__}: {e}") from None

        elif hasattr(self.expected_type, '__bases__') and any(base.__name__ == 'Enum' for base in self.expected_type.__bases__):
            if isinstance(self.expected_type, type) and issubclass(self.expected_type, Enum):
                if isinstance(item, str):
                    if item in self.expected_type.__members__:
                        item = self.expected_type[item]
                    elif hasattr(self.expected_type, '_value2member_map_') and item in self.expected_type._value2member_map_:
                        item = self.expected_type._value2member_map_[item]

        try:
            self.is_instance_of_type(item, self.expected_type)
        except TypeError as e:
            raise TypeError(f"In Type_Safe__List: Invalid type for item: {e}") from None

        return item

    def append(self, item):
        item = self._validate_and_convert_item(item)
        super().append(item)

    def __setitem__(self, index, item):
        item = self._validate_and_convert_item(item)
        super().__setitem__(index, item)

    def __iadd__(self, items):
        for item in items:
            self.append(item)
        return self

    def insert(self, index, item):
        item = self._validate_and_convert_item(item)
        super().insert(index, item)

    def extend(self, items):
        for item in items:
            self.append(item)

    def json(self):                                                                     # Convert the list to a JSON-serializable format.
        from osbot_utils.type_safe.Type_Safe import Type_Safe                           # Import here to avoid circular imports

        result = []
        for item in self:
            if isinstance(item, Type_Safe):
                result.append(item.json())
            elif isinstance(item, Type_Safe__Primitive):
                result.append(item.__to_primitive__())
            elif isinstance(item, (list, tuple, frozenset)):
                result.append([x.json() if isinstance(x, Type_Safe) else serialize_to_dict(x) for x in item])
            elif isinstance(item, dict):
                result.append(serialize_to_dict(item))          # leverage serialize_to_dict since that method already knows how to handle
            elif isinstance(item, type):
                result.append(class_full_name(item))
            else:
                result.append(serialize_to_dict(item))          # also Use serialize_to_dict for unknown types (so that we don't return a non json object)
        return result

    def __add__(self, other):
        # Handle list1 + list2 - returns new Type_Safe__List with validation
        result = Type_Safe__List(expected_type=self.expected_type)
        for item in self:
            result.append(item)
        for item in other:
            result.append(item)  # Validates each item
        return result

    def __radd__(self, other):
        # Handle list + type_safe_list - returns new Type_Safe__List with validation
        result = Type_Safe__List(expected_type=self.expected_type)
        for item in other:
            result.append(item)  # Validates each item
        for item in self:
            result.append(item)
        return result

    def __mul__(self, n):
        # Handle list * n - returns new Type_Safe__List
        result = Type_Safe__List(expected_type=self.expected_type)
        for _ in range(n):
            for item in self:
                result.append(item)
        return result

    def __rmul__(self, n):
        # Handle n * list - same as __mul__
        return self.__mul__(n)

    def __imul__(self, n):
        # Handle list *= n - modifies in place
        items = list(self)
        self.clear()
        for _ in range(n):
            for item in items:
                self.append(item)
        return self

    def copy(self):
        # Return a Type_Safe__List copy, not a plain list
        result = Type_Safe__List(expected_type=self.expected_type)
        for item in self:
            result.append(item)
        return result