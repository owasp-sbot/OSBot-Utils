from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Subscript(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Subscript]'

    def info(self):
        return {'Ast_Subscript': {'ctx'  : self.ctx  (),
                                  'slice': self.slice(),
                                  'value': self.value()}}