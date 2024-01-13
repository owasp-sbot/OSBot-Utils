from osbot_utils.utils.Dev import pprint
from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Generator_Exp(Ast_Node):

    def info(self):
        return {'Ast_Generator_Exp': {'elt'       : self.elt()       ,
                                      'generators': self.generators()}}