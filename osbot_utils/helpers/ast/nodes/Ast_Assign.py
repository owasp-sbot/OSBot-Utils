from osbot_utils.utils.Dev import pprint
from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Assign(Ast_Node):

    def info(self):
        return {'Ast_Assign': {'targets': self.targets(),
                               'value'  : self.value()  }}