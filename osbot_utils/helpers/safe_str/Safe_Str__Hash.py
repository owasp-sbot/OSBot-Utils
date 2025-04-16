import re
from osbot_utils.helpers.safe_str.Safe_Str  import Safe_Str
from osbot_utils.utils.Misc                 import str_md5

# Constants for hash validation
SIZE__VALUE_HASH           = 10
TYPE_SAFE_STR__HASH__REGEX = re.compile(r'[^a-fA-F0-9]')                # Only allow hexadecimal characters

class Safe_Str__Hash(Safe_Str):
    regex                     = TYPE_SAFE_STR__HASH__REGEX
    max_length                = SIZE__VALUE_HASH
    allow_empty               = False                                   # Don't allow empty hash values
    trim_whitespace           = True                                    # Trim any whitespace
    strict_validation         = True                                    # Enable strict validation - new attribute
    exact_length              = True                                    # Require exact length match - new attribute

def safe_str_hash(value : str):
    return str_md5(value)[0:SIZE__VALUE_HASH]
