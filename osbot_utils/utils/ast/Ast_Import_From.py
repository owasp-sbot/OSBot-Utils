from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Import_From(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Import_From]'

    def info(self):
        return {'Ast_Import_From': { 'names'  : self.names()  }}