import hashlib
import re
import random
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive

_regex_obj_id = re.compile(r'^[0-9a-f]{8}$')

def is_obj_id(value):
    if isinstance(value, Obj_Id):
        return True
    if isinstance(value, str) and len(value) == 8:
        return _regex_obj_id.match(value) is not None
    return False

def new_obj_id():
    return hex(random.getrandbits(32))[2:].zfill(8)

class Obj_Id(Type_Safe__Primitive, str):
    def __new__(cls, value: str = None):
        if value:
            if is_obj_id(value):
                obj_id = value
            else:
                raise ValueError(f'in {cls.__name__}: value provided was not a valid {cls.__name__}: {value}')
        else:
            obj_id = new_obj_id()
        return super().__new__(cls, obj_id)

    def __str__(self):
        return str.__str__(self)

    def __add__(self, other):                                           # Concatenation returns plain str, not Obj_Id
        return str.__str__(self) + other

    def __radd__(self, other):                                          # Reverse concatenation returns plain str
        return other + str.__str__(self)

    @classmethod
    def from_seed(cls, seed: str) -> 'Obj_Id':                                       # Create deterministic ID from seed
        if not seed:                                                                 # Seed cannot be empty
            raise ValueError("Seed string cannot be empty")
        hash_bytes  = hashlib.sha256(seed.encode('utf-8')).digest()                  # SHA256 hash of seed
        deterministic_id = hash_bytes.hex()[:8]                                      # First 8 hex chars
        return cls(deterministic_id)