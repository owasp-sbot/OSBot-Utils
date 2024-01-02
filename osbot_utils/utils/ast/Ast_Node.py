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
        if self.node.body:
            return self.ast_nodes(self.node.body)

    def comparators(self):
        return self.ast_nodes(self.node.comparators)

    def ctx(self):
        return self.ast_node(self.node.ctx)

    def dims(self):
        return self.ast_nodes(self.node.dims)

    def elts(self):
        return self.ast_nodes(self.node.elts)

    def func(self):
        return self.ast_node(self.node.func)

    def ifs(self):
        return self.ast_nodes(self.node.ifs)

    def info(self):
        vars_to_del = ['col_offset', 'end_col_offset', 'lineno', 'end_lineno']
        data = obj_data(self.node)
        for var_to_del in vars_to_del:
            if data.get(var_to_del):
                del data[var_to_del]
        return data

    def iter(self):
        return self.ast_node(self.node.iter)

    def finalbody(self):
        return self.ast_nodes(self.node.finalbody)

    def handlers(self):
        return self.ast_nodes(self.node.handlers)

    def keys(self):
        return self.ast_nodes(self.node.keys)

    def keywords(self):
        return self.ast_nodes(self.node.keywords)

    def left(self):
        return self.ast_node(self.node.left)

    def lower(self):
        return self.ast_nodes(self.node.lower)

    def names(self):
        return self.ast_nodes(self.node.names)

    def op(self):
        return self.ast_node(self.node.op)

    def ops(self):
        return self.ast_nodes(self.node.ops)

    def orelse(self):
        return self.ast_nodes(self.node.orelse)

    def right(self):
        return self.ast_node(self.node.right)

    def print(self):
        obj_info(self.node)
        return self

    def slice(self):
        return self.ast_node(self.node.slice)

    def source_code(self):
        return ast.unparse(self.node)

    def target(self):
        return self.ast_node(self.node.target)

    def targets(self):
        return self.ast_nodes(self.node.targets)

    def test(self):
        return self.ast_node(self.node.test)

    def upper(self):
        return self.ast_nodes(self.node.upper)

    def value(self):
        if self.node.value is None:
            return None
        return self.ast_node(self.node.value)

    def values(self):
        return self.ast_nodes(self.node.values)

    def stats(self):
        types_stats = {}
        ast_stats   = {}
        for node in self.all_nodes():
            type_name = node.type_name
            ast_stat  = type(node).__name__
            if types_stats.get(type_name) is None:
                types_stats[type_name] = 0
            if ast_stats.get(ast_stat ) is None:
                ast_stats  [ast_stat ] = 0
            types_stats[type_name] += 1
            ast_stats  [ast_stat ] += 1
        stats = {'ast_types': ast_stats  ,
                 'types'    : types_stats}
        return stats

    # def returns(self):                                    # todo: add this when looking at type hints (which is what this is )
    #     if self.node.returns:
    #         return self.ast_node(self.node.returns)

