import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__TOPIC__REGEX      = re.compile(r'[^a-zA-Z0-9_\- ]')
TYPE_SAFE_STR__TOPIC__MAX_LENGTH = 512

class Safe_Str__Topic(Safe_Str):            # Safe string class for topic names that allows alphanumerics, underscores, hyphens and spaces.
    regex                      = TYPE_SAFE_STR__TOPIC__REGEX
    max_length                 = TYPE_SAFE_STR__TOPIC__MAX_LENGTH
    allow_empty                = True
    trim_whitespace            = True