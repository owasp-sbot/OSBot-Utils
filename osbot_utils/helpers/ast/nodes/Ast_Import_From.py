from osbot_utils.utils.Dev import pprint
from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Import_From(Ast_Node):

    def info(self):
        return {'Ast_Import_From': { 'level': self.level(), 'module': self.module(), 'names'  : self.names()  }}