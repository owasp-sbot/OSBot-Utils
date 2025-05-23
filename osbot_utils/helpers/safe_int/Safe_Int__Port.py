from osbot_utils.helpers.safe_int.Safe_Int import Safe_Int

TYPE_SAFE_INT__PORT__MIN_VALUE = 0
TYPE_SAFE_INT__PORT__MAX_VALUE = 65535

class Safe_Int__Port(Safe_Int):                         # Network port number (0-65535)

    min_value  = TYPE_SAFE_INT__PORT__MIN_VALUE
    max_value  = TYPE_SAFE_INT__PORT__MAX_VALUE
    allow_bool = False
    allow_none = False                                  # don't allow 0 as port value since that is a really weird value for a port