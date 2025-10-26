import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

# todo: review this REGEX, since this look far too permissive for an Auth string (which is usually just ascii values

TYPE_SAFE_STR__HTTP__AUTHORIZATION__REGEX = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')  # Filter control chars
TYPE_SAFE_STR__HTTP__AUTHORIZATION__MAX_LENGTH = 2048


class Safe_Str__Http__Authorization(Safe_Str):
    """
    Safe string class for HTTP Authorization header values.
    Supports Bearer tokens, Basic auth, and other auth schemes.
    Examples: 'Bearer eyJ...', 'Basic dXNlcjpwYXNz'
    """
    regex                      = TYPE_SAFE_STR__HTTP__AUTHORIZATION__REGEX
    max_length                 = TYPE_SAFE_STR__HTTP__AUTHORIZATION__MAX_LENGTH
    trim_whitespace            = True