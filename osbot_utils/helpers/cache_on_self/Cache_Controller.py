import inspect
from typing import Any, Dict


class Cache_Controller:                                                             # Controls cache behavior and reload logic

    def extract_clean_kwargs(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:      # Remove special parameters from kwargs
        return {k: v for k, v in kwargs.items()
                if k not in ['reload_cache', '__return__']}

    def should_reload(self, kwargs         : Dict[str, Any] ,
                            reload_next_flag: bool          ) -> bool:             # Determine if cache should be reloaded
        if reload_next_flag:
            return True
        return kwargs.get('reload_cache', False) is True

    def should_return_cache_manager(self, kwargs: Dict[str, Any]) -> bool:         # Check if should return cache manager
        return kwargs.get('__return__') == 'cache_on_self'

    def extract_self_from_args(self, args: tuple) -> Any:                          # Validate and extract self from args
        if len(args) == 0:
            raise ValueError("cache_on_self could not find self - no arguments provided")

        potential_self = args[0]
        if not inspect.isclass(type(potential_self)):
            raise ValueError("cache_on_self could not find self - first argument is not an instance")

        return potential_self