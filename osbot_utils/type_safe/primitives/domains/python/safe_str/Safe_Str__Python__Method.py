import re
from osbot_utils.type_safe.primitives.core.Safe_Str                                  import Safe_Str


class Safe_Str__Python__Method(Safe_Str):                                            # Python method name
    max_length = 128                                                                 # Reasonable method name limit
    regex      = re.compile(r'[^a-zA-Z0-9_]')                                        # Allows __dunder__ and _private
