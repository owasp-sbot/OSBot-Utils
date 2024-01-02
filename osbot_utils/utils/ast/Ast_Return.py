from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Return(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Return]'

    def info(self):
        value = self.value()
        if value:
            return {'Ast_Return': { 'value': value.info()}}
        return {'Ast_Return': { 'value': None}}

    # def value(self):
    #     return_node = self.ast_node(self.node.value)
    #     return return_node.info()

