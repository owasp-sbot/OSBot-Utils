from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_List(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_List]'

    def info(self):
        return {'Ast_List': { 'ctx'  : self.ctx() ,
                              'elts' : self.elts()}}