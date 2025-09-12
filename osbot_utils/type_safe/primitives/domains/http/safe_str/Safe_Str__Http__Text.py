import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


TYPE_SAFE_STR__TEXT__MAX_LENGTH = 1048576           # Define the size constant - 1 megabyte in bytes

# A more permissive regex that primarily filters out:
# - NULL byte (U+0000)
# - Control characters (U+0001 to U+0008, U+000B to U+000C, U+000E to U+001F)
# - Some potentially problematic characters in various contexts
# But allows:
# - All standard printable ASCII characters
# - Tab (U+0009), Line Feed (U+000A), and Carriage Return (U+000D)
# - A wide range of punctuation, symbols, and Unicode characters for international text

TYPE_SAFE_STR__HTTP__TEXT__REGEX = re.compile(r'[\x00\x01-\x08\x0B\x0C\x0E-\x1F\x7F]')

class Safe_Str__Http__Text(Safe_Str):
    """
    Safe string class for general text content with a 1MB limit.
    Allows a wide range of characters suitable for natural language text,
    including international characters, while filtering out control characters
    and other potentially problematic sequences.
    """
    max_length                  = TYPE_SAFE_STR__TEXT__MAX_LENGTH
    regex                       = TYPE_SAFE_STR__HTTP__TEXT__REGEX
    trim_whitespace             = True              # Trim leading/trailing whitespace
    normalize_newlines          = True              # Option to normalize different newline styles

    def __new__(cls, value=None):

        if cls.normalize_newlines and value is not None and isinstance(value, str):         # Handle newline normalization before passing to parent class
            value = value.replace('\r\n', '\n').replace('\r', '\n')                         # Normalize different newline styles to \n

        return super().__new__(cls, value)                                                  # Now call the parent implementation