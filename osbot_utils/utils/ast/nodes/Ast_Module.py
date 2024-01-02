import ast

from osbot_utils.utils.ast.Ast_Node         import Ast_Node


class Ast_Module(Ast_Node):

    # todo: see if we still need this (and if there is a better way to show it,
    #       specially after we refactor the info() method
    def __repr__(self):
        return f'[Ast_Node][Ast_Module]'

    # todo: see if .info() is the best name for this
    #       I think .data() might be a better name
    #       with the name 'Ast_Module' moved into a variable (or retrieved from the class name)
    def info(self):
        return {'Ast_Module': {'body':self.body()  } }