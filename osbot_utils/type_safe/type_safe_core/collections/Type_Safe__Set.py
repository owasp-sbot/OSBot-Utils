from typing                                     import Type
from osbot_utils.utils.Objects                  import class_full_name, serialize_to_dict
from osbot_utils.type_safe.Type_Safe__Base      import Type_Safe__Base, type_str
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive


class Type_Safe__Set(Type_Safe__Base, set):
    expected_type : Type = None                         # Class-level default

    def __init__(self, expected_type=None, initial_data=None):
        super().__init__()                                                                  # Initialize empty set first

        if isinstance(expected_type, (set, frozenset)) and initial_data is None:            # Smart detection
            initial_data  = expected_type                                                   # They're using the pattern: An_Set({'a', 'b'})
            expected_type = None                                                            # Move the set to initial_data

        self.expected_type = expected_type or self.__class__.expected_type                  # Use provided type, or fall back to class-level attribute

        if self.expected_type is None:                                                      # Validate that we have type set
            raise ValueError(f"{self.__class__.__name__} requires expected_type")

        if initial_data is not None:                                                        # Process initial data through our type-safe add
            for item in initial_data:
                self.add(item)

    def __contains__(self, item):
        if super().__contains__(item):                                                                  # First try direct lookup
            return True

        if type(self.expected_type) is type and issubclass(self.expected_type, Type_Safe__Primitive):   # Handle Type_Safe__Primitive conversions
            try:
                converted_item = self.expected_type(item)
                return super().__contains__(converted_item)
            except (ValueError, TypeError):
                return False

        return False

    def __repr__(self):
        expected_type_name = type_str(self.expected_type)
        return f"set[{expected_type_name}] with {len(self)} elements"

    def add(self, item):
        from osbot_utils.type_safe.Type_Safe import Type_Safe
        if type(self.expected_type) is type and issubclass(self.expected_type, Type_Safe) and type(item) is dict:       # Handle Type_Safe objects from dicts
            item = self.expected_type.from_json(item)
        elif type(self.expected_type) is type and issubclass(self.expected_type, Type_Safe__Primitive):                 # Handle Type_Safe__Primitive conversions (str -> Safe_Str, etc.)
            if not isinstance(item, self.expected_type):
                try:
                    item = self.expected_type(item)
                except (ValueError, TypeError) as e:
                    raise TypeError(f"In Type_Safe__Set: Could not convert {type(item).__name__} to {self.expected_type.__name__}: {e}") from None

        try:                                                                                                            # Now validate the (possibly converted) item
            self.is_instance_of_type(item, self.expected_type)
        except TypeError as e:
            raise TypeError(f"In Type_Safe__Set: Invalid type for item: {e}") from None

        super().add(item)

    def json(self):
        from osbot_utils.type_safe.Type_Safe import Type_Safe

        result = []
        for item in self:
            if isinstance(item, Type_Safe):
                result.append(item.json())
            elif isinstance(item, Type_Safe__Primitive):
                result.append(item.__to_primitive__())
            elif isinstance(item, (list, tuple, set, frozenset)):
                result.append([x.json() if isinstance(x, Type_Safe) else serialize_to_dict(x) for x in item])
            # elif isinstance(item, dict):
            #     result.append({k: v.json() if isinstance(v, Type_Safe) else v for k, v in item.items()})
            elif isinstance(item, type):
                result.append(class_full_name(item))
            else:
                result.append(serialize_to_dict(item))          # Use serialize_to_dict for unknown types (so that we don't return a non json object)
        return result

    def __eq__(self, other):                                        # todo: see if this is needed
        if isinstance(other, (set, Type_Safe__Set)):
            return set(self) == set(other)
        return False

    def update(self, *others):
        for other in others:
            for item in other:
                self.add(item)  # Delegates to add() which validates

    def copy(self):
        # Return a copy of the same subclass type
        result = self.__class__(expected_type=self.expected_type)
        for item in self:
            result.add(item)
        return result

    def __or__(self, other):
        # Handle | operator - returns new instance of same subclass
        result = self.__class__(expected_type=self.expected_type)
        for item in self:
            result.add(item)
        for item in other:
            result.add(item)  # Validates
        return result

    def __ror__(self, other):
        # Handle reverse | operator - returns same subclass type
        result = self.__class__(expected_type=self.expected_type)
        for item in other:
            result.add(item)  # Validates
        for item in self:
            result.add(item)
        return result

    def __and__(self, other):
        # Handle & operator (intersection) - returns same subclass type
        result = self.__class__(expected_type=self.expected_type)
        for item in super().__and__(other):
            result.add(item)
        return result

    def __rand__(self, other):
        # Handle reverse & operator
        return self.__and__(other)

    def __sub__(self, other):
        # Handle - operator (difference) - returns same subclass type
        result = self.__class__(expected_type=self.expected_type)
        for item in super().__sub__(other):
            result.add(item)
        return result

    def __rsub__(self, other):
        # Handle reverse - operator
        result = self.__class__(expected_type=self.expected_type)
        for item in set(other) - set(self):
            result.add(item)  # Validates items from other
        return result

    def __xor__(self, other):
        # Handle ^ operator (symmetric difference) - returns same subclass type
        result = self.__class__(expected_type=self.expected_type)
        for item in set(self) - set(other):
            result.add(item)
        for item in set(other) - set(self):
            result.add(item)  # Validates
        return result

    def __rxor__(self, other):
        # Handle reverse ^ operator
        return self.__xor__(other)

    def union(self, *others):
        # Return same subclass type with validation
        result = self.__class__(expected_type=self.expected_type)
        for item in self:
            result.add(item)
        for other in others:
            for item in other:
                result.add(item)  # Validates
        return result

    def intersection(self, *others):
        # Return same subclass type
        result = self.__class__(expected_type=self.expected_type)
        base_result = set(self)
        for other in others:
            base_result &= set(other)
        for item in base_result:
            result.add(item)
        return result

    def difference(self, *others):
        # Return same subclass type
        result = self.__class__(expected_type=self.expected_type)
        base_result = set(self)
        for other in others:
            base_result -= set(other)
        for item in base_result:
            result.add(item)
        return result

    def symmetric_difference(self, other):
        # Return same subclass type with validation for items from other
        result = self.__class__(expected_type=self.expected_type)
        for item in set(self) - set(other):
            result.add(item)
        for item in set(other) - set(self):
            result.add(item)  # Validates
        return result

    def __ior__(self, other):
        # Handle |= operator
        for item in other:
            self.add(item)  # Delegates to add() which validates
        return self

    def __iand__(self, other):
        # Handle &= operator (intersection) - only keeps existing valid items
        super().__iand__(other)
        return self

    def __isub__(self, other):
        # Handle -= operator (difference) - only removes items
        super().__isub__(other)
        return self

    def __ixor__(self, other):
        # Handle ^= operator (symmetric difference)
        # Items from other need validation before being added
        to_add = set(other) - set(self)
        to_remove = set(self) & set(other)
        for item in to_remove:
            self.discard(item)
        for item in to_add:
            self.add(item)  # Validates
        return self