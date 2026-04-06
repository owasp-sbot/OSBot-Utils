import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

TYPE_SAFE_STR__FILE_PATH__REGEX      = re.compile(r'[^a-zA-Z0-9_\-./\\ ]')  # Allow alphanumerics, underscores, hyphens, dots, slashes, and spaces
TYPE_SAFE_STR__FILE_PATH__MAX_LENGTH = 1024

# todo:: this doesn't prevent path like "../../../etc/passwd" since those are valid paths
#        look at what we can do there (in terms of adding methods for __add__ + __radd__ , having a different class with that type of protection (i.e. does not allow ../ paths)
class Safe_Str__File__Path(Safe_Str):
    regex                      = TYPE_SAFE_STR__FILE_PATH__REGEX
    max_length                 = TYPE_SAFE_STR__FILE_PATH__MAX_LENGTH
    allow_empty                = True
    trim_whitespace            = True
    allow_all_replacement_char = False


    # todo: look at how we could add a method here to help preventing or detecting path transversal issues