from decimal import Decimal
from enum import Enum, auto
from types import NoneType

from osbot_utils.decorators.methods.cache import cache


class Sqlite__Field__Type(Enum):
    DECIMAL = Decimal
    INTEGER = int
    TEXT    = str
    BLOB    = bytes
    REAL    = float
    NUMERIC = 'numeric'                         # special case to have some support for using NUMERIC in the Create Table
    UNKNOWN = NoneType                          # special type to handle cases when the type is not known # todo: handle this on the table creation stage

    def __repr__(self):
        return f'sqlite.{self.name}'

    @classmethod
    @cache
    def type_map(cls):
        type_map = {}
        for member in cls:
            if member.value not in [auto()]:
                type_map[member.value] = member
        return type_map

    @classmethod
    @cache
    def enum_map(cls):
        return {member.name: member.value for member in cls}

