from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Assert(Ast_Node):

    def info(self):
        return {'Ast_Assert': { 'msg'  : self.msg() ,
                                'test' : self.test()   }}