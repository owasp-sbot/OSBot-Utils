from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Eq(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Eq]'

    def info(self):
        return {'Ast_Eq': {}}