import re
from osbot_utils.type_safe.primitives.core.Safe_Str                                  import Safe_Str


class Safe_Str__Python__Package(Safe_Str):                                           # Python package name
    max_length = 256                                                                 # Packages can have long paths
    regex      = re.compile(r'[^a-z0-9_]')                                           # Lowercase by convention (PEP 8)
