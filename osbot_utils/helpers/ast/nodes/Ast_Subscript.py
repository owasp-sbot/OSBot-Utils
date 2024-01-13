from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Subscript(Ast_Node):

    def info(self):
        return {'Ast_Subscript': {'ctx'  : self.ctx  (),
                                  'slice': self.slice(),
                                  'value': self.value()}}