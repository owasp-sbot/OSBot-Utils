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

    def ast_node(self, node):
        type_key      = type(node)
        resolved_type = type_registry.resolve(type_key)
        if resolved_type:
           return resolved_type(node)
        return Ast_Node(node)

    def info(self):
        return obj_data(self.node)

    def source_code(self):
        return ast.unparse(self.node)

