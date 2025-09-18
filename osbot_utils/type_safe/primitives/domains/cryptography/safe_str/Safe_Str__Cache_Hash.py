import re
from osbot_utils.type_safe.primitives.core.Safe_Str                         import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode

class Safe_Str__Cache_Hash(Safe_Str):               # Variable-length cache hash (10-96 chars)
    regex             = re.compile(r'^[a-f0-9]{10,96}$')
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    min_length        = 10
    max_length        = 96
    strict_validation = True
    allow_empty       = True
    trim_whitespace   = True