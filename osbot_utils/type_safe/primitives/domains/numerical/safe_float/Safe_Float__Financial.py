from osbot_utils.type_safe.primitives.core.Safe_Float import Safe_Float

class Safe_Float__Financial(Safe_Float):
        decimal_places = 2
        use_decimal    = True
        allow_inf      = False
        allow_nan      = False
        round_output   = True