import re
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id


class Safe_Str__Display_Name(Safe_Str__Id):                    # For user-facing names with more allowed characters
    regex = re.compile(r'[^a-zA-Z0-9_\- ().\'#]')