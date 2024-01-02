from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Return(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Return]'

    def info(self):
        return {'Ast_Return': { 'value': self.value().info()}}

    # def value(self):
    #     return_node = self.ast_node(self.node.value)
    #     return return_node.info()
