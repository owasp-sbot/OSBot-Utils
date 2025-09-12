import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


class Safe_Str__Username(Safe_Str):
    """Allows only alphanumerics and underscores, with a 32 character limit."""
    regex = re.compile(r'[^a-zA-Z0-9_]')
    max_length = 32