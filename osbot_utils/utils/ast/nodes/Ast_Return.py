from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Return(Ast_Node):

    def info(self):
        return {'Ast_Return': { 'value': self.value()}}

