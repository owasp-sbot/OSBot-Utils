from osbot_utils.utils.Dev import pprint
from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_List(Ast_Node):

    def info(self):
        return {'Ast_List': { 'ctx'  : self.ctx() ,
                              'elts' : self.elts()}}