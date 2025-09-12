import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


class Safe_Str__LLM__Message__Tool(Safe_Str):                   # For tool/function responses
    max_length  = 16384                                         # Tool responses often shorter
    regex       = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F]')   # Permissive for JSON/structured data