import ast

from osbot_utils.utils.ast.Ast_Node         import Ast_Node


class Ast_Module(Ast_Node):

    def data(self):
        return {}

    # todo: see if .info() is the best name for this
    #       I think .data() might be a better name
    #       with the name 'Ast_Module' moved into a variable (or retrieved from the class name)
    def info(self):
        return {'Ast_Module': {'body':self.body()  } }