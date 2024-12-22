import re

REGEX__ASCII_VALUE = re.compile(r'[^a-zA-Z0-9_\s!@#$%^&*()\[\]{}\-+=:;,.?]')

class Str_ASCII(str):
    """
    A string subclass that ensures values only contain safe ASCII characters.
    Replaces any unsafe characters with underscores.
    """
    def __new__(cls, value=None, max_length=None):
        if value is None:
            value = ""

        if not isinstance(value, str):
            value = str(value)

        if max_length and len(value) > max_length:
            raise ValueError(f"Value length exceeds maximum of {max_length} characters (was {len(value)})")

        sanitized_value = REGEX__ASCII_VALUE.sub('_', value)

        return super().__new__(cls, sanitized_value)