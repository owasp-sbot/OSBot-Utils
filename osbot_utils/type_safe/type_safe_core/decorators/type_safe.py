import functools                                                                                    # For wrapping functions
from osbot_utils.type_safe.Type_Safe__Base                          import Type_Safe__Base
from osbot_utils.type_safe.Type_Safe__Primitive                     import Type_Safe__Primitive
from osbot_utils.type_safe.type_safe_core.methods.Type_Safe__Method import Type_Safe__Method


def type_safe(func):                                                                                # Main decorator function
    type_checker = Type_Safe__Method(func)  # Create type checker instance
    return_type  = func.__annotations__.get('return')

    validator        = Type_Safe__Base() if return_type else None
    has_only_self    = len(type_checker.params) == 1 and type_checker.params[0] == 'self'           # Check if method has only 'self' parameter or no parameters
    has_no_params    = len(type_checker.params) == 0
    direct_execution = has_no_params or has_only_self                                               # these are major performance optimisation where this @type_safe had an overhead of 250x (even on methods with no params) to now having an over head of ~5x

    @functools.wraps(func)                                                                          # Preserve function metadata
    def wrapper(*args, **kwargs):                                                                   # Wrapper function
        if direct_execution:
            result =  func(*args, **kwargs)
        else:
            bound_args = type_checker.handle_type_safety(args, kwargs)                              # Validate type safety
            result     =  func(**bound_args.arguments)                                              # Call original function

        if return_type is not None and result is not None:                                          # Validate return type using existing type checking infrastructure
            if isinstance(return_type, type) and issubclass(return_type, Type_Safe__Primitive):     # Try to convert Type_Safe__Primitive types
                result = return_type(result)                                                        # Since we are using a Type_Safe__Primitive, if there is bad data (like a negative number in Safe_UInt) this will trigger an exception
            try:
                validator.is_instance_of_type(result, return_type)
            except TypeError as e:
                raise TypeError(f"Function '{func.__qualname__}' return type validation failed: {e}") from None

        return result
    return wrapper                                                                                  # Return wrapped function

