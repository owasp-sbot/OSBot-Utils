from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Not_In(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Not_In]'

    def info(self):
        return {'Ast_Not_In': {}}