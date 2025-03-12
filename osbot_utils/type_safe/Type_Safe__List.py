from osbot_utils.type_safe.Type_Safe__Base import Type_Safe__Base, type_str

class Type_Safe__List(Type_Safe__Base, list):

    def __init__(self, expected_type, *args):
        super().__init__(*args)
        self.expected_type = expected_type

    def __repr__(self):
        expected_type_name = type_str(self.expected_type)
        return f"list[{expected_type_name}] with {len(self)} elements"

    def append(self, item):
        from osbot_utils.type_safe.Type_Safe import Type_Safe
        if type(self.expected_type) is type and issubclass(self.expected_type, Type_Safe) and type(item) is dict:  # if self.expected_type is Type_Safe and we have a dict
            item = self.expected_type.from_json(item)  # try to convert the dict into self.expected_type
        else:
            try:
                self.is_instance_of_type(item, self.expected_type)
            except TypeError as e:
               raise TypeError(f"In Type_Safe__List: Invalid type for item: {e}")
        super().append(item)


    def json(self): # Convert the list to a JSON-serializable format.
        from osbot_utils.type_safe.Type_Safe import Type_Safe                           # Import here to avoid circular imports

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
