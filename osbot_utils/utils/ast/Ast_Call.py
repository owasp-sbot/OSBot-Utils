from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Call(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Call]'

    def info(self):
        return {'Ast_Call': { 'args'  : self.args()      ,
                              'func'  : self.func()      ,
                              'keywords': self.keywords()}}