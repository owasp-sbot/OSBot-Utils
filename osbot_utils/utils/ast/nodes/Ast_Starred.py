from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Starred(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Starred]'

    def info(self):
        return {'Ast_Starred': {'ctx': self.ctx(),
                                'value': self.value()}}