from osbot_utils.helpers.safe_float.Safe_Float import Safe_Float

class Safe_Float__Engineering(Safe_Float):          # Engineering calculations with controlled precision
    #decimal_places  = 6
    epsilon         = 1e-6
    round_output    = True
    use_decimal     = False                         # Performance over exactness