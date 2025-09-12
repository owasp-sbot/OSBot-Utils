import re
from osbot_utils.type_safe.primitives.core.Safe_Str                         import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode




TYPE_SAFE_STR__VERSION__REGEX      = re.compile(r'^v(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')              # Regex to match versions like v0.1.1 or v999.999.999
TYPE_SAFE_STR__VERSION__MAX_LENGTH = 12                                                             # Max length for 'v999.999.999'

class Safe_Str__Version(Safe_Str):
    regex             = TYPE_SAFE_STR__VERSION__REGEX
    regex_mode        =  Enum__Safe_Str__Regex_Mode.MATCH                                            # in this case we need an exact match of the version regex
    max_length        = TYPE_SAFE_STR__VERSION__MAX_LENGTH
    allow_empty       = True
    trim_whitespace   = True
    strict_validation = True                                                                        # Ensure the value exactly matches the regex

    def __add__(self, other):                                                                       # Concatenation returns regular str, not Safe_Str__Version
        return str.__add__(self, other)

    def __radd__(self, other):                                                                      # Reverse concatenation also returns regular str
        return str.__add__(other, self)