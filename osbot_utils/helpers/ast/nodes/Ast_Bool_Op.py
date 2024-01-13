from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Bool_Op(Ast_Node):

    def info(self):
        return {'Ast_Bool_Op': {'op'     : self.op    (),
                                'values' : self.values()}}