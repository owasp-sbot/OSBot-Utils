from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Slice(Ast_Node):

    def info(self):
        return {'Ast_Slice': {'lower': self.lower  (),
                              'step' : self.node.step,
                              'upper': self.upper()}}