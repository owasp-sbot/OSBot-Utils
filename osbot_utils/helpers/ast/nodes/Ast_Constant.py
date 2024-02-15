from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Constant(Ast_Node):

    def info(self):
        return {'Ast_Constant': {'value': self.value()}}     # we need to use the actual value here