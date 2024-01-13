from osbot_utils.utils.Dev import pprint
from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_If(Ast_Node):

    def info(self):
        return {'Ast_If': { 'body'  : self.body()  ,
                            'test'  : self.test()  ,
                            'orelse': self.orelse()}}