from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt

DEFAULT__VALUE_UINT__LLM__MAX_TOKENS = 5000

class Safe_UInt__LLM__Max_Tokens(Safe_UInt):                                    # LLM max tokens parameter
    min_value : int = 1                                                         # Minimum 1 token required
    max_value : int = 200000                                                    # Maximum 200k tokens (Claude's limit)

    @classmethod
    def __default__value__(cls):
        return DEFAULT__VALUE_UINT__LLM__MAX_TOKENS                             # Sensible default instead of min_value