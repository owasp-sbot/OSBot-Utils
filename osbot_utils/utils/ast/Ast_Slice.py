from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Slice(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Slice]'

    def info(self):
        return {'Ast_Slice': {'lower': self.lower  (),
                              'step' : self.node.step,
                              'upper': self.upper()}}