import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

class Safe_Str__LLM__Model_Slug(Safe_Str):                                      # URL-safe LLM model slug
    max_length = 256
    regex      = re.compile(r'[^a-zA-Z0-9/\-._]')                              # Allows: alphanumeric, /, -, ., _

    # URL-safe slugs for routing/APIs:
    # - "gpt-4-turbo"
    # - "claude-3-opus"
    # - "llama-3.1-70b"
    # - "command_r_plus"