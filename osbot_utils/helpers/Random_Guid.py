# todo add to osbot utils
from osbot_utils.utils.Misc import random_guid

class Random_Guid(str):
    def __new__(cls, value=None):
        if value is None:
            value = random_guid()
        return str.__new__(cls, value)

    def __init__(self, value=None):
        self.value = value if value is not None else random_guid()

    def __str__(self):
        return self
