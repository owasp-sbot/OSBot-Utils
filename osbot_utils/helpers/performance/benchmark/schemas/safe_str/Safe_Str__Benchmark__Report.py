import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__TEXT__MAX_LENGTH = 1_048_576                                 # allow reports up to 1Mb in size
TYPE_SAFE_STR__TEXT__REGEX = (r'[^a-zA-Z0-9_ ()\[\]\-+=:;,.?*\'"\n'         # needed for text content        
                              r'─│┌┐└┘├┤┼]'                         )       # needed for displaying ok the Print_Table output

class Safe_Str__Benchmark__Report(Safe_Str):
    regex      = re.compile(TYPE_SAFE_STR__TEXT__REGEX)
    max_length = TYPE_SAFE_STR__TEXT__MAX_LENGTH