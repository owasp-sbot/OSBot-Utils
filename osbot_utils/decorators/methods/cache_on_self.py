from functools                                         import wraps
from typing                                            import Any, Callable, TypeVar, Dict
from weakref                                           import WeakKeyDictionary
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
