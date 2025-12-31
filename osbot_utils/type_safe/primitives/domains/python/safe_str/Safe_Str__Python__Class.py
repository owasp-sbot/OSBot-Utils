import re
from osbot_utils.type_safe.primitives.core.Safe_Str                                  import Safe_Str


class Safe_Str__Python__Class(Safe_Str):                                             # Python class name
    max_length = 128                                                                 # Reasonable class name limit
    regex      = re.compile(r'[^a-zA-Z0-9_]')                                        # Valid Python identifier chars
