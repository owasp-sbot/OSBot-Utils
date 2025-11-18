from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.enums.Enum__Hash__Algorithm import Enum__Hash__Algorithm


class Schema__Cache__Hash__Config(Type_Safe):                                      # Configuration for hash generation
    algorithm : Enum__Hash__Algorithm = Enum__Hash__Algorithm.SHA256               # Hash algorithm to use
    length    : int                   = 16                                         # Hash length: 10, 16, 32, 64, 96