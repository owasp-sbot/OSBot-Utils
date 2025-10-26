import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__HTTP__COOKIE__REGEX = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')  # Filter control chars
#TYPE_SAFE_STR__HTTP__COOKIE__MAX_LENGTH = 4096
TYPE_SAFE_STR__HTTP__COOKIE__MAX_LENGTH = 32768     # 32k but, this should really be 4k , but validate this with data from live usage of this class

class Safe_Str__Http__Cookie(Safe_Str):
    """
    Safe string class for HTTP Cookie header values.
    Allows cookie name-value pairs with standard separators.
    Example: 'session=abc123; user_id=456; preferences={"theme":"dark"}'
    """
    regex                      = TYPE_SAFE_STR__HTTP__COOKIE__REGEX
    max_length                 = TYPE_SAFE_STR__HTTP__COOKIE__MAX_LENGTH
    trim_whitespace            = True