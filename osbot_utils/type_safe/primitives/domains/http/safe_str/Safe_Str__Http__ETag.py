import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__HTTP__ETAG__REGEX = re.compile(r'[^a-zA-Z0-9"\/\-_.:]')  # Allow alphanumerics, quotes, slashes, hyphens, underscores, periods, colons
TYPE_SAFE_STR__HTTP__ETAG__MAX_LENGTH = 128

class Safe_Str__Http__ETag(Safe_Str):
    regex                      = TYPE_SAFE_STR__HTTP__ETAG__REGEX
    max_length                 = TYPE_SAFE_STR__HTTP__ETAG__MAX_LENGTH
    trim_whitespace            = True