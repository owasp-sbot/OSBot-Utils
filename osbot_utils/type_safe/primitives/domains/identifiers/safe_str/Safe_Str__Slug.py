import re
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id

class Safe_Str__Slug(Safe_Str__Id):                    # URL-friendly strings (lowercase, hyphens only)
    regex = re.compile(r'[^a-z0-9\-]')
    to_lower_case = True