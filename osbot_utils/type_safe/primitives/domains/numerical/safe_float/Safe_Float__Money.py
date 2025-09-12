from osbot_utils.type_safe.primitives.core.Safe_Float import Safe_Float


class Safe_Float__Money(Safe_Float):    # Money calculations with exact decimal arithmetic
    decimal_places  = 2
    use_decimal     = True              # Use Decimal internally
    allow_inf       = False
    allow_nan       = False
    min_value       = 0.0
    round_output    = True