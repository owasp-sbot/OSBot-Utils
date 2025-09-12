import re

from osbot_utils.type_safe.primitives.core.Safe_Str                         import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode

# Full 40-character commit SHA
TYPE_SAFE_STR__GITHUB__SHA__REGEX = re.compile(r'^[a-fA-F0-9]{40}$')
TYPE_SAFE_STR__GITHUB__SHA__LENGTH = 40

# todo: move to OSBot_Utils
class Safe_Str__SHA1(Safe_Str):
    """
    Safe string class for full 40-character Git commit SHAs.

    Examples:
    - "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d"
    - "abc1234567890abcdef1234567890abcdef12345"
    """
    regex             = TYPE_SAFE_STR__GITHUB__SHA__REGEX
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    max_length        = TYPE_SAFE_STR__GITHUB__SHA__LENGTH
    exact_length      = True
    allow_empty       = True
    trim_whitespace   = True
    strict_validation = True