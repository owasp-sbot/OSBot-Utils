import types
from enum import EnumMeta

from osbot_utils.helpers.Safe_Id            import Safe_Id

IMMUTABLE_TYPES = (bool, int, float, complex, str, bytes, types.NoneType, EnumMeta, type,
                   Safe_Id          # ok to add since these classes use str as a base class
                   )