import ast

from osbot_utils.helpers.Type_Registry import type_registry
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects              import type_base_classes, obj_info, obj_data


class Ast_Node:

    def __init__(self, node):
        if node.__module__ != 'ast':
             raise Exception(f'Expected node.__module__ to be ast, got: {node.__module__}')
        self.node      = node
        self.type      = node.__class__
        self.type_name = node.__class__.__name__

    def __repr__(self):
        return f"[Ast_Node][????] {self.type}"

    def args(self):
        return self.ast_nodes(self.node.args)

    def ast_node(self, node):
        type_key      = type(node)
        resolved_type = type_registry.resolve(type_key)
        if resolved_type:
           return resolved_type(node)
        return Ast_Node(node)

    def ast_nodes(self, nodes):
        ast_nodes = []
        for node in nodes:
            ast_node = self.ast_node(node)
            ast_nodes.append(ast_node.info())           # todo: see the use of .info() here (should be better to return the ast_node)
        return ast_nodes

    def all_nodes(self):
        nodes = []
        for node in ast.walk(self.node):
            node = self.ast_node(node)
            nodes.append(node)
        return nodes

    def bases(self):
        return self.ast_nodes(self.node.bases)
        # nodes     = self.node.bases
        # ast_nodes = []
        # for node in nodes:
        #     ast_node = self.ast_node(node)
        #     ast_nodes.append(ast_node.info())
        # return ast_nodes

    def body(self):
        return self.ast_nodes(self.node.body)

    def ctx(self):
        return self.ast_node(self.node.ctx)

    def func(self):
        return self.ast_node(self.node.func)

    def info(self):
        return obj_data(self.node)

    def keys(self):
        return self.ast_nodes(self.node.keys)

    def keywords(self):
        return self.ast_nodes(self.node.keywords)

    def print(self):
        obj_info(self.node)
        return self

    def source_code(self):
        return ast.unparse(self.node)

    def targets(self):
        return self.ast_nodes(self.node.targets)

    def value(self):
        return self.ast_node(self.node.value)

    def values(self):
        return self.ast_nodes(self.node.values)

    def stats(self):
        types_stats = {}
        for node in self.all_nodes():
            type_name = node.type_name
            if types_stats.get(type_name) is None:
                types_stats[type_name] = 0
            types_stats[type_name] += 1
        stats = {'types': types_stats}
        return stats

    # def returns(self):                                    # todo: add this when looking at type hints (which is what this is )
    #     if self.node.returns:
    #         return self.ast_node(self.node.returns)

