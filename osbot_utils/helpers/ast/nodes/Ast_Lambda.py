from osbot_utils.utils.Dev import pprint
from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Lambda(Ast_Node):

    def info(self):
        return {'Ast_Lambda': { 'args' : self.args()  ,
                                'body' : self.body() }}