import inspect
from typing import Tuple, Any


# todo: review the impact of having these methods static
class Cache_Controller:                                      # Controls cache behavior and reload logic

    @staticmethod
    def should_reload_cache(kwargs: dict                    # Check if cache should be reloaded and return cleaned kwargs.
                       ) -> Tuple[bool, dict]:              #    Returns: (should_reload, cleaned_kwargs)
        if 'reload_cache' not in kwargs:
            return False, kwargs

        reload = kwargs.get('reload_cache') is True                                         # todo: why not just del kwargs[reload_cache] since we know it exists in kwargs
        cleaned_kwargs = {k: v for k, v in kwargs.items() if k != 'reload_cache'}           # Create new dict without reload_cache
        return reload, cleaned_kwargs

    @staticmethod
    def validate_self_argument(args: tuple) -> Any:                                         # Validate and extract self from args
        if len(args) == 0:
            raise Exception("In Method_Wrappers.cache_on_self could not find self")

        potential_self = args[0]
        if inspect.isclass(type(potential_self)):
            return potential_self

        raise Exception("In Method_Wrappers.cache_on_self could not find self")

