from osbot_utils.type_safe.primitives.core.Safe_Int import Safe_Int

TYPE_SAFE_INT__POSITIVE__MIN_VALUE = 1

class Safe_Int__Positive(Safe_Int):              # Positive numbers → strictly greater than zero → 1, 2, 3, …
    min_value = TYPE_SAFE_INT__POSITIVE__MIN_VALUE