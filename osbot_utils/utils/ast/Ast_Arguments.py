import ast
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Arguments(Ast_Node):

    def __init__(self, args):
        if type(args) is not ast.arguments:
            raise Exception(f'Expected module to be of type ast.arguments, got: {args}')
        super().__init__(args)
        self.args = args

    def __repr__(self):
        return f'[Ast_Node][Ast_Arguments]'

    def info(self):
        return {'Ast_Args': {'args': self.names()}}

    def names(self):
        return [arg.arg for arg in self.args.args]
