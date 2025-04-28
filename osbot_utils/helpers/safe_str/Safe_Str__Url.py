
import re
from osbot_utils.helpers.safe_str.Safe_Str import Safe_Str

TYPE_SAFE_STR__URL__MAX_LENGTH = 2048                                                        # Common maximum URL length
TYPE_SAFE_STR__URL__REGEX      = re.compile(r'^(?!https?://).*|[^a-zA-Z0-9:/\-._~&=?#+%@]')  # Allow characters valid in URLs

class Safe_Str__Url(Safe_Str):
    regex                      = TYPE_SAFE_STR__URL__REGEX
    max_length                 = TYPE_SAFE_STR__URL__MAX_LENGTH
    trim_whitespace            = True
    allow_all_replacement_char = False