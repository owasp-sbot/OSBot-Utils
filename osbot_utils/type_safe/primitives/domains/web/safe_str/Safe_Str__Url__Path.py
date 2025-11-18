import re
from osbot_utils.type_safe.primitives.core.Safe_Str                         import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode

TYPE_SAFE_STR__URL__PATH__MAX_LENGTH = 2048
TYPE_SAFE_STR__URL__PATH__REGEX      = re.compile(r'^/?[a-zA-Z0-9/\-._~%]*$')

class Safe_Str__Url__Path(Safe_Str):
    """
    Safe string class for URL path component.

    Examples:
    - "/api/v1/users"  (absolute path)
    - "api/v1/users"   (relative path)
    - "products/123"
    - "/"
    - ""
    """
    regex                      = TYPE_SAFE_STR__URL__PATH__REGEX
    regex_mode                 = Enum__Safe_Str__Regex_Mode.MATCH
    max_length                 = TYPE_SAFE_STR__URL__PATH__MAX_LENGTH
    trim_whitespace            = True
    strict_validation          = True
    allow_empty                = True

    def __add__(self, other):
        """Smart concatenation that returns appropriate URL component type"""
        from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Query       import Safe_Str__Url__Query
        from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Path_Query  import Safe_Str__Url__Path_Query

        if isinstance(other, Safe_Str__Url__Path):                          # Path + Path = Path
            left = str(self)
            right = str(other)

            # Both empty
            if not left and not right:
                return Safe_Str__Url__Path('')

            # One is empty - return the other AS-IS (preserve slashes)
            if not left:
                return Safe_Str__Url__Path(right)
            if not right:
                return Safe_Str__Url__Path(left)

            # Both non-empty - smart join
            left_clean = left.rstrip('/')
            right_clean = right.lstrip('/')
            result = f"{left_clean}/{right_clean}"
            return Safe_Str__Url__Path(result)

        elif isinstance(other, Safe_Str__Url__Query):                       # Path + Query = Path_Query
            query_str = str(other)
            if query_str:
                result = f"{self}?{query_str}"
            else:
                result = str(self)
            return Safe_Str__Url__Path_Query(result)

        elif isinstance(other, str) and other.startswith('?'):              # Path + string starting with '?' = Path_Query
            result = f"{self}{other}"
            return Safe_Str__Url__Path_Query(result)

        else:                                                               # Default: Path + string = Path
            result = str(self) + str(other)
            return Safe_Str__Url__Path(result)


    def __radd__(self, other):                                              # Handle reverse addition: string + Path
        if isinstance(other, str):
            left = other
            right = str(self)

            # One is empty - return the other AS-IS
            if not left:
                return Safe_Str__Url__Path(right)
            if not right:
                return Safe_Str__Url__Path(left)

            # Both non-empty - smart join
            left_clean = left.rstrip('/')
            right_clean = right.lstrip('/')
            result = f"{left_clean}/{right_clean}"
            return Safe_Str__Url__Path(result)

        return NotImplemented