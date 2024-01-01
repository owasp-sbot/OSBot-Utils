from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Attribute(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Attribute]'

    def info(self):
        return {'Ast_Attribute': { 'attr'  : self.node.attr  ,
                                   'ctx'   : self.ctx()}     ,
                                   'value' : self.value()    }