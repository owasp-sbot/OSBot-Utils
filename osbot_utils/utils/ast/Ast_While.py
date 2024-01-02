from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_While(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_While]'

    def info(self):
        return {'Ast_While': {'body'  : self.body  (),
                              'orelse': self.orelse(),
                              'test'  : self.test  ()}}