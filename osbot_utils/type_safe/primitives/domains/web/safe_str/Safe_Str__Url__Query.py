import re
from osbot_utils.type_safe.primitives.core.Safe_Str                             import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode     import Enum__Safe_Str__Regex_Mode


TYPE_SAFE_STR__URL__QUERY__MAX_LENGTH = 8192        # (see note in Safe_Str__Url why this is so high)
TYPE_SAFE_STR__URL__QUERY__CHARS      = r'[a-zA-Z0-9=&\-._~%+,;!\'()*$]'
TYPE_SAFE_STR__URL__QUERY__REGEX      = re.compile(rf'^{TYPE_SAFE_STR__URL__QUERY__CHARS}*$')


class Safe_Str__Url__Query(Safe_Str):
    """
    Safe string class for URL query parameters (after ?).

    Examples:
    - "page=1&limit=10"
    - "search=test&sort=desc"
    - "id=123"
    - "" (empty is valid for URLs without query params)
    """
    regex                      = TYPE_SAFE_STR__URL__QUERY__REGEX
    regex_mode                 = Enum__Safe_Str__Regex_Mode.MATCH
    max_length                 = TYPE_SAFE_STR__URL__QUERY__MAX_LENGTH
    trim_whitespace            = True
    strict_validation          = True
    allow_empty                = True


    def __add__(self, other):
        """Smart concatenation for query strings"""
        # Query + Query = Query (with & separator)
        if isinstance(other, Safe_Str__Url__Query):
            left = str(self)
            right = str(other)
            if left and right:
                result = f"{left}&{right}"
            else:
                result = left or right
            return Safe_Str__Url__Query(result)

        # Query + string = Query
        else:
            result = str(self) + str(other)
            return Safe_Str__Url__Query(result)