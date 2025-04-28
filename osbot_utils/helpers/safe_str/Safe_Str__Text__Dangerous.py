import re
from osbot_utils.helpers.safe_str.Safe_Str import Safe_Str

TYPE_SAFE_STR__TEXT__DANGEROUS__MAX_LENGTH = 65536
TYPE_SAFE_STR__TEXT__DANGEROUS__REGEX      = r'[^a-zA-Z0-9_\s!@#$%^&*()\[\]{}\-+=:;,.?"/\\<>\']'

class Safe_Str__Text__Dangerous(Safe_Str):
    regex      = re.compile(TYPE_SAFE_STR__TEXT__DANGEROUS__REGEX)
    max_length = TYPE_SAFE_STR__TEXT__DANGEROUS__MAX_LENGTH


Safe_Str__HTML = Safe_Str__Text__Dangerous          # we can reuse this class for Safe_Str__HTML since the regex and size are the same