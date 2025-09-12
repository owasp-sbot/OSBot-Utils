import random
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive

_hex_table = [f"{i:02x}" for i in range(256)]

def is_obj_id(value: str):
    var_type = type(value)
    if var_type is Obj_Id:
        return True
    if var_type is str:
        if len(value) == 8:         # todo: add efficient check if we only have hex values
            return True
    return False

def new_obj_id():
    return hex(random.getrandbits(32))[2:].zfill(8)  # slice off '0x' and pad

class Obj_Id(Type_Safe__Primitive,str):
    def __new__(cls, value: str=None):
        if value:
            if is_obj_id(value):
                obj_id = value
            else:
                raise ValueError(f'in Obj_Id: value provided was not a valid Obj_Id: {value}')
        else:
            obj_id = new_obj_id()
        return super().__new__(cls, obj_id)                                          # Return a new instance of Guid initialized with the string version of the UUID

    def __str__(self):
        return self