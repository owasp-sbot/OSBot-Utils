import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__ID__REGEX      = re.compile(r'[^a-zA-Z0-9_\-]')
TYPE_SAFE_STR__ID__MAX_LENGTH = 128

class Safe_Str__Id(Safe_Str):           #     Safe string class for identifiers that allows alphanumerics, underscores, and hyphens.
    regex                      = TYPE_SAFE_STR__ID__REGEX
    max_length                 = TYPE_SAFE_STR__ID__MAX_LENGTH
    allow_empty                = True
    trim_whitespace            = True