import ast
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Arguments(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Arguments]'

    def info(self):
        return {'Ast_Arguments': {'args': self.args()}}

    # def names(self):
    #     return [arg.arg for arg in self.args.args]
