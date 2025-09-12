import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

class Safe_Str__LLM__Tokenizer(Safe_Str):                                       # LLM tokenizer type identifier
    max_length = 64
    regex      = re.compile(r'[^a-zA-Z0-9\-_\s]')                              # Allows: alphanumeric, -, _, space

    # Supports tokenizer names:
    # - "cl100k_base"
    # - "tiktoken"
    # - "GPT-4 Tokenizer"
    # - "sentencepiece"
    # - "BPE"