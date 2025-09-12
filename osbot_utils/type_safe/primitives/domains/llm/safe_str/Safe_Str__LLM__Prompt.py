import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


class Safe_Str__LLM__Prompt(Safe_Str):                       # Or Safe_Str__LLM__Message
    max_length = 32768                                       # Common context window size
    regex = re.compile(r'[\x00\x01-\x08\x0B\x0C\x0E-\x1F]')  # Remove control chars only