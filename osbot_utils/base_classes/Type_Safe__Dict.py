from osbot_utils.base_classes.Type_Safe__Base import type_str, Type_Safe__Base

class Type_Safe__Dict(Type_Safe__Base, dict):
    def __init__(self, expected_key_type, expected_value_type, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.expected_key_type   = expected_key_type
        self.expected_value_type = expected_value_type

        for k, v in self.items():                           # check type-safety of ctor arguments
            self.is_instance_of_type(k, self.expected_key_type  )
            self.is_instance_of_type(v, self.expected_value_type)

    def __setitem__(self, key, value):                                  # Check type-safety before allowing assignment.
        self.is_instance_of_type(key, self.expected_key_type)
        self.is_instance_of_type(value, self.expected_value_type)
        super().__setitem__(key, value)

    def __repr__(self):
        key_type_name   = type_str(self.expected_key_type)
        value_type_name = type_str(self.expected_value_type)
        return f"dict[{key_type_name}, {value_type_name}] with {len(self)} entries"
