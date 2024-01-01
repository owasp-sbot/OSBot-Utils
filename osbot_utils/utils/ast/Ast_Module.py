import ast

from osbot_utils.utils.ast.Ast_Node         import Ast_Node


class Ast_Module(Ast_Node):

    module : ast.Module

    def __init__(self, module):
        if type(module) is not ast.Module:
            raise Exception(f'Expected module to be of type ast.Module, got: {module}')
        super().__init__(module)
        self.module = module

    def __repr__(self):
        return f'[Ast_Node][Ast_Module]'

    def source_code(self):
        return ast.unparse(self.module)


    def info(self):                             # todo: see if .info() is the best name for this
        return {'Ast_Module': {'body':self.body()  } }