import re
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id

class Safe_Str__Namespace(Safe_Str__Id):                    # For namespaced identifiers
    regex =  re.compile(r'[^a-zA-Z0-9.\-]')
