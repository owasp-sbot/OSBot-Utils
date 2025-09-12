from osbot_utils.type_safe.primitives.core.Safe_Float import Safe_Float


class Safe_Float__Percentage_Exact(Safe_Float):         # Exact percentage calculations
    min_value       = 0.0
    max_value       = 100.0
    decimal_places  = 2
    use_decimal     = True
    round_output    = True