import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__FILE_PATH__REGEX      = re.compile(r'[^a-zA-Z0-9_\-./\\ ]')  # Allow alphanumerics, underscores, hyphens, dots, slashes, and spaces
TYPE_SAFE_STR__FILE_PATH__MAX_LENGTH = 1024

class Safe_Str__File__Path(Safe_Str):
    regex                      = TYPE_SAFE_STR__FILE_PATH__REGEX
    max_length                 = TYPE_SAFE_STR__FILE_PATH__MAX_LENGTH
    allow_empty                = True
    trim_whitespace            = True
    allow_all_replacement_char = False
