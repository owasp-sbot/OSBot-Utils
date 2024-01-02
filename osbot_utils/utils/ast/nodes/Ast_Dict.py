from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Dict(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Dict]'

    def info(self):
        return {'Ast_Dict': { 'keys'  : self.keys()  ,
                              'values': self.values()}}