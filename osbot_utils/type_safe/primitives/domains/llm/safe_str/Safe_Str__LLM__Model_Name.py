import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

class Safe_Str__LLM__Model_Name(Safe_Str):                                      # Human-readable LLM model name
    max_length = 256
    regex = re.compile(r'[^a-zA-Z0-9: .\-()+,]')                               # Allows: alphanumeric, :, space, ., -, (, ), +, &, ,

    # Supports various display names:
    # - "GPT-4 Turbo"
    # - "Claude 3 Opus (Latest)"
    # - "Llama 3.1: Instruct (70B)"
    # - "Command R+"
    # - "Gemini Pro 1.5"