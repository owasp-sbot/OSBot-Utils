import re
import keyword
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

class Safe_Str__Python__Identifier(Safe_Str):
    """
    Ensures strings are valid Python identifiers.

    Rules:
    - Must start with letter or underscore
    - Can only contain letters, numbers, underscores
    - Cannot be a Python keyword

    Transformations:
    - Converts invalid starting characters (e.g., '8b1a...' → '_8b1a...')
    - Replaces invalid characters with underscores
    - Handles Python keywords by prefixing with underscore

    Examples:
        '8b1a9953c4' → '_8b1a9953c4'
        'my-var' → 'my_var'
        'class' → '_class'
    """
    max_length       = 255
    regex            = re.compile(r'[^a-zA-Z0-9_]')
    replacement_char = '_'
    to_lower_case    = False
    trim_whitespace  = True

    def __new__(cls, value: str = None):
        instance = super().__new__(cls, value)
        result = str(instance)

        if not result:
            return str.__new__(cls, '_')

        # Ensure starts with letter or underscore
        if not (result[0].isalpha() or result[0] == '_'):
            result = '_' + result

        # Check if it's a Python keyword

        if keyword.iskeyword(result):
            result = '_' + result

        return str.__new__(cls, result)