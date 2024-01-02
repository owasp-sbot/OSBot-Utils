from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Aug_Assign(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Aug_Assign]'

    def info(self):
        return {'Ast_Aug_Assign': { 'op'    : self.op    (),
                                    'target': self.target(),
                                    'value' : self.value ()}}