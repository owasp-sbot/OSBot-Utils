import types
from enum import EnumMeta

IMMUTABLE_TYPES = (bool, int, float, complex, str, tuple, frozenset, bytes, types.NoneType, EnumMeta, type)

class Type_Safe__Validation:
    pass


type_safe_validation = Type_Safe__Validation()
