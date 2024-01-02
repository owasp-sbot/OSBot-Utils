from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_List_Comp(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_List_Comp]'

    def info(self):
        return {'Ast_List_Comp': { 'elt'        : self.elt()        ,
                                   'generators' : self.generators() }}