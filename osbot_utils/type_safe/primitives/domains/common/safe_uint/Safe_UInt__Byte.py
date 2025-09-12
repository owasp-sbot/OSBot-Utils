from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt

TYPE_SAFE_UINT__BYTE__MIN_VALUE = 0
TYPE_SAFE_UINT__BYTE__MAX_VALUE = 255

class Safe_UInt__Byte(Safe_UInt):           # Single byte value (0-255)

    min_value = TYPE_SAFE_UINT__BYTE__MIN_VALUE
    max_value = TYPE_SAFE_UINT__BYTE__MAX_VALUE
    allow_bool = False