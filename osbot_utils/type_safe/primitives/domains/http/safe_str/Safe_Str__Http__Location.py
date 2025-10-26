import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

# note: as with the others check if this regex is over permissive
TYPE_SAFE_STR__HTTP__LOCATION__REGEX      = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')  # Filter control chars
TYPE_SAFE_STR__HTTP__LOCATION__MAX_LENGTH = 2048

class Safe_Str__Http__Location(Safe_Str):
    """
    Safe string class for HTTP Location header values (redirect URLs).
    Used in redirect responses (3xx status codes).
    Example: 'https://example.com/new-page', '/relative/path'
    """
    regex                      = TYPE_SAFE_STR__HTTP__LOCATION__REGEX
    max_length                 = TYPE_SAFE_STR__HTTP__LOCATION__MAX_LENGTH
    trim_whitespace            = True