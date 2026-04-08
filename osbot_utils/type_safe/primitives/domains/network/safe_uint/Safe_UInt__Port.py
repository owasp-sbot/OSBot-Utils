from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt

TYPE_SAFE_UINT__PORT__MIN_VALUE = 0
TYPE_SAFE_UINT__PORT__MAX_VALUE = 65535

class Safe_UInt__Port(Safe_UInt):                         # Network port number (0-65535)

    min_value  = TYPE_SAFE_UINT__PORT__MIN_VALUE
    max_value  = TYPE_SAFE_UINT__PORT__MAX_VALUE