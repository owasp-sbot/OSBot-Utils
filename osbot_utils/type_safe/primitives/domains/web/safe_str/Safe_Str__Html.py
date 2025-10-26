import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

# Define the size constant

# Safe string class for HTML content with a 10MB limit.
# Allows HTML tags, attributes, and all characters needed for valid HTML,
# while filtering out control characters and NULL bytes that could cause
# security issues or rendering problems.
#
# This is specifically for HTML content (not general text), so it:
# - Allows angle brackets < > for tags
# - Allows quotes " ' for attributes
# - Preserves tabs and newlines for formatting
# - Has a large 10MB limit for full HTML documents
# - Trims outer whitespace but preserves internal formatting

TYPE_SAFE_STR__HTML__MAX_LENGTH = 10485760  # 10 megabytes in bytes (for large HTML documents)
TYPE_SAFE_STR__HTML__REGEX = re.compile(r'[\x00\x01-\x08\x0B\x0C\x0E-\x1F\x7F]')


class Safe_Str__Html(Safe_Str):
    max_length                 = TYPE_SAFE_STR__HTML__MAX_LENGTH
    regex                      = TYPE_SAFE_STR__HTML__REGEX
    trim_whitespace             = True                          # Trim leading/trailing whitespace
    normalize_newlines          = True                          # Normalize different newline styles

    def __new__(cls, value=None):
        if cls.normalize_newlines and value is not None and isinstance(value, str):
            value = value.replace('\r\n', '\n').replace('\r', '\n')                     # Normalize to \n

        return super().__new__(cls, value)

