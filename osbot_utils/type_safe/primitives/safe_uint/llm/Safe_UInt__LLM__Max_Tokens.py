from osbot_utils.type_safe.primitives.safe_uint.Safe_UInt import Safe_UInt


class Safe_UInt__LLM__Max_Tokens(Safe_UInt):                                    # LLM max tokens parameter
    min_value : int = 1                                                         # Minimum 1 token required
    max_value : int = 200000                                                    # Maximum 200k tokens (Claude's limit)
