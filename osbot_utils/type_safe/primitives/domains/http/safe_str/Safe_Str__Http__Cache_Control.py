import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__HTTP__CACHE_CONTROL__REGEX      = re.compile(r'[^a-zA-Z0-9\-,=\s]')
TYPE_SAFE_STR__HTTP__CACHE_CONTROL__MAX_LENGTH = 256

class Safe_Str__Http__Cache_Control(Safe_Str):
    """
    Safe string class for HTTP Cache-Control header values.
    Allows standard cache directives with parameters.
    Examples: 'no-cache', 'max-age=3600', 'private, must-revalidate'
    """
    regex                      = TYPE_SAFE_STR__HTTP__CACHE_CONTROL__REGEX
    max_length                 = TYPE_SAFE_STR__HTTP__CACHE_CONTROL__MAX_LENGTH
    trim_whitespace            = True