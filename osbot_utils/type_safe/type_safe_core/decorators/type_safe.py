import functools                                                                                    # For wrapping functions
from typing                                                         import get_args
from osbot_utils.type_safe.Type_Safe__Base                          import Type_Safe__Base
from osbot_utils.type_safe.Type_Safe__Primitive                     import Type_Safe__Primitive
from osbot_utils.type_safe.type_safe_core.methods.Type_Safe__Method import Type_Safe__Method
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Cache   import type_safe_cache


def type_safe(func):                                                                                # Main decorator function
    type_checker = Type_Safe__Method(func).setup()                                                  # Create type checker instance
    return_type  = func.__annotations__.get('return')

    validator        = Type_Safe__Base() if return_type else None
    has_only_self    = len(type_checker.params) == 1 and type_checker.params[0] == 'self'           # Check if method has only 'self' parameter or no parameters
    has_no_params    = len(type_checker.params) == 0
    direct_execution = has_no_params or has_only_self                                               # these are major performance optimisation where this @type_safe had an overhead of 250x (even on methods with no params) to now having an over head of ~5x
    has_var_keyword  = type_checker.var_keyword_param is not None                                   # Pre-calculate if we need to handle VAR_KEYWORD parameters (performance optimization)


    @functools.wraps(func)                                                                          # Preserve function metadata
    def wrapper(*args, **kwargs):                                                                   # Wrapper function
        if direct_execution:
            result =  func(*args, **kwargs)
        else:
            bound_args = type_checker.handle_type_safety(args, kwargs)                              # Validate type safety
            if has_var_keyword:                                                                     # Only call prepare_function_arguments if needed
                regular_args, var_kwargs = type_checker.prepare_function_arguments(bound_args)
                result = func(**regular_args, **var_kwargs)
            else:
                result = func(**bound_args.arguments)

        if return_type is not None and result is not None:                                          # Validate return type using existing type checking infrastructure
            if isinstance(return_type, type) and issubclass(return_type, Type_Safe__Primitive):     # Try to convert Type_Safe__Primitive types
                result = return_type(result)                                                        # Since we are using a Type_Safe__Primitive, if there is bad data (like a negative number in Safe_UInt) this will trigger an exception

            result = convert_return_value(result, return_type)                                      # todo: refactor convert_return_value into another class (maybe validator or a new converter class)
            try:
                validator.is_instance_of_type(result, return_type)
            except TypeError as e:
                raise TypeError(f"Function '{func.__qualname__}' return type validation failed: {e}") from None

        return result
    return wrapper                                                                                  # Return wrapped function


# todo: see if we can optmise this return value conversion, namely in detecting if a conversion is needed
def convert_return_value(result, return_type):
    """Convert return value to match expected type with auto-conversion."""
    from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List import Type_Safe__List
    from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set  import Type_Safe__Set
    from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict import Type_Safe__Dict

    origin = type_safe_cache.get_origin(return_type)
    args   = get_args(return_type)

    # # Handle List[T] -> Type_Safe__List conversion
    if origin is list and args and isinstance(result, list) and not isinstance(result, Type_Safe__List):
        item_type = args[0]
        type_safe_list = Type_Safe__List(expected_type=item_type)
        for item in result:
            type_safe_list.append(item)  # Auto-converts items
        return type_safe_list

    # Handle Set[T] -> Type_Safe__Set conversion
    if origin is set and args and isinstance(result, set) and not isinstance(result, Type_Safe__Set):
        item_type = args[0]
        type_safe_set = Type_Safe__Set(expected_type=item_type)
        for item in result:
            type_safe_set.add(item)  # Auto-converts items
        return type_safe_set

    # Handle Dict[K, V] -> Type_Safe__Dict conversion
    if origin is dict and args and len(args) == 2 and isinstance(result, dict) and not isinstance(result, Type_Safe__Dict):
        key_type, value_type = args
        type_safe_dict = Type_Safe__Dict(expected_key_type=key_type, expected_value_type=value_type)
        for k, v in result.items():
            type_safe_dict[k] = v  # Auto-converts keys and values
        return type_safe_dict

    # Handle Type_Safe__List subclass directly (e.g., -> An_List)
    if isinstance(return_type, type) and issubclass(return_type, Type_Safe__List):
        if isinstance(result, list) and not isinstance(result, return_type):
            return return_type(result)  # Uses nice constructor: An_List(['a', 'b'])
        return result

    # Handle Type_Safe__Set subclass directly (e.g., -> An_Set)
    if isinstance(return_type, type) and issubclass(return_type, Type_Safe__Set):
        if isinstance(result, (set, list, tuple)) and not isinstance(result, return_type):
            return return_type(result)  # Uses nice constructor: An_Set({'a', 'b'})
        return result

    # Handle Type_Safe__Dict subclass directly (e.g., -> Hash_Mapping)
    if isinstance(return_type, type) and issubclass(return_type, Type_Safe__Dict):
        if isinstance(result, dict) and not isinstance(result, return_type):
            return return_type(result)  # Uses nice constructor: Hash_Mapping({'key': 'val'})
        return result

    return result