import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


class Safe_Str__LLM__Message__User(Safe_Str):                  # For user messages
    max_length  = 32768                                        # Full context window for user input
    regex       = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F]')  # Permissive - only control chars