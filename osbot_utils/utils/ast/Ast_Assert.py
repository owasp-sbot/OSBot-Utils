from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Assert(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Assert]'

    def info(self):
        return {'Ast_Assert': { 'msg'  : self.node.msg ,
                                'test' : self.test()   }}