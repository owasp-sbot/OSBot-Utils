import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

class Safe_Str__LLM__Model_Id(Safe_Str):                                        # Generic LLM model identifier
    max_length = 256
    regex      = re.compile(r'[^a-zA-Z0-9/\-.:_@]')                             # Allows: alphanumeric, /, -, ., :, _, @


    # Supports various model ID formats:
    # - OpenRouter: "openai/gpt-4", "anthropic/claude-3-opus"
    # - OpenAI: "gpt-4", "gpt-3.5-turbo"
    # - Anthropic: "claude-3-opus-20240229", "claude-3-sonnet@20240229"
    # - Cohere: "command-r-plus"
    # - Google: "models/gemini-pro"