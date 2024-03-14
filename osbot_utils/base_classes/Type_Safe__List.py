class Type_Safe__List(list):

    def __init__(self, expected_type, *args):
        super().__init__(*args)
        self.expected_type = expected_type

    def __repr__(self):
        return f"list[{self.expected_type.__name__}] with {len(self)} elements"

    def append(self, item):
        if not isinstance(item, self.expected_type):
            raise TypeError(f"In Type_Safe__List: Invalid type for item: Expected '{self.expected_type.__name__}', but got '{type(item).__name__}'")
        super().append(item)

