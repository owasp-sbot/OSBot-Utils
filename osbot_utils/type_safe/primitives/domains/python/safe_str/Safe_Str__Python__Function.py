import re
from osbot_utils.type_safe.primitives.core.Safe_Str                                  import Safe_Str


class Safe_Str__Python__Function(Safe_Str):                                          # Python function name
    max_length = 128                                                                 # Reasonable function name limit
    regex      = re.compile(r'[^a-zA-Z0-9_]')                                        # Valid Python identifier chars
