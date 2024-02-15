from osbot_utils.utils.Dev import pprint
from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_If_Exp(Ast_Node):

    def info(self):
        return {'Ast_If_Exp': { 'body'  : self.body  (),        # note: body is not an array here
                                'orelse': self.orelse(),
                                'test'  : self.test  ()}}