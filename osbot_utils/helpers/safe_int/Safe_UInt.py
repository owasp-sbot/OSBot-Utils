from osbot_utils.helpers.safe_int.Safe_Int import Safe_Int

class Safe_UInt(Safe_Int):             # Unsigned Integer - only accepts non-negative integer values

    min_value  = 0       # Unsigned means >= 0
    max_value  = None    # No upper limit by default
    allow_bool = False  # Don't allow True/False as 1/0