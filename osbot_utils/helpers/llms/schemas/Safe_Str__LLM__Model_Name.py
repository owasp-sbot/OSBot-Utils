import re

from osbot_utils.type_safe.primitives.safe_str.Safe_Str import Safe_Str

TYPE_SAFE_STR__LLM__MODEL_NAME__MAX_LENGTH = 256
TYPE_SAFE_STR__LLM__MODEL_NAME__REGEX      =  r'[^a-zA-Z0-9/_\-.:]'

class Safe_Str__LLM__Model_Name(Safe_Str):
    regex      = re.compile(TYPE_SAFE_STR__LLM__MODEL_NAME__REGEX)
    max_length = TYPE_SAFE_STR__LLM__MODEL_NAME__MAX_LENGTH