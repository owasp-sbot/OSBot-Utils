import re
from osbot_utils.type_safe.primitives.core.Safe_Str                         import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode

TYPE_SAFE_STR__NACL__PRIVATE_KEY__REGEX  = re.compile(r'^[a-fA-F0-9]{64}$')
TYPE_SAFE_STR__NACL__PRIVATE_KEY__LENGTH = 64  # 32 bytes as hex = 64 characters

class Safe_Str__NaCl__Private_Key(Safe_Str):
    """
    Safe string class for NaCl (Curve25519) private keys in hexadecimal format.

    NaCl private keys are 32 bytes (256 bits), represented as 64 hexadecimal characters.
    These keys are used with libsodium/PyNaCl for asymmetric encryption.

    Examples:
    - "d4c8f7e3a2b1c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3"
    - "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

    Security Note: Private keys should NEVER be exposed or logged.
    """
    regex             = TYPE_SAFE_STR__NACL__PRIVATE_KEY__REGEX
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    max_length        = TYPE_SAFE_STR__NACL__PRIVATE_KEY__LENGTH
    exact_length      = True
    allow_empty       = True
    trim_whitespace   = True
    strict_validation = True
