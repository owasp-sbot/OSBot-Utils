import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__HTTP__LAST_MODIFIED__REGEX = re.compile(r'[^a-zA-Z0-9:, -]')
TYPE_SAFE_STR__HTTP__LAST_MODIFIED__MAX_LENGTH = 64

class Safe_Str__Http__Last_Modified(Safe_Str):
    regex                      = TYPE_SAFE_STR__HTTP__LAST_MODIFIED__REGEX
    max_length                 = TYPE_SAFE_STR__HTTP__LAST_MODIFIED__MAX_LENGTH
    trim_whitespace            = True