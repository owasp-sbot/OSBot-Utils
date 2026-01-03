import re
from osbot_utils.type_safe.primitives.core.Safe_Str                                  import Safe_Str


class Safe_Str__Python__Qualified_Name(Safe_Str):                                    # Full path: module.Class.method
    max_length = 512                                                                 # Can be quite long
    regex      = re.compile(r'[^a-zA-Z0-9_.]')                                       # Allows dots for path separator
