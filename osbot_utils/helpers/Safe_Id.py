from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive
from osbot_utils.utils.Misc                     import random_id_short
from osbot_utils.utils.Str                      import safe_id

SAFE_ID__MAX_LENGTH = 512

class Safe_Id(Type_Safe__Primitive, str):
    def __new__(cls, value=None, max_length=SAFE_ID__MAX_LENGTH):
        if value is None:
            value = safe_id(random_id_short('safe-id'))
        sanitized_value = safe_id(value, max_length=max_length)
        return str.__new__(cls, sanitized_value)

    # def __str__(self):
    #     return self


# note: here is the regex applied on safe_id:  REGEX__SAFE_ID_REGEX       = re.compile(r'[^a-zA-Z0-9_-]')