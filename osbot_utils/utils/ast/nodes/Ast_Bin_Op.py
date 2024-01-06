from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Bin_Op(Ast_Node):

    def info(self):
        return {'Ast_Bin_Op': {'left' : self.left (),
                               'op'   : self.op   (),
                               'right': self.right()}}