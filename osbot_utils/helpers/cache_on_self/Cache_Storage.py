from typing                                                 import Any
from osbot_utils.helpers.cache_on_self.Cache_Key_Generator  import CACHE_ON_SELF_KEY_PREFIX

# todo: review the side effects of having these static methods (since this could have some side effects)
class Cache_Storage:                                                                                                    # Handles cache storage and retrieval on instance

    @staticmethod
    def has_cached_value(instance: Any, cache_key: str) -> bool:                # Check if cached value exists
        return hasattr(instance, cache_key)

    @staticmethod
    def get_cached_value(instance: Any, cache_key: str) -> Any:                 # Retrieve cached value
        return getattr(instance, cache_key)

    @staticmethod
    def set_cached_value(instance: Any, cache_key: str, value: Any) -> None:    # Store value in cache
        setattr(instance, cache_key, value)

    @staticmethod
    def get_all_cache_keys(instance: Any) -> list:                              # Get all cache keys for debugging/inspection
        return [k for k in instance.__dict__.keys()
                if k.startswith(CACHE_ON_SELF_KEY_PREFIX)]

    @staticmethod
    def clear_cache(instance: Any) -> None:                                     # Clear all cached values for an instance
        cache_keys = Cache_Storage.get_all_cache_keys(instance)
        for key in cache_keys:
            delattr(instance, key)