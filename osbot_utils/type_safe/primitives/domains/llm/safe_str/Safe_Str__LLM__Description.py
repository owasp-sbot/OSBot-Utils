import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

class Safe_Str__LLM__Description(Safe_Str):                                            # LLM model or feature description
    max_length = 4096
    regex      = re.compile(r'[^a-zA-Z0-9_ ()\[\]\-+=:;,.?*/\\×\n`&"\'#%<>{}$@|!\s~]')  # Allows common description chars

    # Supports rich descriptions with:
    # - Basic punctuation and formatting
    # - Mathematical symbols (×, +, -)
    # - Common special characters for technical descriptions
    # - Newlines for multi-line descriptions
    # - Brackets for annotations [like this]
    # - Quotes for "emphasis" or 'terms'