import re
from osbot_utils.helpers.safe_str.Safe_Str import Safe_Str

class Safe_Str__File__Name(Safe_Str):
    regex                      = re.compile(r'[^a-zA-Z0-9_\-. ]')
    allow_empty                = False
    trim_whitespace            = True
    allow_all_replacement_char = False