from osbot_utils.utils.Objects                  import class_full_name, serialize_to_dict
from osbot_utils.type_safe.Type_Safe__Base      import Type_Safe__Base, type_str
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive


class Type_Safe__Set(Type_Safe__Base, set):
    def __init__(self, expected_type, *args):
        super().__init__(*args)
        self.expected_type = expected_type

    def __contains__(self, item):
        if super().__contains__(item):                                                                  # First try direct lookup
            return True

        if type(self.expected_type) is type and issubclass(self.expected_type, Type_Safe__Primitive):   # Handle Type_Safe__Primitive conversions
            try:
                converted_item = self.expected_type(item)
                return super().__contains__(converted_item)
            except (ValueError, TypeError):
                return False

        return False

    def __repr__(self):
        expected_type_name = type_str(self.expected_type)
        return f"set[{expected_type_name}] with {len(self)} elements"

    def add(self, item):
        from osbot_utils.type_safe.Type_Safe import Type_Safe
        if type(self.expected_type) is type and issubclass(self.expected_type, Type_Safe) and type(item) is dict:       # Handle Type_Safe objects from dicts
            item = self.expected_type.from_json(item)
        elif type(self.expected_type) is type and issubclass(self.expected_type, Type_Safe__Primitive):                 # Handle Type_Safe__Primitive conversions (str -> Safe_Str, etc.)
            if not isinstance(item, self.expected_type):
                try:
                    item = self.expected_type(item)
                except (ValueError, TypeError) as e:
                    raise TypeError(f"In Type_Safe__Set: Could not convert {type(item).__name__} to {self.expected_type.__name__}: {e}") from None

        try:                                                                                                            # Now validate the (possibly converted) item
            self.is_instance_of_type(item, self.expected_type)
        except TypeError as e:
            raise TypeError(f"In Type_Safe__Set: Invalid type for item: {e}") from None

        super().add(item)

    def json(self):
        from osbot_utils.type_safe.Type_Safe import Type_Safe

        result = []
        for item in self:
            if isinstance(item, Type_Safe):
                result.append(item.json())
            elif isinstance(item, Type_Safe__Primitive):
                result.append(item.__to_primitive__())
            elif isinstance(item, (list, tuple, set, frozenset)):
                result.append([x.json() if isinstance(x, Type_Safe) else serialize_to_dict(x) for x in item])
            # elif isinstance(item, dict):
            #     result.append({k: v.json() if isinstance(v, Type_Safe) else v for k, v in item.items()})
            elif isinstance(item, type):
                result.append(class_full_name(item))
            else:
                result.append(serialize_to_dict(item))          # Use serialize_to_dict for unknown types (so that we don't return a non json object)
        return result

    def __eq__(self, other):                                        # todo: see if this is needed
        if isinstance(other, (set, Type_Safe__Set)):
            return set(self) == set(other)
        return False