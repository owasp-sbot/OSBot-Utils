from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_For(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_For]'

    def info(self):
        return {'Ast_For': { 'body'  : self.body(),
                             'iter'  : self.iter(),
                             'orelse': self.orelse(),
                             'target': self.target()}}