import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

class Safe_Str__LLM__Modality(Safe_Str):                                        # LLM model modality descriptor
    max_length = 128
    regex      = re.compile(r'[^a-zA-Z0-9+\->\s]')                             # Allows: alphanumeric, +, -, >, space

    # Supports modality descriptions:
    # - "text"
    # - "text->image"
    # - "image+text->text"
    # - "multimodal"
    # - "text + vision"
    # - "audio->text"