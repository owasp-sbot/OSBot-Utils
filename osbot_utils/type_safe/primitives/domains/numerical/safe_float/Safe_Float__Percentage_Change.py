from osbot_utils.type_safe.primitives.core.Safe_Float import Safe_Float


class Safe_Float__Percentage_Change(Safe_Float):        # Percentage change (positive or negative)
    min_value       = -1_000_000.0                      # Up to 10,000× slower
    max_value       =  1_000_000.0                      # Up to 10,000× faster
    decimal_places  = 2
    use_decimal     = True
    round_output    = True