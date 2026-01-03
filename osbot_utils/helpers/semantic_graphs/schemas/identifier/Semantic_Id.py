import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

SAFE_STR__SEMANTIC_ID__REGEX      = re.compile(r'[^a-zA-Z0-9_\-.]')
SAFE_STR__SEMANTIC_ID__MAX_LENGTH = 128

class Semantic_Id(Safe_Str):

    regex           = SAFE_STR__SEMANTIC_ID__REGEX
    max_length      = SAFE_STR__SEMANTIC_ID__MAX_LENGTH
    allow_empty     = True
    trim_whitespace = True