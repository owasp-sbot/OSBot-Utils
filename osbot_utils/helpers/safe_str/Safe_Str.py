import re
from typing                                              import Optional

TYPE_SAFE__STR__REGEX__SAFE_STR = re.compile(r'[^a-zA-Z0-9]')    # Only allow alphanumerics and numbers
TYPE_SAFE__STR__MAX_LENGTH      = 512

class Safe_Str(str):
    max_length                : int           = TYPE_SAFE__STR__MAX_LENGTH
    regex                     : re.Pattern    = TYPE_SAFE__STR__REGEX__SAFE_STR
    replacement_char          : str           = '_'
    allow_empty               : bool          = True
    trim_whitespace           : bool          = False
    allow_all_replacement_char: bool          = True

    def __new__(cls, value: Optional[str] = None) -> 'Safe_Str':

        if value is None:                                                                                               # Validate inputs
            if cls.allow_empty:
                value = ""
            else:
                raise ValueError("Value cannot be None when allow_empty is False")

        if not isinstance(value, str):                                                                                  # Convert to string if not already
            value = str(value)

        if cls.trim_whitespace:                                                                                         # Trim whitespace if requested
            value = value.strip()

        if not cls.allow_empty and (value is None or value == ""):                                                      # Check for empty string if not allowed
            raise ValueError("Value cannot be empty when allow_empty is False")

        if len(value) > cls.max_length:                                                                                 # Check max length
            raise ValueError(f"Value exceeds maximum length of {cls.max_length} characters (was {len(value)})")

        sanitized_value = cls.regex.sub(cls.replacement_char, value)                                                    # Apply regex sanitization

        if not cls.allow_all_replacement_char and set(sanitized_value) == {cls.replacement_char} and sanitized_value:   # Check if sanitized value consists entirely of replacement characters
            raise ValueError(f"Sanitized value consists entirely of '{cls.replacement_char}' characters")

        return str.__new__(cls, sanitized_value)