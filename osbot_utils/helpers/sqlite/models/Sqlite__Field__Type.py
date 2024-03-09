from decimal import Decimal
from enum import Enum, auto

from osbot_utils.decorators.methods.cache import cache


class Sqlite__Field__Type(Enum):
    DECIMAL = Decimal
    INTEGER = int
    TEXT    = str
    BLOB    = bytes
    REAL    = float
    NUMERIC = auto()

    @classmethod
    @cache
    def type_map(cls):
        type_map = {}
        for member in cls:
            if member.value not in [auto(), None]:
                type_map[member.value] = member
        return type_map

    @classmethod
    @cache
    def enum_map(cls):
        return {member.name: member.value for member in cls}

