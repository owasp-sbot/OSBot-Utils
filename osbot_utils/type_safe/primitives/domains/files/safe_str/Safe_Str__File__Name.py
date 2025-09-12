import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__FILE__NAME__REGEX = re.compile(r'[^a-zA-Z0-9_\-. ]')

class Safe_Str__File__Name(Safe_Str):
    regex                      = TYPE_SAFE_STR__FILE__NAME__REGEX
    allow_empty                = True
    trim_whitespace            = True
    allow_all_replacement_char = False