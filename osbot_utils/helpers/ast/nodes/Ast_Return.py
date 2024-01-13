from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Return(Ast_Node):

    def info(self):
        return {'Ast_Return': { 'value': self.value()}}

