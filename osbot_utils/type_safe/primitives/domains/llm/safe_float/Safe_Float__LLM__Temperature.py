from osbot_utils.type_safe.primitives.core.Safe_Float import Safe_Float


class Safe_Float__LLM__Temperature(Safe_Float):                                   # LLM temperature parameter (0.0-2.0)
    min_value      : float = 0.0                                                  # Minimum temperature (deterministic)
    max_value      : float = 2.0                                                  # Maximum temperature (very creative)
    decimal_places : int   = 2                                                    # Two decimal precision
    clamp_to_range : bool  = True                                                 # Auto-clamp values to valid range