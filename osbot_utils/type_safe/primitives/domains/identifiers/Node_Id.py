from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id


class Node_Id(Obj_Id):                         # helper class so that we don't use Obj_Id to represent the graph_id class
    def __new__(cls, value=None):
        if value is None or value == '':
            return str.__new__(cls, '')
        else:
            return super(Obj_Id, cls).__new__(cls, value)