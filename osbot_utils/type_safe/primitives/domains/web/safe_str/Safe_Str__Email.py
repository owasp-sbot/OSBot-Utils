import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

class Safe_Str__Email(Safe_Str):    # Special class for emails with simple custom validation.
    regex = re.compile(r'[^a-zA-Z0-9_\-.@]')
    max_length = 256

    def __new__(cls, value=None):
        result = super().__new__(cls, value)
        if value and '@' not in result:                                                               # Additional validation for email format
            raise ValueError(f"in {cls.__name__}, email must contain an @ symbol")
        return result