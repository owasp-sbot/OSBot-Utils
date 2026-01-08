import re

from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


class Safe_Str__Javascript(Safe_Str):
    max_length = 1_000_000
    regex      = re.compile(r'[^\x20-\x7E\n\t\r]')