import json
from enum                   import Enum
from typing                 import Callable, Dict, List, Tuple, Any
from osbot_utils.utils.Misc import str_md5


CACHE_ON_SELF_TYPES      = [int, float, bytearray, bytes, bool, complex, str]
CACHE_ON_SELF_KEY_PREFIX = '__cache_on_self__'


class Cache_Key_Generator:                                                          # Handles all cache key generation logic

    def __init__(self, supported_types: List[type] = None):
        self.supported_types = supported_types or CACHE_ON_SELF_TYPES

    def generate_key(self, function : Callable          ,
                           args     : Tuple   [Any, ...],
                           kwargs   : Dict    [str, Any]
                      ) -> str:                             # Generate cache key from function name and arguments
        key_name    = function.__name__
        args_hash   = self.get_args_hash(args)
        kwargs_hash = self.get_kwargs_hash(kwargs)
        return f'{CACHE_ON_SELF_KEY_PREFIX}_{key_name}_{args_hash}_{kwargs_hash}'

    def get_args_hash(self, args: Tuple[Any, ...]) -> str:                         # Get hash for args or empty string if no hashable args
        args_str = self.args_to_str(args)
        if args_str:
            return self.compute_hash(args_str)
        return ''

    def get_kwargs_hash(self, kwargs: Dict[str, Any]) -> str:                      # Get hash for kwargs or empty string if no hashable kwargs
        kwargs_str = self.kwargs_to_str(kwargs)
        if kwargs_str:
            return self.compute_hash(kwargs_str)
        return ''

    def args_to_str(self, args: Tuple[Any, ...]) -> str:                           # Convert supported args to string representation
        if not args:
            return ''

        parts = []
        for i, arg in enumerate(args):
            arg_str = self.value_to_cache_str(arg)
            if arg_str:
                # Include index to avoid collisions like (1, 23) vs (12, 3)
                parts.append(f"[{i}]:{arg_str}")
        return '|'.join(parts)

    def kwargs_to_str(self, kwargs: Dict[str, Any]) -> str:                        # Convert supported kwargs to string representation
        if not kwargs:
            return ''

        parts = []
        for key, value in sorted(kwargs.items()):  # Sort for consistent ordering
            value_str = self.value_to_cache_str(value)
            if value_str:
                parts.append(f'{key}:{value_str}')
        return '|'.join(parts)

    def value_to_cache_str(self, value: Any) -> str:                              # Convert a value to a cacheable string representation
        """Convert any value to a string suitable for cache key generation.

        Returns a type-prefixed string for all supported types.
        Returns empty string ONLY for unsupported types.
        """
        if value is None:
            return '<none>'

        # Handle primitive types with type prefix to avoid any collision
        value_type = type(value)
        if value_type in self.supported_types:
            type_name = value_type.__name__
            return f"<{type_name}>:{value}"

        # Handle mutable types by converting to a stable string representation
        try:
            if isinstance(value, dict):
                # Sort dict by keys for consistent ordering
                sorted_items = sorted(value.items())
                return f"<dict>:{json.dumps(sorted_items, sort_keys=True, separators=(',', ':'))}"

            elif isinstance(value, list):
                return f"<list>:{json.dumps(value, separators=(',', ':'))}"

            elif isinstance(value, tuple):
                return f"<tuple>:{json.dumps(value, separators=(',', ':'))}"

            elif isinstance(value, set):
                # Convert to sorted list for consistent ordering
                return f"<set>:{json.dumps(sorted(list(value)), separators=(',', ':'))}"

            elif isinstance(value, frozenset):
                return f"<frozenset>:{json.dumps(sorted(list(value)), separators=(',', ':'))}"

            elif isinstance(value, Enum):                                   # Handle Enum types - include both class name and member name for uniqueness
                enum_class = type(value).__name__
                enum_member = value.name
                return f"<enum:{enum_class}>:{enum_member}"


            else:
                # For other types, try to use repr if it's likely to be stable
                # This is a fallback - specific types should be handled above
                if hasattr(value, '__dict__'):
                    # For objects, we could hash their dict representation
                    # But this is risky, so we'll skip for now
                    return ''
                else:
                    # For other immutable types, try repr
                    try:
                        return f"other:{repr(value)}"
                    except:
                        return ''

        except (TypeError, ValueError, RecursionError):
            # If we can't serialize the value, skip it
            return ''

    def compute_hash(self, value: str) -> str:                                     # Compute hash of string value
        return str_md5(value)