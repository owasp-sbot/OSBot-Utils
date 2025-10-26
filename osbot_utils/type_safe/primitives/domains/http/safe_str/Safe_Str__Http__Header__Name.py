import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__HTTP__HEADER_NAME__REGEX      = re.compile(r'[^a-zA-Z0-9\-]')
TYPE_SAFE_STR__HTTP__HEADER_NAME__MAX_LENGTH = 128

class Safe_Str__Http__Header__Name(Safe_Str):
    """
    Safe string class for HTTP header names.
    Allows alphanumerics and hyphens as per RFC 7230.
    HTTP/2 (RFC 7540) and HTTP/3 (RFC 9114) require header names to be lowercase.
    Common examples: content-type, authorization, user-agent, accept, cache-control
    """
    regex                      = TYPE_SAFE_STR__HTTP__HEADER_NAME__REGEX
    max_length                 = TYPE_SAFE_STR__HTTP__HEADER_NAME__MAX_LENGTH
    trim_whitespace            = True
    to_lower_case              = True
    allow_empty                = True