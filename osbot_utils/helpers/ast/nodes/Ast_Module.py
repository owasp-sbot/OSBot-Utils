import ast

from osbot_utils.helpers.ast.Ast_Node         import Ast_Node


class Ast_Module(Ast_Node):

    def __init__(self, target):
        if self.is_not_ast(target):
            target = self.parse(target)
        super().__init__(target)

    # def body(self):
    #     return self.node.body

    # todo: see if .info() is the best name for this
    #       I think .data() might be a better name
    #       with the name 'Ast_Module' moved into a variable (or retrieved from the class name)
    def info(self):
        return {'Ast_Module': {'body':self.body()  } }