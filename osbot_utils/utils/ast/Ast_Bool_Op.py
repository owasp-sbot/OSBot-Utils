from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Bool_Op(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Bool_Op]'

    def info(self):
        return {'Ast_Bool_Op': {'op'     : self.op    (),
                                'values' : self.values()}}