from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Unary_Op(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Unary_Op]'

    def info(self):
        return {'Ast_Unary_Op': {'op'     : self.op()      ,
                                 'operand': self.operand()}}