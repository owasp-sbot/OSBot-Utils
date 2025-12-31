import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

class Safe_Str__Python__Module(Safe_Str):
    """
    Python module/package names - valid as both:
    - Python identifiers: must start with letter/underscore, only letters/numbers/underscores
    - File system paths: safe on all platforms

    Examples: 'users', 'admin', 'file_store', 'api_v1'
    NOT: 'api-v1', 'api.v1', 'api/v1', '{users}'
    """
    max_length       = 64
    regex            = re.compile(r'[^a-z0-9_]')
    replacement_char = '_'
    to_lower_case    = True
    allow_empty      = True
    trim_whitespace  = True

    def __new__(cls, value: str = None):
        instance = super().__new__(cls, value)
        result = str(instance)                                              # Additional validation: must start with letter or underscore
        if result and not (result[0].isalpha() or result[0] == '_'):
            result = '_' + result
        return str.__new__(cls, result)