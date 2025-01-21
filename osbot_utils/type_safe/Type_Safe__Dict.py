from osbot_utils.type_safe.Type_Safe__Base import Type_Safe__Base

class Type_Safe__Dict(Type_Safe__Base, dict):
    def __init__(self, expected_key_type, expected_value_type, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.expected_key_type   = expected_key_type
        self.expected_value_type = expected_value_type

        # todo: see if we need to do this, since there was not code coverage hitting it
        # for k, v in self.items():                           # check type-safety of ctor arguments
        #     self.is_instance_of_type(k, self.expected_key_type  )
        #     self.is_instance_of_type(v, self.expected_value_type)

    def __setitem__(self, key, value):                                  # Check type-safety before allowing assignment.
        self.is_instance_of_type(key, self.expected_key_type)
        self.is_instance_of_type(value, self.expected_value_type)
        super().__setitem__(key, value)

    # def __repr__(self):
    #     key_type_name   = type_str(self.expected_key_type)
    #     value_type_name = type_str(self.expected_value_type)
    #     return f"dict[{key_type_name}, {value_type_name}] with {len(self)} entries"

    def json(self):                                                                         # Convert the dictionary to a JSON-serializable format.
        from osbot_utils.type_safe.Type_Safe import Type_Safe                               # can only import this here to avoid circular imports

        result = {}
        for key, value in self.items():
            if isinstance(value, Type_Safe):                                                # Handle Type_Safe objects in values
                result[key] = value.json()
            elif isinstance(value, (list, tuple)):                                          # Handle lists/tuples that might contain Type_Safe objects
                result[key] = [item.json() if isinstance(item, Type_Safe) else item
                               for item in value]
            elif isinstance(value, dict):                                                   # Handle nested dictionaries that might contain Type_Safe objects
                result[key] = {k: v.json() if isinstance(v, Type_Safe) else v
                               for k, v in value.items()}
            else:                                                                           # Regular values can be used as-is
                result[key] = value
        return result
