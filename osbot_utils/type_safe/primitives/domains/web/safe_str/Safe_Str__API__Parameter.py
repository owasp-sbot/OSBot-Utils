import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

class Safe_Str__API__Parameter(Safe_Str):                                       # Generic API parameter name
    max_length = 64
    regex      = re.compile(r'[^a-zA-Z0-9_]')                                  # Allows: alphanumeric, _

    # Standard API parameter names:
    # - "max_tokens"
    # - "temperature"
    # - "top_p"
    # - "stream"
    # - "response_format"