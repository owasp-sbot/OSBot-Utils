import re

from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


class Safe_Str__Password(Safe_Str): # Password with minimum requirements.
    regex = re.compile(r'[^a-zA-Z0-9_\-.\s!@#$%^&*()]')
    min_length = 8  # Custom attribute

    def __new__(cls, value=None):
        result = super().__new__(cls, value)
        if len(result) < cls.min_length:
            raise ValueError(f"Password must be at least {cls.min_length} characters long")
        return result
