import re
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Topic import Safe_Str__Topic


class Safe_Str__Label(Safe_Str__Topic):         # ike Topic but allows dots and colons for hierarchical labels
    regex = re.compile(r'[^a-zA-Z0-9_\-.: ]')