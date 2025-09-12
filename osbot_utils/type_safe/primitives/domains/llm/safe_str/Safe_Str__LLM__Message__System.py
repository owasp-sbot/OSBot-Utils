import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


class Safe_Str__LLM__Message__System(Safe_Str):  # For system prompts
    max_length  = 4096                                         # Shorter than full prompts
    regex = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F]')        # Remove control chars EXCEPT tab (\x09), newline (\x0A), and carriage return (\x0D)
