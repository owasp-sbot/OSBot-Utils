from osbot_utils.utils.Objects              import class_full_name, serialize_to_dict
from osbot_utils.type_safe.Type_Safe__Base  import Type_Safe__Base, type_str

class Type_Safe__Tuple(Type_Safe__Base, tuple):

    def __new__(cls, expected_types, items=None):
        items = items or tuple()

        converted_items = cls.convert_items(expected_types, items)                  # Convert items BEFORE creating the tuple

        instance = super().__new__(cls, converted_items)
        instance.expected_types = expected_types
        return instance

    def __init__(self, expected_types, items=None):
        if items:
            self.validate_items(self)                                               # Validate the already-converted items

    @classmethod
    def convert_items(cls, expected_types, items):                                  # Convert items to expected types before creating the tuple.
        from osbot_utils.type_safe.Type_Safe            import Type_Safe
        from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive

        if not items:
            return tuple()

        if len(items) != len(expected_types):
            raise ValueError(f"Expected {len(expected_types)} elements, got {len(items)}")


        converted = []
        for item, expected_type in zip(items, expected_types):
            if type(expected_type) is type and issubclass(expected_type, Type_Safe) and type(item) is dict: # Handle Type_Safe objects from dicts
                item = expected_type.from_json(item)
            elif type(expected_type) is type and issubclass(expected_type, Type_Safe__Primitive):           # Handle Type_Safe__Primitive conversions
                if not isinstance(item, expected_type):
                    try:
                        item = expected_type(item)
                    except (ValueError, TypeError) as e:
                        raise TypeError(f"In Type_Safe__Tuple: Could not convert {type(item).__name__} to {expected_type.__name__}: {e}") from None

            converted.append(item)

        return tuple(converted)

    def validate_items(self, items):
        if len(items) != len(self.expected_types):
            raise ValueError(f"Expected {len(self.expected_types)} elements, got {len(items)}")
        for item, expected_type in zip(items, self.expected_types):
            try:
                self.is_instance_of_type(item, expected_type)
            except TypeError as e:
                raise TypeError(f"In Type_Safe__Tuple: Invalid type for item: {e}")

    def __repr__(self):
        types_str = ', '.join(type_str(t) for t in self.expected_types)
        return f"tuple[{types_str}] with {len(self)} elements"

    def json(self):
        from osbot_utils.type_safe.Type_Safe            import Type_Safe
        from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive

        result = []
        for item in self:
            if isinstance(item, Type_Safe):
                result.append(item.json())
            elif isinstance(item, Type_Safe__Primitive):
                result.append(item.__to_primitive__())  # Convert primitives to base types
            elif isinstance(item, (list, tuple, frozenset)):
                result.append([x.json() if isinstance(x, Type_Safe) else serialize_to_dict(x) for x in item])
            elif isinstance(item, dict):
                result.append(serialize_to_dict(item))
            elif isinstance(item, type):
                result.append(class_full_name(item))
            else:
                result.append(serialize_to_dict(item))          # Use serialize_to_dict for unknown types (so that we don't return a non json object)
        return result

    def __add__(self, other):
        # Tuple concatenation - requires defining new expected_types
        # This is tricky because we need to know the types of the other tuple
        # Option 1: Raise an error (safest)
        # Option 2: Return plain tuple (loses type safety)
        # Option 3: If other is Type_Safe__Tuple, combine expected_types

        if isinstance(other, Type_Safe__Tuple):
            new_expected_types = self.expected_types + other.expected_types
            new_items = tuple(self) + tuple(other)
            return Type_Safe__Tuple(expected_types=new_expected_types, items=new_items)
        else:
            # Can't safely concatenate without knowing types
            raise TypeError(
                f"Cannot concatenate Type_Safe__Tuple with {type(other).__name__}. "
                f"Use Type_Safe__Tuple for both operands to preserve type safety."
            )

    def __radd__(self, other):
        # Reverse concatenation
        if isinstance(other, Type_Safe__Tuple):
            new_expected_types = other.expected_types + self.expected_types
            new_items = tuple(other) + tuple(self)
            return Type_Safe__Tuple(expected_types=new_expected_types, items=new_items)
        else:
            raise TypeError(
                f"Cannot concatenate {type(other).__name__} with Type_Safe__Tuple. "
                f"Use Type_Safe__Tuple for both operands to preserve type safety."
            )

    def __mul__(self, n):
        # Tuple repetition - repeat expected_types n times
        if not isinstance(n, int) or n < 0:
            raise TypeError(f"can't multiply Type_Safe__Tuple by non-int of type {type(n).__name__}")

        new_expected_types = self.expected_types * n
        new_items = tuple(self) * n
        return Type_Safe__Tuple(expected_types=new_expected_types, items=new_items)

    def __rmul__(self, n):
        # Handle n * tuple
        return self.__mul__(n)