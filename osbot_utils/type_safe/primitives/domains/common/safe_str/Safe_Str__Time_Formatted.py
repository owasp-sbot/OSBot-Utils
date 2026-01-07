import re

from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


class Safe_Str__Time_Formatted(Safe_Str):
    max_length = 50
    regex      = re.compile(r'[^0-9,.\s\wµ]')                                   # digits, comma, dot, space, letters, µ