import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__HTTP__ACCEPT__REGEX      = re.compile(r'[^a-zA-Z0-9/\-+.*,;=\s]')
TYPE_SAFE_STR__HTTP__ACCEPT__MAX_LENGTH = 512

# todo: review with other http safe_str classes and see if we can't an Safe_Str__Http__Base
#       defines chars like this, and with the max length being the main difference
#       also, connect this with the RFP for the HTTP protocol, since that one should be providing a good set of
#       mappings for what chars are allowed in these http values
class Safe_Str__Http__Accept(Safe_Str):
    """
    Safe string class for HTTP Accept header values.
    Allows MIME types with quality parameters.
    Examples: 'text/html,application/json;q=0.9', 'application/*', '*/*'
    """
    regex                      = TYPE_SAFE_STR__HTTP__ACCEPT__REGEX
    max_length                 = TYPE_SAFE_STR__HTTP__ACCEPT__MAX_LENGTH
    trim_whitespace            = True