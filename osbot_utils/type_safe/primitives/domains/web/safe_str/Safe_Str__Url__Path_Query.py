import re
from osbot_utils.type_safe.primitives.core.Safe_Str                             import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode     import Enum__Safe_Str__Regex_Mode
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Query import TYPE_SAFE_STR__URL__QUERY__CHARS

TYPE_SAFE_STR__URL__PATH_QUERY__MAX_LENGTH = 8192                           # Combined length (see note in Safe_Str__Url why this is so high)

TYPE_SAFE_STR__URL__PATH_QUERY__REGEX = re.compile(
    rf'^/?[a-zA-Z0-9/\-._~%]*'                    # Path part
    rf'(\?{TYPE_SAFE_STR__URL__QUERY__CHARS}*)?$' # Query part
)


class Safe_Str__Url__Path_Query(Safe_Str):
    """
    Safe string class for URL path with optional query parameters.

    Examples:
    - "/api/v1/users?page=1&limit=10"
    - "/products/123"
    - "/search?q=test&sort=desc"
    - "/"
    """
    regex                      = TYPE_SAFE_STR__URL__PATH_QUERY__REGEX
    regex_mode                 = Enum__Safe_Str__Regex_Mode.MATCH
    max_length                 = TYPE_SAFE_STR__URL__PATH_QUERY__MAX_LENGTH
    trim_whitespace            = True
    strict_validation          = True
    allow_empty                = True


    def __add__(self, other):                                                   # Smart concatenation for path+query
        from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Query import Safe_Str__Url__Query

        if isinstance(other, Safe_Str__Url__Query):
            base = str(self)
            query = str(other)

            if query:
                if '?' in base:
                    result = f"{base}&{query}"
                else:
                    result = f"{base}?{query}"
            else:
                result = base
            return Safe_Str__Url__Path_Query(result)

        else:                                                                   # Default behavior
            result = str(self) + str(other)
            return Safe_Str__Url__Path_Query(result)