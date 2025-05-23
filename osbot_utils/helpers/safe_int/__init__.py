from osbot_utils.helpers.safe_int.Safe_Int import Safe_Int

TYPE_SAFE_INT__BYTE__MIN_VALUE = 0
TYPE_SAFE_INT__BYTE__MAX_VALUE = 255

class Safe_Int__Byte(Safe_Int): # Single byte value (0-255)

    min_value = TYPE_SAFE_INT__BYTE__MIN_VALUE
    max_value = TYPE_SAFE_INT__BYTE__MAX_VALUE
    allow_bool = False