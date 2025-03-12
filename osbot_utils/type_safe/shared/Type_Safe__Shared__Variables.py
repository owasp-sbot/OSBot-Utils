import types
from enum import EnumMeta

from osbot_utils.helpers.Safe_Id           import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str import Safe_Str

IMMUTABLE_TYPES = (bool, int, float, complex, str, bytes, types.NoneType, EnumMeta, type,
                   #Safe_Id, Safe_Str             # ok to add since these classes use str as a base class # todo: see if we still need these
                   )