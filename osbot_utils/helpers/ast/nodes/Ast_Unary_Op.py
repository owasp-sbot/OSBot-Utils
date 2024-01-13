from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Unary_Op(Ast_Node):

    def info(self):
        return {'Ast_Unary_Op': {'op'     : self.op()      ,
                                 'operand': self.operand()}}