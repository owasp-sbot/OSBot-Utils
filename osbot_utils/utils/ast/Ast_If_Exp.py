from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_If_Exp(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_If_Exp]'

    def info(self):
        return {'Ast_If_Exp': { 'body'  : self.body  (),        # note: body is not an array here
                                'orelse': self.orelse(),
                                'test'  : self.test  ()}}