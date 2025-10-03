import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__TEXT__MAX_LENGTH = 4096
TYPE_SAFE_STR__TEXT__REGEX      = r'[^a-zA-Z0-9_ ()\[\]\-+=:;,.?*\'"]'

class Safe_Str__Text(Safe_Str):
    regex      = re.compile(TYPE_SAFE_STR__TEXT__REGEX)
    max_length = TYPE_SAFE_STR__TEXT__MAX_LENGTH