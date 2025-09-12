import re
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id

class Safe_Str__Key(Safe_Str__Id):                    # For dictionary/map keys, config keys
    regex = re.compile(r'[^a-zA-Z0-9_.-]')
