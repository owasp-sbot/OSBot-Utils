from osbot_utils.type_safe.Type_Safe__Base import Type_Safe__Base, type_str

class Type_Safe__Tuple(Type_Safe__Base, tuple):

    def __new__(cls, expected_types, items=None):
        items    = items or tuple()
        instance = super().__new__(cls, items)
        instance.expected_types = expected_types
        return instance

    def __init__(self, expected_types, items=None):             # todo: see if we should be assigning expected_types to self here
        if items:
            self.validate_items(items)

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
        from osbot_utils.type_safe.Type_Safe import Type_Safe

        result = []
        for item in self:
            if isinstance(item, Type_Safe):
                result.append(item.json())
            elif isinstance(item, (list, tuple)):
                result.append([x.json() if isinstance(x, Type_Safe) else x for x in item])
            elif isinstance(item, dict):
                result.append({k: v.json() if isinstance(v, Type_Safe) else v for k, v in item.items()})
            else:
                result.append(item)
        return result