from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Assert(Ast_Node):

    def info(self):
        return {'Ast_Assert': { 'msg'  : self.msg() ,
                                'test' : self.test()   }}