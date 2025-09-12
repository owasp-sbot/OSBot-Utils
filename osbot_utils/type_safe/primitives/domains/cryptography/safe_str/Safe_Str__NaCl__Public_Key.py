import re
from osbot_utils.type_safe.primitives.core.Safe_Str                         import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode

TYPE_SAFE_STR__NACL__PUBLIC_KEY__REGEX  = re.compile(r'^[a-fA-F0-9]{64}$')
TYPE_SAFE_STR__NACL__PUBLIC_KEY__LENGTH = 64  # 32 bytes as hex = 64 characters

# todo: refactor this with  Safe_Str__NaCl__Private_Key since the code is just about the same
class Safe_Str__NaCl__Public_Key(Safe_Str):
    """
    Safe string class for NaCl (Curve25519) public keys in hexadecimal format.

    NaCl public keys are 32 bytes (256 bits), represented as 64 hexadecimal characters.
    These keys are used with libsodium/PyNaCl for asymmetric encryption using SealedBox.

    Examples:
    - "a1b2c3d4e5f6789012345678901234567890abcdefabcdefabcdefabcdefabcd"
    - "fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210"

    Security Note: Public keys can be safely shared and transmitted.
    """
    regex             = TYPE_SAFE_STR__NACL__PUBLIC_KEY__REGEX
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    max_length        = TYPE_SAFE_STR__NACL__PUBLIC_KEY__LENGTH
    exact_length      = True
    allow_empty       = True
    trim_whitespace   = True
    strict_validation = True