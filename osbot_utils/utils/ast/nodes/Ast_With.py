from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_With(Ast_Node):

    def info(self):
        return {'Ast_With': {'body' : self.body()      ,
                             'items': self.items()}}