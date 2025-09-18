from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive

class Random_Guid(Type_Safe__Primitive, str):
    def __new__(cls, value=None):
        from osbot_utils.utils.Misc import random_guid, is_guid

        if value is None:
            value = random_guid()
        if is_guid(value):
            return str.__new__(cls, value)
        raise ValueError(f'in Random_Guid: value provided was not a Guid: {value}')
