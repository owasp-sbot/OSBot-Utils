from osbot_utils.utils.Misc                     import random_guid_short
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive


class Random_Guid_Short(Type_Safe__Primitive, str):
    def __new__(cls, value=None):
        if value is None:
            value = random_guid_short()
        return str.__new__(cls, value)

    def __init__(self, value=None):
        self.value = value if value is not None else random_guid_short()

    def __str__(self):
        return self
