import types
from enum import EnumMeta

IMMUTABLE_TYPES = (bool, int, float, complex, str, bytes, types.NoneType, EnumMeta, type)