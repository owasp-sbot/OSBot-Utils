import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__HTTP__CONTENT_TYPE__REGEX = re.compile(r'[^a-zA-Z0-9/\-+.;= ]')
TYPE_SAFE_STR__HTTP__CONTENT_TYPE__MAX_LENGTH = 256

class Safe_Str__Http__Content_Type(Safe_Str):
    regex                      = TYPE_SAFE_STR__HTTP__CONTENT_TYPE__REGEX
    max_length                 = TYPE_SAFE_STR__HTTP__CONTENT_TYPE__MAX_LENGTH
    allow_empty                = True
    trim_whitespace            = True
    allow_all_replacement_char = False