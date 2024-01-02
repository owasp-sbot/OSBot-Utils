from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Bin_Op(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Bin_Op]'

    def info(self):
        return {'Ast_Bin_Op': {'left' : self.left (),
                               'op'   : self.op   (),
                               'right': self.right()}}