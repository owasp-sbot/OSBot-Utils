from osbot_utils.utils.ast.Ast_Node import Ast_Node


class Ast_Argument(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Argument]'

    def info(self):
        return {'Ast_Argument': {'arg': self.node.arg}}