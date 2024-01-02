from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Alias(Ast_Node):

    def info(self):
        return {'Ast_Alias': { 'asname'  : self.node.asname , 'name': self.node.name }}