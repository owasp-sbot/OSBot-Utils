from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Generator_Exp(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Generator_Exp]'

    def info(self):
        return {'Ast_Generator_Exp': {'elt'       : self.elt()       ,
                                      'generators': self.generators()}}