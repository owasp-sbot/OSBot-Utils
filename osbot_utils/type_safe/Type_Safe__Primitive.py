class Type_Safe__Primitive:

    __primitive_base__ = None                                                   # Cache the primitive base type at class level

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for base in cls.__mro__:                                                # Find and cache the primitive base type when the class is created
            if base in (str, int, float):                                       # for now, we only support str, int, float
                cls.__primitive_base__ = base
                break

    def __add__(self, other):
        """Override addition/concatenation to maintain type safety"""
        if self.__primitive_base__ is str:                                      # For string concatenation
            result = super().__add__(other)                                     # Perform the operation
            return type(self)(result)                                           # Return instance of the safe type
        else:                                                                   # For numeric types (int, float)
            result = super().__add__(other)
            if result is NotImplemented:
                return result                                                   # Let Python try the reverse operation
            try:
                return type(self)(result)                                       # Try to create safe type
            except (ValueError, TypeError):
                return result                                                   # Fall back to primitive if constraints violated


    def __eq__(self, other):
        if type(self) is type(other):                                           # Same type → compare values
            return super().__eq__(other)
        if self.__primitive_base__ and type(other) is self.__primitive_base__:  # Compare with cached primitive base type
            return super().__eq__(other)
        return False                                                            # Different types → not equal

    def __enter__(self):                                                        # support context manager
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):                                                     # Include type in hash to maintain hash/eq contract , This works for str, int, float subclasses
        return hash((type(self).__name__, super().__hash__()))

    def __radd__(self, other):
        """Reverse addition/concatenation for when safe type is on the right"""
        if self.__primitive_base__ is str:
            result = other + str(self)                                         # Perform string concatenation
            return type(self)(result)                                          # Return instance of the safe type
        else:
            result = other + self.__primitive_base__(self)
            try:
                return type(self)(result)
            except (ValueError, TypeError):
                return result

    def __str__(self):                                              # Return the primitive string representation"""
        if self.__primitive_base__ is float:                        # Format the value using the primitive type's string formatting
            return format(float(self), '')
        elif self.__primitive_base__ is int:
            return format(int(self), '')
        elif self.__primitive_base__ is str:
            return str.__str__(self)
        return super().__str__()

    def __repr__(self):                                             # Enhanced repr for debugging that shows type information
        value_str = self.__str__()
        if self.__primitive_base__ is str:
            return f"{type(self).__name__}('{value_str}')"
        else:
            return f"{type(self).__name__}({value_str})"

    def __to_primitive__(self):                                     # Convert this Type_Safe__Primitive instance to its base primitive type.
        if self.__primitive_base__:
            return self.__primitive_base__(self)
        return str(self)                                            # fallback

    def obj(self):                                                                  # Get configuration as namespace object
        from osbot_utils.testing.__helpers import dict_to_obj
        return dict_to_obj(self.__cls_kwargs__())

    def __cls_kwargs__(self):                                                      # Get class-level kwargs (configuration)
        """Return dictionary of class-level configuration parameters"""
        kwargs = {}

        # Walk MRO but stop before primitive base classes
        for cls in reversed(self.__class__.__mro__):
            if cls in (float, int, str, object, Type_Safe__Primitive):
                continue

            # Get class attributes that are configuration parameters
            if hasattr(cls, '__annotations__'):
                for attr_name in cls.__annotations__:
                    if hasattr(cls, attr_name):
                        kwargs[attr_name] = getattr(cls, attr_name)

        return kwargs