import re
from osbot_utils.utils.Misc                     import random_id_short
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive


SAFE_ID__MAX_LENGTH     = 512
REGEX__SAFE_ID_REGEX    = re.compile(r'[^a-zA-Z0-9_-]')

class Safe_Id(Type_Safe__Primitive, str):
    def __new__(cls, value=None, max_length=SAFE_ID__MAX_LENGTH):
        if value is None:
            value = safe_id(random_id_short(prefix='safe-id'))
        sanitized_value = safe_id(value, max_length=max_length)
        return str.__new__(cls, sanitized_value)

    # def __str__(self):
    #     return self

def safe_id(value, max_length=36):
    if value is None or value == "":
        raise ValueError("Invalid ID: The ID must not be empty.")

    if not isinstance(value, str):
        value = str(value)

    if len(value) > max_length:
        raise ValueError(f"Invalid ID: The ID must not exceed {max_length} characters (was {len(value)}).")

    sanitized_value = REGEX__SAFE_ID_REGEX.sub('_', value)

    if set(sanitized_value) == {'_'}:
        raise ValueError("Invalid ID: The sanitized ID must not consist entirely of underscores.")

    return sanitized_value