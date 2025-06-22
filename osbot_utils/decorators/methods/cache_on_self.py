from functools                                         import wraps
from typing                                            import Any, Callable, TypeVar
from osbot_utils.helpers.cache_on_self.Cache_On_Self   import Cache_On_Self


T = TypeVar('T', bound=Callable[..., Any])


def cache_on_self(function: T) -> T:                                                # Main decorator function
    """
    Decorator to cache method results on the instance.

    Use this for cases where we want the cache to be tied to the
    Class instance (i.e. not global for all executions)
    """
    cache_manager = Cache_On_Self(function=function)                                # Create cache manager in closure

    @wraps(function)
    def wrapper(*args, **kwargs):
        # Fast path - no special kwargs
        if not kwargs:
            return cache_manager.handle_call(args, kwargs)

        # Check for special __return__ parameter
        if kwargs.get('__return__') == 'cache_on_self':
            return cache_manager

        # Normal call with kwargs
        return cache_manager.handle_call(args, kwargs)

    return wrapper


# todo: these methods should be removed once all new tests have been added
# Convenience functions for backwards compatibility

def cache_on_self__get_cache_in_key(function, args=None, kwargs=None):              # Get cache key - backwards compatibility
    from osbot_utils.helpers.cache_on_self.Cache_Key_Generator import Cache_Key_Generator
    key_gen = Cache_Key_Generator()
    return key_gen.generate_key(function, args or (), kwargs or {})


def cache_on_self__args_to_str(args):                                              # Convert args to string - backwards compatibility
    from osbot_utils.helpers.cache_on_self.Cache_Key_Generator import Cache_Key_Generator
    key_gen = Cache_Key_Generator()
    return key_gen.args_to_str(args)


def cache_on_self__kwargs_to_str(kwargs):                                          # Convert kwargs to string - backwards compatibility
    from osbot_utils.helpers.cache_on_self.Cache_Key_Generator import Cache_Key_Generator
    key_gen = Cache_Key_Generator()
    return key_gen.kwargs_to_str(kwargs)