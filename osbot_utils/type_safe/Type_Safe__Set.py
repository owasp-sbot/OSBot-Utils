from osbot_utils.type_safe.Type_Safe__Base import Type_Safe__Base, type_str

class Type_Safe__Set(Type_Safe__Base, set):
    def __init__(self, expected_type, *args):
        super().__init__(*args)
        self.expected_type = expected_type

    def __repr__(self):
        expected_type_name = type_str(self.expected_type)
        return f"set[{expected_type_name}] with {len(self)} elements"

    def add(self, item):
        try:
            self.is_instance_of_type(item, self.expected_type)
        except TypeError as e:
            raise TypeError(f"In Type_Safe__Set: Invalid type for item: {e}")
        super().add(item)

    def json(self):
        from osbot_utils.type_safe.Type_Safe import Type_Safe

        result = []
        for item in self:
            if isinstance(item, Type_Safe):
                result.append(item.json())
            elif isinstance(item, (list, tuple, set)):
                result.append([x.json() if isinstance(x, Type_Safe) else x for x in item])
            elif isinstance(item, dict):
                result.append({k: v.json() if isinstance(v, Type_Safe) else v for k, v in item.items()})
            else:
                result.append(item)
        return result

    def __eq__(self, other):                                        # todo: see if this is needed
        if isinstance(other, (set, Type_Safe__Set)):
            return set(self) == set(other)
        return False