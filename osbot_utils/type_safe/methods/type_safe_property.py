from typing import TypeVar, Type, Optional

T = TypeVar('T')

def type_safe_property(target_path: str, target_name: str, expected_type: Optional[Type[T]] = None) -> T: # Creates a type-safe property that delegates get/set operations to a nested data object

    def getter(self) -> T:
        target = self
        for part in target_path.split('.'):
            target = getattr(target, part)

        value = getattr(target, target_name)

        if expected_type and value is not None:
            if not isinstance(value, expected_type):
                raise TypeError(f"Property '{target_name}' returned value of type {type(value)}, expected {expected_type}")
        return value

    def setter(self, value: T) -> None:
        if expected_type and value is not None:
            if not isinstance(value, expected_type):
                raise TypeError(f"Cannot set property '{target_name}' with value of type {type(value)}, expected {expected_type}")

        target = self
        for part in target_path.split('.'):
            target = getattr(target, part)
        if hasattr(target, target_name) is False:
            raise AttributeError(f"Target path '{target_path}' does not have an attribute '{target_name}'")
        setattr(target, target_name, value)

    return property(getter, setter)


wire_as_property = type_safe_property
bind_as_property = type_safe_property
set_as_property  = type_safe_property
