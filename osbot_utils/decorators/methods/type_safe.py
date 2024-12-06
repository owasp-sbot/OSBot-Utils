import functools                                                                           # For wrapping functions
from osbot_utils.helpers.Type_Safe_Method import Type_Safe_Method

def type_safe(func):                                                                       # Main decorator function
    @functools.wraps(func)                                                                 # Preserve function metadata
    def wrapper(*args, **kwargs):                                                          # Wrapper function
        type_checker = Type_Safe_Method(func)                                              # Create type checker instance
        bound_args   = type_checker.handle_type_safety(args, kwargs)                       # Validate type safety
        return func(**bound_args.arguments)                                                # Call original function

    return wrapper                                                                         # Return wrapped function

