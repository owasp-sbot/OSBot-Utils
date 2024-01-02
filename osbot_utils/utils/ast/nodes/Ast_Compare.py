from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Compare(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Compare]'

    def info(self):
        return {'Ast_Compare': { 'comparators'  : self.comparators(),
                                 'left'         : self.left       (),
                                 'ops'          : self.ops        ()}}