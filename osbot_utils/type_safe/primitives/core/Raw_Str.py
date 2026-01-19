from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive


class Raw_Str(Type_Safe__Primitive, str):                                        # Base for validated-but-not-sanitized strings
    __primitive_base__ = str
    max_length         = None                                                    # Override in subclasses
    min_length         = None                                                    # Override in subclasses
    allow_empty        = True                                                    # Override in subclasses

    def __new__(cls, value=None):
        if value is None:
            value = ''
        if not isinstance(value, str):
            value = str(value)
        if not cls.allow_empty and value == '':
            raise ValueError(f"{cls.__name__} cannot be empty")
        if cls.min_length is not None and len(value) < cls.min_length:
            raise ValueError(f"{cls.__name__} must be at least {cls.min_length} chars")
        if cls.max_length is not None and len(value) > cls.max_length:
            raise ValueError(f"{cls.__name__} exceeds max length of {cls.max_length}")
        return super().__new__(cls, value)
