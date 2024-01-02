from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Expr(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Expr]'

    def info(self):
        return {'Ast_Expr': { 'value'  : self.value()  }}