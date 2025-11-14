import collections
import inspect                                                                                                                       # For function introspection
from enum                                                                     import Enum
from typing                                                                   import get_args, get_origin, Union, List, Any, Dict    # For type hinting utilities
from osbot_utils.type_safe.Type_Safe__Base                                    import Type_Safe__Base
from osbot_utils.type_safe.Type_Safe__Primitive                               import Type_Safe__Primitive
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Annotations       import type_safe_annotations
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Shared__Variables import IMMUTABLE_TYPES


class Type_Safe__Method:                                                                  # Class to handle method type safety validation
    def __init__(self, func):                                                             # Initialize with function
        self.func         = func                                                          # Store original function
        self.sig          = inspect.signature(func)                                       # Get function signature
        self.annotations  = func.__annotations__                                          # Get function annotations
        self.params       = list(self.sig.parameters.keys())

    def check_for_any_use(self):
        for param_name, type_hint in self.annotations.items():
            if type_hint is any:  # Detect incorrect usage of lowercase any
                raise ValueError(f"Parameter '{param_name}' uses lowercase 'any' instead of 'Any' from typing module. "
                                f"Please use 'from typing import Any' and annotate as '{param_name}: Any'")

    def convert_primitive_parameters(self, bound_args):         # Convert parameters to Type_Safe__Primitive types where applicable

        for param_name, param_value in bound_args.arguments.items():
            if param_name == 'self' or param_name not in self.annotations:
                continue

            expected_type = self.annotations[param_name]

            enum_type = type_safe_annotations.extract_enum_from_annotation(expected_type)
            if enum_type and isinstance(param_value, str):
                if param_value in enum_type.__members__:                                                        # Reuse the exact conversion logic from Type_Safe__Step__Init
                    bound_args.arguments[param_name] = enum_type[param_value]
                    continue
                elif hasattr(enum_type, '_value2member_map_') and param_value in enum_type._value2member_map_:
                    bound_args.arguments[param_name] = enum_type._value2member_map_[param_value]
                    continue

            if not (isinstance(expected_type, type) and issubclass(expected_type, Type_Safe__Primitive)):           # Check if expected type is a Type_Safe__Primitive subclass
                continue

            primitive_base = expected_type.__primitive_base__                                                       # Try direct conversion for common cases

            if primitive_base in (int, float) and isinstance(param_value, (int, float,str)):                        # Handle string to int/float/str conversions
                try:
                    bound_args.arguments[param_name] = expected_type(param_value)
                    continue
                except (ValueError, TypeError):
                    pass                                                                                            # Let normal validation handle the error

            if primitive_base and isinstance(param_value, primitive_base):                                          # Handle values that match the primitive base type
                try:
                    bound_args.arguments[param_name] = expected_type(param_value)
                except (ValueError, TypeError):
                    pass                                                                                            # Let normal validation handle the error

    def handle_type_safety(self, args: tuple, kwargs: dict):                                # Main method to handle type safety
        self.check_for_any_use()
        bound_args = self.bind_args(args, kwargs)                                           # Bind arguments to parameters

        self.convert_primitive_parameters(bound_args)                                       # Pre-process primitive type conversions

        for param_name, param_value in bound_args.arguments.items():                        # Iterate through arguments
            if param_name != 'self':                                                        # Skip self parameter
                self.validate_parameter(param_name, param_value, bound_args)                # Validate each parameter
        return bound_args                                                                   # Return bound arguments

    def bind_args(self, args: tuple, kwargs: dict):                                         # Bind args to parameters
        bound_args = self.sig.bind(*args, **kwargs)                                         # Bind arguments to signature
        bound_args.apply_defaults()                                                         # Apply default values
        return bound_args                                                                   # Return bound arguments

    def validate_parameter(self, param_name: str, param_value: Any, bound_args):            # Validate a single parameter
        self.validate_immutable_parameter(param_name, param_value)                          # Validata the param_value (make sure if it set it is on of IMMUTABLE_TYPES)
        if param_name in self.annotations:                                                  # Check if parameter is annotated
            expected_type = self.annotations[param_name]                                    # Get expected type
            self.check_parameter_value(param_name, param_value, expected_type, bound_args)  # Check value against type

    def validate_immutable_parameter(self, param_name, param_value):
        param = self.sig.parameters.get(param_name)      # Check if this is a default value from a mutable type
        if param and param.default is param_value:       # This means the default value is being used
            if param_value is not None:
                if isinstance(param_value, IMMUTABLE_TYPES) is False:                            # Check if the value is an instance of any IMMUTABLE_TYPES
                    raise ValueError(f"Parameter '{param_name}' has a mutable default value of type '{type(param_value).__name__}'. "
                                     f"Only immutable types are allowed as default values in type_safe functions.")

    def check_parameter_value(self, param_name   : str,
                                    param_value  : Any,                    # Check parameter value against expected type
                                    expected_type: Any,
                                    bound_args       ):                              # Method parameters
        is_optional = self.is_optional_type(expected_type)                                # Check if type is optional
        has_default = self.has_default_value(param_name)                                  # Check if has default value

        if param_value is None:                                                           # Handle None value case
            self.validate_none_value(param_name, is_optional, has_default)                # Validate None value
            return                                                                        # Exit early

        if is_optional:                                                                     # Extract the non-None type from Optional
            non_none_type   = next(arg for arg in get_args(expected_type) if arg is not type(None))
            non_none_origin = get_origin(non_none_type)

            if non_none_origin is type:                                                     # If it's Optional[Type[T]], validate it
                self.validate_type_parameter(param_name, param_value, non_none_type)
                return
            else:                                                                           # If it's any other Optional type, validate against the non-None type
                self.check_parameter_value(param_name, param_value, non_none_type, bound_args)
                return

        origin_type = get_origin(expected_type)                                           # Get base type

        if origin_type is type:
            self.validate_type_parameter(param_name, param_value, expected_type)
            return

        if self.is_list_type(origin_type):                                               # Check if list type
            self.validate_list_type(param_name, param_value, expected_type)              # Validate list
            return                                                                       # Exit early

        if self.is_union_type(origin_type, is_optional):                                 # Check if union type
            self.validate_union_type(param_name, param_value, expected_type)             # Validate union
            return                                                                       # Exit early

        self.validate_direct_type(param_name, param_value, expected_type)                # Direct type validation

    def is_optional_type(self, type_hint: Any) -> bool:                                  # Check if type is Optional
        if get_origin(type_hint) is Union:                                               # Check if Union type
            return type(None) in get_args(type_hint)                                     # Check if None is allowed
        return False                                                                     # Not optional

    def has_default_value(self, param_name: str) -> bool:                               # Check if parameter has default value
        return (param_name in self.sig.parameters and                                   # Check parameter exists
                self.sig.parameters[param_name].default is not inspect._empty)          # Check has non-empty default

    def validate_none_value(self, param_name: str,                                      # Validate None value
                                  is_optional: bool,
                                  has_default: bool):
        if not (is_optional or has_default):                                            # If neither optional nor default
            raise ValueError(f"Parameter '{param_name}' is not optional but got None")  # Raise error for None value

    def is_list_type(self, origin_type: Any) -> bool:                                 # Check if type is a List
        return origin_type is list or origin_type is List                             # Check against list types

    def validate_list_type(self, param_name: str,                                                                                   # Validate list type and contents
                                 param_value: Any, expected_type: Any):                                                                     # List parameters
        if not isinstance(param_value, list):                                                                                       # Check if value is a list
            raise ValueError(f"Parameter '{param_name}' expected a list but got {type(param_value)}")                               # Raise error if not list

        args = get_args(expected_type)                                                                                              # Get type arguments
        if not args:                                                                                                                # If no type arguments (just List)
            return                                                                                                                  # Skip item validation - no type info available

        item_type = args[0]                                                                                                         # Get list item type
        item_origin = get_origin(item_type)                                                                                         # Get origin of item type

        if item_origin is dict or item_origin is Dict:                                                                              # Handle Dict[K, V] items
            key_type, value_type = get_args(item_type)                                                                              # Extract key and value types
            for i, item in enumerate(param_value):                                                                                  # Validate each dict in list
                if not isinstance(item, dict):                                                                                      # Check item is a dict
                    raise ValueError(f"List item at index {i} expected dict but got {type(item)}")                                  # Raise error if not dict
                if key_type is Any and value_type is Any:                                                                           # Skip validation if both are Any
                    continue                                                                                                        # No type checking needed
                for k, v in item.items():                                                                                           # Validate dict contents
                    if key_type is not Any and not isinstance(k, key_type):                                                         # Check key type if not Any
                        raise ValueError(f"Dict key '{k}' at index {i} expected type {key_type}, but got {type(k)}")                # Raise error for invalid key
                    if value_type is not Any and not isinstance(v, value_type):                                                     # Check value type if not Any
                        raise ValueError(f"Dict value for key '{k}' at index {i} expected type {value_type}, but got {type(v)}")    # Raise error for invalid value
        elif item_origin is collections.abc.Callable:                                                                               # Handle Callable[[...], ...] items
            for i, item in enumerate(param_value):                                                                                  # Validate each callable in list
                if not callable(item):                                                                                              # Check item is callable
                    raise ValueError(f"List item at index {i} expected callable but got {type(item)}")                              # Raise error if not callable
                # Note: Full signature validation would require is_callable_compatible method
        elif item_origin is not None:                                                                                               # Handle other subscripted types
            raise NotImplementedError(f"Validation for list items with subscripted type"
                                      f" '{item_type}' is not yet supported "
                                      f"in parameter '{param_name}'.")                                                              # todo: add support for checking for subscripted types
        else:                                                                                                                       # Handle non-subscripted types
            for i, item in enumerate(param_value):                                                                                  # Handle Type_Safe__Primitive conversion and validation
                if isinstance(item_type, type) and issubclass(item_type, Type_Safe__Primitive):                                     # Try to convert Type_Safe__Primitive types
                    if not isinstance(item, item_type):                                                                             # Only convert if not already correct type
                        try:
                            param_value[i] = item_type(item)                                                                        # Convert in place - will raise if invalid
                        except (ValueError, TypeError) as e:
                            raise ValueError(f"List item at index {i} could not be converted to {item_type}: {e}")
                elif not isinstance(item, item_type):
                    raise ValueError(f"List item at index {i} expected type {item_type}, but got {type(item)}")


    def validate_type_parameter(self, param_name: str, param_value: Any, expected_type: Any):                                       # Validate a Type[T] parameter
        if not isinstance(param_value, type):
            raise ValueError(f"Parameter '{param_name}' expected a type class but got {type(param_value)}")

        type_args = get_args(expected_type)                                                         # Extract the T from Type[T]
        if type_args:
            required_base = type_args[0]                                                            # get direct type (this doesn't handle Forward refs)
            if hasattr(required_base, '__origin__') or isinstance(required_base, type):
                if not issubclass(param_value, required_base):
                    raise ValueError(f"Parameter '{param_name}' expected type {expected_type}, but got "
                                     f"{param_value.__module__}.{param_value.__name__} which is not a subclass of {required_base}")

    def is_union_type(self, origin_type: Any, is_optional: bool) -> bool:             # Check if type is a Union
        return origin_type is Union and not is_optional                               # Must be Union but not Optional

    def validate_union_type(self, param_name   : str,
                                  param_value  : Any,
                                  expected_type: Any):                                  # validate Union type  parameters

        args_types = get_args(expected_type)                                         # Get allowed types
        if not any(isinstance(param_value, arg_type) for arg_type in args_types):    # Check if value matches any type
            raise ValueError(f"Parameter '{param_name}' expected one of types {args_types}, but got {type(param_value)}")  # Raise error if no match

    def try_basic_type_conversion(self, param_value: Any, expected_type: Any, param_name: str,bound_args) -> bool:      # Try to convert basic types
        if type(param_value) in [int, str]:                                                                             # Check if basic type
            try:                                                                                                        # Attempt conversion
                converted_value = expected_type(param_value)                                                            # Convert value
                bound_args.arguments[param_name] = converted_value                                                      # Update bound arguments
                return True                                                                                             # Return success
            except Exception:                                                                                           # Handle conversion failure
                pass                                                                                                    # Continue without conversion
        elif isinstance(param_value, Enum):                                                                             # Check if value is an Enum
            try:
                if issubclass(expected_type, str):                                                                      # If expecting string type
                    bound_args.arguments[param_name] = param_value.value                                                # Use enum's value
                    return True                                                                                         # Return success
            except Exception:                                                                                           # Handle conversion failure
                pass                                                                                                    # Continue without conversion
        return False                                                                                                    # Return failure
                                                            # Return failure

    # todo: refactor the method below in separate methods (or classes) since this is getting too complex)
    #       also see if there is opportunity to reuse other parts of the code base
    def validate_direct_type(self, param_name: str, param_value: Any, expected_type: Any):
        if expected_type is Any:                            # Handle typing.Any which accepts everything
            return True

        if param_value is None:                                                           # Handle None value case
            is_optional = self.is_optional_type(expected_type)                            # Check if type is optional
            has_default = self.has_default_value(param_name)                              # Check if has default value
            self.validate_none_value(param_name, is_optional, has_default)                # Validate None value
            return True

        origin = get_origin(expected_type)

        if origin is Union:                                                               # If it's a Union type
            return True                                                                   # there is another check that confirms it: todo: confirm this

        if origin is not None:                                                                              # If it's a generic type (like Dict, List, etc)
            if origin in (dict, Dict):                                                                      # Special handling for Dict
                if not isinstance(param_value, dict):
                    raise ValueError(f"Parameter '{param_name}' expected dict but got {type(param_value)}")

                type_args = get_args(expected_type)
                if not type_args:                                                                           # Dict without parameters (e.g., Dict instead of Dict[str, int])
                    return True                                                                             # Accept any dict without validating keys/values

                key_type, value_type = type_args

                if value_type is Any:                                                                       # if value type is Any, we don't need to do any checks since they will all match
                    return True

                validator = Type_Safe__Base()
                converted_dict = {}

                for k, v in param_value.items():
                    # Handle key conversion for Type_Safe__Primitive
                    if isinstance(key_type, type) and issubclass(key_type, Type_Safe__Primitive):
                        if not isinstance(k, key_type):
                            try:
                                k = key_type(k)
                            except (ValueError, TypeError) as e:
                                raise ValueError(f"Dict key '{k}' could not be converted to {key_type}: {e}") from None
                    elif get_origin(key_type) is None:                                                        # Validate key (existing logic)
                        if not isinstance(k, key_type):
                            raise ValueError(f"Dict key '{k}' expected type {key_type}, but got {type(k)}")
                    else:
                        try:
                            validator.is_instance_of_type(k, key_type)
                        except TypeError as e:
                            raise ValueError(f"Dict key '{k}' in parameter '{param_name}': {e}") from None

                    # Handle value conversion for Type_Safe__Primitive
                    if value_type is not Any:
                        if isinstance(value_type, type) and issubclass(value_type, Type_Safe__Primitive):
                            if not isinstance(v, value_type):
                                try:
                                    v = value_type(v)
                                except (ValueError, TypeError) as e:
                                    raise ValueError(f"Dict value for key '{k}' could not be converted to {value_type}: {e}") from None
                        else:
                            try:
                                validator.is_instance_of_type(v, value_type)
                            except TypeError as e:
                                raise ValueError(f"Dict value for key '{k}' in parameter '{param_name}': {e}") from None

                    converted_dict[k] = v

                # Replace the original dict with converted dict
                param_value.clear()
                param_value.update(converted_dict)

                return True
            base_type = origin
        else:
            base_type = expected_type

        if not isinstance(param_value, base_type):
            raise ValueError(f"Parameter '{param_name}' expected type {expected_type}, but got {type(param_value)}") from None
        return True