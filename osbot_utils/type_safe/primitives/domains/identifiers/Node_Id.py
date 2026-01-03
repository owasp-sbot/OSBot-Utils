from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id


class Node_Id(Obj_Id):
    def __new__(cls, value=None):
        if value is None or value == '':
            return str.__new__(cls, '')
        else:
            return super().__new__(cls, value)