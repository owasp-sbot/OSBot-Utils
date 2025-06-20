from functools import wraps
from typing import Callable, TypeVar, Any

from osbot_utils.helpers.cache_on_self.Cache_Controller import Cache_Controller
from osbot_utils.helpers.cache_on_self.Cache_Key_Generator import Cache_Key_Generator
from osbot_utils.helpers.cache_on_self.Cache_Metrics import Cache_Metrics
from osbot_utils.helpers.cache_on_self.Cache_Storage import Cache_Storage


def create_cache_wrapper(function       : Callable                  ,
                         key_generator  : Cache_Key_Generator = None,
                         storage        : Cache_Storage       = None,
                         controller     : Cache_Controller    = None,
                         metrics        : Cache_Metrics       = None
                    ) -> Callable:                              # Create the cache wrapper with injected dependencies
    
    # Use defaults if not provided
    key_gen     = key_generator or Cache_Key_Generator()
    storage     = storage or Cache_Storage
    controller  = controller or Cache_Controller
    
    @wraps(function)
    def wrapper(*args, **kwargs):
        self                        = controller.validate_self_argument(args  )                                         # Validate self argument
        should_reload, clean_kwargs = controller.should_reload_cache   (kwargs)                                         # Check reload cache parameter
        cache_key                   = key_gen   .generate_key          (function, args, clean_kwargs)                   # Generate cache key

        if should_reload or not storage.has_cached_value(self, cache_key):                                              # Check cache and execute if needed
            if metrics:
                metrics.record_miss() if not should_reload else metrics.record_reload()

            result = function(*args, **clean_kwargs)                                                                    # Execute function

            storage.set_cached_value(self, cache_key, result)                                                           # Store in cache
        else:
            if metrics:
                metrics.record_hit()

        return storage.get_cached_value(self, cache_key)                                                                # Return cached value
    
    # Attach utilities for testing/debugging        # todo: this is really not a good idea, since it is kinda a hack
    wrapper._cache_key_generator = key_gen
    wrapper._cache_storage       = storage
    wrapper._cache_controller    = controller
    wrapper._cache_metrics       = metrics
    
    return wrapper

T = TypeVar('T', bound=Callable[..., Any])

def cache_on_self(function: T) -> T:                                                    # Main decorator function (maintains original interface)
    """
    Decorator to cache method results on the instance.

    Use this for cases where we want the cache to be tied to the
    Class instance (i.e. not global for all executions)
    """
    return create_cache_wrapper(function)


# Convenience functions for backwards compatibility

def cache_on_self__get_cache_in_key(function, args=None, kwargs=None):                                                  # Get cache key - backwards compatibility
    key_gen = Cache_Key_Generator()
    return key_gen.generate_key(function, args or (), kwargs or {})


def cache_on_self__args_to_str(args):                                                                                   # Convert args to string - backwards compatibility
    key_gen = Cache_Key_Generator()
    return key_gen.args_to_str(args)


def cache_on_self__kwargs_to_str(kwargs):                                                                               # Convert kwargs to string - backwards compatibility
    key_gen = Cache_Key_Generator()
    return key_gen.kwargs_to_str(kwargs)