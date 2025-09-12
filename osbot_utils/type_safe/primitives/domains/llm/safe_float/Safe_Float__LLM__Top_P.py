from osbot_utils.type_safe.primitives.core.Safe_Float import Safe_Float

class Safe_Float__LLM__Top_P(Safe_Float):                                       # LLM nucleus sampling parameter
    min_value      : float = 0.0                                                # Minimum 0.0 (deterministic)
    max_value      : float = 1.0                                                # Maximum 1.0 (consider all tokens)
    decimal_places : int   = 2                                                  # Two decimal precision
    clamp_to_range : bool  = True                                               # Auto-clamp values to valid range

    @classmethod
    def __default__value__(cls, var_type):
        return 0.9                                                              # Common default for balanced creativity