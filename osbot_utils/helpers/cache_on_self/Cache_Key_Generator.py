from typing                 import Callable
from osbot_utils.utils.Misc import str_md5

CACHE_ON_SELF_TYPES      = [int, float, bytearray, bytes, bool, complex, str]
CACHE_ON_SELF_KEY_PREFIX = '__cache_on_self__'

class Cache_Key_Generator:                                                                                              # Handles all cache key generation logic

    def __init__(self, supported_types: list = None):
        self.supported_types = supported_types or CACHE_ON_SELF_TYPES

    def generate_key(self, function: Callable, args: tuple, kwargs: dict) -> str:                                       # Generate cache key from function name and arguments
        key_name    = function.__name__
        args_hash   = self.get_args_hash(args)
        kwargs_hash = self.get_kwargs_hash(kwargs)
        return f'{CACHE_ON_SELF_KEY_PREFIX}_{key_name}_{args_hash}_{kwargs_hash}'

    def get_args_hash(self, args: tuple) -> str:                                                                        # Get hash for args or empty string if no hashable args
        args_str = self.args_to_str(args)
        if args_str:
            return self.compute_hash(args_str)
        return ''

    def get_kwargs_hash(self, kwargs: dict) -> str:                                                                     # Get hash for kwargs or empty string if no hashable kwargs
        kwargs_str = self.kwargs_to_str(kwargs)
        if kwargs_str:
            return self.compute_hash(kwargs_str)
        return ''

    def args_to_str(self, args: tuple) -> str:                                                                          # Convert supported args to string representation
        if not args:
            return ''

        parts = []
        for arg in args:
            if type(arg) in self.supported_types:
                parts.append(str(arg))
        return ''.join(parts)

    def kwargs_to_str(self, kwargs: dict) -> str:                                                                       # Convert supported kwargs to string representation
        if not kwargs:
            return ''

        parts = []
        for key, value in kwargs.items():
            if type(value) in self.supported_types:
                parts.append(f'{key}:{value}|')
        return ''.join(parts)

    def compute_hash(self, value: str) -> str:                                                                          # Compute hash of string value
        return str_md5(value)