from osbot_utils.type_safe.primitives.core.Safe_Float import Safe_Float


class Safe_Float__Scientific(Safe_Float):
    allow_inf       = True
    allow_nan       = True
    decimal_places  = 15
    use_decimal     = False