from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_While(Ast_Node):

    def info(self):
        return {'Ast_While': {'body'  : self.body  (),
                              'orelse': self.orelse(),
                              'test'  : self.test  ()}}