import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__HTTP__HEADER_VALUE__REGEX = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')  # Filter control chars except tab
TYPE_SAFE_STR__HTTP__HEADER_VALUE__MAX_LENGTH = 8192

class Safe_Str__Http__Header__Value(Safe_Str):
    """
    Safe string class for HTTP header values.
    Allows visible ASCII and spaces per RFC 7230.
    Filters out control characters except tab (0x09).
    """
    regex                      = TYPE_SAFE_STR__HTTP__HEADER_VALUE__REGEX
    max_length                 = TYPE_SAFE_STR__HTTP__HEADER_VALUE__MAX_LENGTH
    trim_whitespace            = True