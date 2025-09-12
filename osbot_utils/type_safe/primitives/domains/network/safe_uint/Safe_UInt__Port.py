from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt

TYPE_SAFE_UINT__PORT__MIN_VALUE = 0
TYPE_SAFE_UINT__PORT__MAX_VALUE = 65535

class Safe_UInt__Port(Safe_UInt):                         # Network port number (0-65535)

    min_value  = TYPE_SAFE_UINT__PORT__MIN_VALUE
    max_value  = TYPE_SAFE_UINT__PORT__MAX_VALUE
    allow_bool = False
    allow_none = False                                  # don't allow 0 as port value since that is a really weird value for a port