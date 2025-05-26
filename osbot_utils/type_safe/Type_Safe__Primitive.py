class Type_Safe__Primitive:

    __primitive_base__ = None                                                   # Cache the primitive base type at class level

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for base in cls.__mro__:                                                # Find and cache the primitive base type when the class is created
            if base in (str, int, float):                                       # for now, we only support str, int, float
                cls.__primitive_base__ = base
                break

    def __eq__(self, other):
        if type(self) is type(other):                                           # Same type → compare values
            return super().__eq__(other)
        if self.__primitive_base__ and type(other) is self.__primitive_base__:  # Compare with cached primitive base type
            return super().__eq__(other)
        return False                                                            # Different types → not equal

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):                                                     # Include type in hash to maintain hash/eq contract , This works for str, int, float subclasses
        return hash((type(self).__name__, super().__hash__()))

    def __repr__(self):                                                     # Enhanced repr to show type information in assertions
        value_repr = super().__repr__()
        return f"{type(self).__name__}({value_repr})"

