from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_If(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_If]'

    def info(self):
        return {'Ast_If': { 'body'  : self.body()  ,
                            'test'  : self.test()  ,
                            'orelse': self.orelse()}}