from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_BoolOp(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_BoolOp]'

    def info(self):
        return {'Ast_BoolOp': {'op'     : self.op    (),
                               'values' : self.values()}}