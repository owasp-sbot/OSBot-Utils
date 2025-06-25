from weakref import WeakKeyDictionary
from typing import Any, Dict, List

class Cache_Storage:    # Handles all cache storage without polluting instance attributes

    def __init__(self):
        self.cache_data: WeakKeyDictionary = WeakKeyDictionary()  # Use WeakKeyDictionary so cache is automatically cleaned up when instances are garbage collected , instance -> {cache_key: value}

    def has_cached_value(self, instance: Any, cache_key: str) -> bool:
        if instance in self.cache_data:
            return cache_key in self.cache_data[instance]
        return False

    def get_cached_value(self, instance: Any, cache_key: str) -> Any:
        return self.cache_data[instance][cache_key]

    def set_cached_value(self, instance: Any, cache_key: str, value: Any) -> None:
        if instance not in self.cache_data:
            self.cache_data[instance] = {}
        self.cache_data[instance][cache_key] = value

    def get_all_cache_keys(self, instance: Any) -> List[str]:
        if instance in self.cache_data:
            return list(self.cache_data[instance].keys())
        return []

    def clear_key(self, instance: Any, cache_key: str) -> None:
        if instance in self.cache_data:
            self.cache_data[instance].pop(cache_key, None)

    def clear_all(self, instance: Any) -> None:
        if instance in self.cache_data:
            del self.cache_data[instance]