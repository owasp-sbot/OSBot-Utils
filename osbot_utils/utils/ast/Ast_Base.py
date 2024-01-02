import ast

from osbot_utils.utils.Objects import obj_data, obj_info


class Ast_Base:

    def __init__(self, node):
        if node.__module__ != 'ast':
             raise Exception(f'Expected node.__module__ to be ast, got: {node.__module__}')
        self.node      = node

    def info(self):
        vars_to_del = ['col_offset', 'end_col_offset', 'lineno', 'end_lineno', 'type_comment']
        data = self.obj_data()
        for var_to_del in vars_to_del:
            if data.get(var_to_del):
                del data[var_to_del]
        return data

    def print(self):
        obj_info(self.node)
        return self

    def obj_data(self):
        return obj_data(self.node)

    def source_code(self):
        return ast.unparse(self.node)
