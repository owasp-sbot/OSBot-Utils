import ast

from osbot_utils.utils.ast.Ast_Node         import Ast_Node


class Ast_Module(Ast_Node):

    module : ast.Module

    def __init__(self, module):
        if type(module) is not ast.Module:
            raise Exception(f'Expected module to be of type ast.Module, got: {module}')
        super().__init__(module)
        self.module = module

    def __repr__(self):
        return f'[Ast_Node][Ast_Module]'

    def source_code(self):
        return ast.unparse(self.module)

    def all_nodes(self):
        nodes = []
        for node in ast.walk(self.module):
            node = self.ast_node(node)
            nodes.append(node)
        return nodes

    def info(self):
        return {'Ast_Module': {'body': self.node.body } }     # todo: add parser to self.node.body