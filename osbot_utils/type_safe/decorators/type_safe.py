import functools                                                                           # For wrapping functions
from osbot_utils.type_safe.Type_Safe__Method import Type_Safe__Method

def type_safe(func):                                                                        # Main decorator function
    type_checker = Type_Safe__Method(func)  # Create type checker instance

    has_only_self    = len(type_checker.params) == 1 and type_checker.params[0] == 'self'   # Check if method has only 'self' parameter or no parameters
    has_no_params    = len(type_checker.params) == 0
    direct_execution = has_no_params or has_only_self                                       # these are major performance optimisation where this @type_safe had an overhead of 250x (even on methods with no params) to now having an over head of ~5x
    if direct_execution:                                                                    # todo: review if we really need to do this, since although it is an optimisation, the idea of the type_safe attribute is to check when there are params
        return func

    @functools.wraps(func)                                                                 # Preserve function metadata
    def wrapper(*args, **kwargs):                                                          # Wrapper function
        if direct_execution:
            return func(*args, **kwargs)
        else:
            bound_args   = type_checker.handle_type_safety(args, kwargs)                       # Validate type safety
            return func(**bound_args.arguments)                                                # Call original function

    return wrapper                                                                         # Return wrapped function

