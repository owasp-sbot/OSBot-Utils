from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Is(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Is]'

    def info(self):
        return {'Ast_Is': {}}