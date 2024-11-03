from osbot_utils.utils.Str import safe_id

class Safe_Id(str):
    def __new__(cls, value):
        sanitized_value = safe_id(value)
        return str.__new__(cls, sanitized_value)

    def __str__(self):
        return self