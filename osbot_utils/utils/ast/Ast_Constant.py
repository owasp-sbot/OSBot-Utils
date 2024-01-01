from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Constant(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Constant]'

    def info(self):
        return {'Ast_Constant': {'value': self.node.value}}