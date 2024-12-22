from osbot_utils.utils.Misc import random_id_short
from osbot_utils.utils.Str  import safe_id

class Safe_Id(str):
    def __new__(cls, value=None, max_length=36):
        if value is None:
            value = safe_id(random_id_short('safe-id'))
        sanitized_value = safe_id(value, max_length=max_length)
        return str.__new__(cls, sanitized_value)

    def __str__(self):
        return self