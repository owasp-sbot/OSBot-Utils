import re
from typing                                          import Any
from osbot_utils.utils.Misc                          import bytes_md5
from osbot_utils.type_safe.primitives.core.Safe_Str  import Safe_Str


# Constants for hash validation
SIZE__VALUE_HASH           = 10
TYPE_SAFE_STR__HASH__REGEX = re.compile(r'[^a-fA-F0-9]')                # Only allow hexadecimal characters

class Safe_Str__Hash(Safe_Str):
    regex                     = TYPE_SAFE_STR__HASH__REGEX
    max_length                = SIZE__VALUE_HASH
    allow_empty               = True                                   # Don't allow empty hash values
    trim_whitespace           = True                                   # Trim any whitespace
    strict_validation         = True                                   # Enable strict validation - new attribute
    exact_length              = True                                   # Require exact length match - new attribute

def safe_str_hash(value: Any) -> Safe_Str__Hash:
    if isinstance(value, str):
        value = value.encode()
    elif not isinstance(value, bytes):
        raise ValueError('In safe_str_hash, value must be a string or bytes')

    hash_value = bytes_md5(value)[0:SIZE__VALUE_HASH]
    return Safe_Str__Hash(hash_value)
