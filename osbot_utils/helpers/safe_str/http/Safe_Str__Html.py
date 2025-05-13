import re
from osbot_utils.helpers.safe_str.Safe_Str import Safe_Str

# Define the size constant
TYPE_SAFE_STR__HTML__MAX_LENGTH = 1048576  # 1 megabyte in bytes

# A minimal regex that only filters out:
# - NULL byte (U+0000)
# - Control characters (U+0001 to U+0008, U+000B to U+000C, U+000E to U+001F)
# We explicitly allow:
# - Tab (U+0009), Line Feed (U+000A), and Carriage Return (U+000D)
# - All other Unicode characters
TYPE_SAFE_STR__HTML__REGEX = re.compile(r'[\x00\x01-\x08\x0B\x0C\x0E-\x1F]')

class Safe_Str__Html(Safe_Str):
    max_length                 = TYPE_SAFE_STR__HTML__MAX_LENGTH
    regex                      = TYPE_SAFE_STR__HTML__REGEX