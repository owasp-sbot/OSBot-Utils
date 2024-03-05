from enum import auto, Enum

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

class Sqlite__Field__Type(Enum):
    INTEGER = 1

class Sqlite__Field(Kwargs_To_Self):
    cid        : int
    name       : str
    type       : Sqlite__Field__Type = Sqlite__Field__Type.INTEGER
    notnull    : int
    dflt_value : None
    pk         : int