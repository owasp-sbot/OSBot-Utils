import types
from enum import EnumMeta


IMMUTABLE_TYPES = (bool, int, float, complex, str, tuple, frozenset, bytes, types.NoneType, EnumMeta, type)