from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt

TYPE_SAFE_UINT__PERCENTAGE__MIN_VALUE = 0
TYPE_SAFE_UINT__PERCENTAGE__MAX_VALUE = 100

class Safe_UInt__Percentage(Safe_UInt):           # Percentage value (0-100)

    min_value = TYPE_SAFE_UINT__PERCENTAGE__MIN_VALUE
    max_value = TYPE_SAFE_UINT__PERCENTAGE__MAX_VALUE
    allow_bool = False