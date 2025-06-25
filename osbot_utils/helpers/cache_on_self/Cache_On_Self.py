from typing                                                import Any, Callable, Dict, List
from osbot_utils.type_safe.Type_Safe                       import Type_Safe
from osbot_utils.helpers.cache_on_self.Cache_Controller    import Cache_Controller
from osbot_utils.helpers.cache_on_self.Cache_Key_Generator import Cache_Key_Generator, CACHE_ON_SELF_KEY_PREFIX
from osbot_utils.helpers.cache_on_self.Cache_Metrics       import Cache_Metrics
from osbot_utils.helpers.cache_on_self.Cache_Storage       import Cache_Storage


class Cache_On_Self(Type_Safe):
    cache_storage       : Cache_Storage                                             # Storage handler instance
    controller          : Cache_Controller                                          # Controller instance
    key_generator       : Cache_Key_Generator                                       # Key generator instance
    metrics             : Cache_Metrics                                             # Metrics tracking
    function            : Callable                                                  # The wrapped function
    function_name       : str                                                       # Cached function name
    no_args_key         : str                                                       # Pre-computed key for no args
    target_self         : Any                        = None                         # The instance being cached on
    current_cache_key   : str                        = ''                           # Current cache key
    current_cache_value : Any                        = None                         # Current cached value
    reload_next         : bool                       = False                        # Force reload on next call
    disabled            : bool                       = False                         # cache disable status

    def __init__(self, function       : Callable                   = None ,
                       supported_types: List[type]                 = None ):
        super().__init__()
        self.function       = function
        self.function_name  = function.__name__ if function else ''
        self.no_args_key    = f'{CACHE_ON_SELF_KEY_PREFIX}_{self.function_name}__' # Pre-compute for performance
        self.cache_storage  = Cache_Storage()
        self.controller     = Cache_Controller()
        self.key_generator  = Cache_Key_Generator(supported_types)
        self.metrics        = Cache_Metrics()

    def handle_call(self, args: tuple, kwargs: dict) -> Any:                        # Main entry point for cached calls
        # Check if caching is disabled
        if self.disabled:
            return self.execute(args, kwargs)

        if not kwargs and len(args) == 1:                                           # Fast path for common case: no kwargs, single arg (self)
            target_self = args[0]
            cache_key   = self.no_args_key

            if self.cache_storage.has_cached_value(target_self, cache_key):         # Use cache_storage
                self.metrics.hits += 1                                              # Increment cache Hit
                return self.cache_storage.get_cached_value(target_self, cache_key)  # Use cache_storage

            self.metrics.misses += 1                                                # Increment cache miss - execute and store (Direct increment)
            result = self.function(*args)
            self.cache_storage.set_cached_value(target_self, cache_key, result)    # Use cache_storage instead of setattr
            return result

        return self.handle_call_full(args, kwargs)

    def handle_call_full(self, args  : tuple,
                               kwargs: dict
                          ) -> Any:                                                 # Full logic for complex cases
        # Check if caching is disabled
        if self.disabled:
            clean_kwargs = self.controller.extract_clean_kwargs(kwargs)
            return self.execute(args, clean_kwargs)

        # Extract values - don't store as instance variables to avoid recursion issues
        target_self   = self.controller.extract_self_from_args(args)
        clean_kwargs  = self.controller.extract_clean_kwargs(kwargs)
        should_reload = self.controller.should_reload(kwargs, self.reload_next)
        cache_key     = self.key_generator.generate_key(self.function, args, clean_kwargs)

        if should_reload:
            self.reload_next = False                                                # Reset reload flag

        cached_exists = self.cache_storage.has_cached_value(target_self, cache_key)

        if should_reload or not cached_exists:
            # Execute and cache, passing the cache key directly
            result = self.execute_and_cache(args, clean_kwargs, target_self, cache_key, should_reload)
        else:
            self.metrics.record_hit()
            result = self.cache_storage.get_cached_value(target_self, cache_key)

        # Update instance state only for external inspection
        self.target_self = target_self
        self.current_cache_key = cache_key
        self.current_cache_value = result

        return result

    def execute(self, args   : tuple,
                      kwargs : dict ,
                 ) -> Any:                                # Execute function
        return self.function(*args, **kwargs)

    def execute_and_cache(self, args         : tuple,
                                clean_kwargs : dict,
                                target_self  : Any,
                                cache_key    : str,
                                should_reload: bool) -> Any:                      # Execute function and store result
        if should_reload:
            self.metrics.record_reload()
        else:
            self.metrics.record_miss()

        result = self.execute(args=args, kwargs=clean_kwargs)
        self.cache_storage.set_cached_value(target_self, cache_key, result)
        return result

    def clear(self) -> None:                                                        # Clear current cache entry
        if self.target_self and self.current_cache_key:
            self.cache_storage.clear_key(self.target_self, self.current_cache_key)

    def clear_all(self) -> None:                                                    # Clear all cache for current instance
        if self.target_self:
            self.cache_storage.clear_all(self.target_self)

    def get_all_keys(self) -> List[str]:                                           # Get all cache keys for current instance
        if self.target_self:
            return self.cache_storage.get_all_cache_keys(self.target_self)
        return []

    def stats(self) -> Dict[str, Any]:                                             # Get cache statistics
        return { 'hits'      : self.metrics.hits      ,
                 'misses'    : self.metrics.misses    ,
                 'reloads'   : self.metrics.reloads   ,
                 'hit_rate'  : self.metrics.hit_rate  ,
                 'cache_key' : self.current_cache_key }