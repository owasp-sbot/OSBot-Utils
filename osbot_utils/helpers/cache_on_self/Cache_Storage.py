from typing                                                import Any, List, TYPE_CHECKING
from osbot_utils.helpers.cache_on_self.Cache_Key_Generator import CACHE_ON_SELF_KEY_PREFIX

if TYPE_CHECKING:
    from osbot_utils.helpers.cache_on_self.Cache_On_Self import Cache_On_Self


class Cache_Storage():                                                                # Handles cache storage and retrieval on instance

    def __init__(self, cache_on_self: 'Cache_On_Self'):
        self.cache_on_self = cache_on_self

    def has_cached_value(self, instance : Any ,
                               cache_key : str ) -> bool:                           # Check if cached value exists
        return hasattr(instance, cache_key)

    def get_cached_value(self, instance : Any ,
                               cache_key : str ) -> Any:                            # Retrieve cached value
        return getattr(instance, cache_key)

    def set_cached_value(self, instance : Any  ,
                               cache_key : str  ,
                               value     : Any  ) -> None:                          # Store value in cache
        setattr(instance, cache_key, value)

    def get_all_cache_keys(self, instance: Any) -> List[str]:                      # Get all cache keys for debugging/inspection
        return [k for k in instance.__dict__.keys()
                if k.startswith(CACHE_ON_SELF_KEY_PREFIX)]

    def clear_key(self, instance : Any ,
                        cache_key: str ) -> None:                                   # Clear specific cache key
        if hasattr(instance, cache_key):
            delattr(instance, cache_key)

    def clear_all(self, instance: Any) -> None:                                    # Clear all cached values for an instance
        cache_keys = self.get_all_cache_keys(instance)
        for key in cache_keys:
            delattr(instance, key)