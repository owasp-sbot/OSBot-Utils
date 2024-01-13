from osbot_utils.utils.Dev import pprint
from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Comprehension(Ast_Node):

    def info(self):
        return {'Ast_Comprehension': {'ifs'     : self.ifs(),
                                      'is_async': self.node.is_async,
                                      'iter'    : self.iter(),
                                      'target'  : self.target()}}