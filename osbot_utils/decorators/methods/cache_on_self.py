import inspect
from functools                                         import wraps
from typing import Any, Callable, TypeVar, Dict
from weakref import WeakKeyDictionary

from osbot_utils.helpers.cache_on_self.Cache_On_Self   import Cache_On_Self


T = TypeVar('T', bound=Callable[..., Any])

# Global registry of cache managers per instance per method
# Structure: {instance: {method_name: Cache_On_Self}}
_cache_managers_registry: WeakKeyDictionary[Any, Dict[str, Cache_On_Self]] = WeakKeyDictionary()



def cache_on_self(function: T) -> T:
    """
    Decorator to cache method results on the instance.

    Use this for cases where we want the cache to be tied to the
    Class instance (i.e. not global for all executions)
    """
    function_name = function.__name__

    @wraps(function)
    def wrapper(*args, **kwargs):
        # Extract self from args
        if not args:
            raise ValueError("cache_on_self could not find self - no arguments provided")

        self = args[0]

        # we can't do this here for performance reasons
        # Check if this is a class (not instance)
        # if inspect.isclass(type(self)):
        #     # Normal instance method call
        #     pass
        # else:
        #     raise ValueError("cache_on_self could not find self - first argument is not an instance")

        # Get or create cache manager for this instance/method combination
        if self not in _cache_managers_registry:
            _cache_managers_registry[self] = {}

        if function_name not in _cache_managers_registry[self]:
            # Create new cache manager for this instance/method
            _cache_managers_registry[self][function_name] = Cache_On_Self(function=function)

        cache_manager = _cache_managers_registry[self][function_name]

        # Handle special __return__ parameter
        if kwargs.get('__return__') == 'cache_on_self':
            return cache_manager

        # Normal call
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