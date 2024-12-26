from osbot_utils.base_classes.Type_Safe__Base import Type_Safe__Base, type_str


class Type_Safe__List(Type_Safe__Base, list):

    def __init__(self, expected_type, *args):
        super().__init__(*args)
        self.expected_type = expected_type

    def __repr__(self):
        expected_type_name = type_str(self.expected_type)
        return f"list[{expected_type_name}] with {len(self)} elements"

    def append(self, item):
        try:
            self.is_instance_of_type(item, self.expected_type)
        except TypeError as e:
            raise TypeError(f"In Type_Safe__List: Invalid type for item: {e}")
        super().append(item)



