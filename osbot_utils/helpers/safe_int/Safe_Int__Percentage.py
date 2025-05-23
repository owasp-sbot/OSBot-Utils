from osbot_utils.helpers.safe_int.Safe_Int import Safe_Int

TYPE_SAFE_INT__PERCENTAGE__MIN_VALUE = 0
TYPE_SAFE_INT__PERCENTAGE__MAX_VALUE = 100

class Safe_Int__Percentage(Safe_Int):           # Percentage value (0-100)

    min_value = TYPE_SAFE_INT__PERCENTAGE__MIN_VALUE
    max_value = TYPE_SAFE_INT__PERCENTAGE__MAX_VALUE
    allow_bool = False