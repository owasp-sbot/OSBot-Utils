import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


class Safe_Str__LLM__Message__Response(Safe_Str):              # For assistant/AI responses
    max_length  = 32768                                         # Full context window for responses
    regex       = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F]')   # Permissive - only control chars