from osbot_utils.utils.Dev import pprint
from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Except_Handler(Ast_Node):

    def info(self):
        return {'Ast_Except_Handler': { 'body': self.body()    ,
                                        'name': self.node.name ,
                                        'type': self.type()    }}