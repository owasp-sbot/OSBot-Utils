from osbot_utils.utils.Dev import pprint
from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Tuple(Ast_Node):

    def info(self):
        return {'Ast_Tuple': { 'ctx'  : self.ctx(),
                               'dims' : self.dims(),
                               'elts' : self.elts()}}