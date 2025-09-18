from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash import Safe_Str__Cache_Hash
from osbot_utils.utils.Misc                                                              import random_bytes, bytes_sha256

class Random_Hash(Safe_Str__Cache_Hash, str):
    def __new__(cls, value=None):
        if not value:
            hash_obj = bytes_sha256(random_bytes())       # hash from 32 bytes of randomness
            value = hash_obj[:16]                         # Take first 16 chars to match Safe_Str__Cache_Hash

        return Safe_Str__Cache_Hash.__new__(cls, value)   # let Safe_Str__Cache_Hash handle the validation