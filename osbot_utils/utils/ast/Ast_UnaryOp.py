from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_UnaryOp(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_UnaryOp]'

    def info(self):
        return {'Ast_UnaryOp': {'op'     : self.op()      ,
                                'operand': self.operand()}}