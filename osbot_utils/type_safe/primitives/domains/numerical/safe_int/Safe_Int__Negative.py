from osbot_utils.type_safe.primitives.core.Safe_Int import Safe_Int

TYPE_SAFE_INT__NEGATIVE__MAX_VALUE = -1

class Safe_Int__Negative(Safe_Int):              # Negative numbers → strictly less than zero → −1, −2, −3, …
    max_value = TYPE_SAFE_INT__NEGATIVE__MAX_VALUE