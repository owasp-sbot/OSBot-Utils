from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_BinOp(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_BinOp]'

    def info(self):
        return {'Ast_BinOp': {'left' : self.left (),
                              'op'   : self.op   (),
                              'right': self.right()}}