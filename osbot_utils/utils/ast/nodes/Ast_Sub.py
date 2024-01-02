from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Sub(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Sub]'

    def info(self):
        return {'Ast_Sub': {}}