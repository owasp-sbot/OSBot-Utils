

class Random_Guid(str):
    def __new__(cls, value=None):
        from osbot_utils.utils.Misc import random_guid, is_guid

        if value is None:
            value = random_guid()
        if is_guid(value):
            return str.__new__(cls, value)
        raise ValueError(f'in Random_Guid: value provided was not a Guid: {value}')

    def __str__(self):
        return self