import ast

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import obj_data, obj_info


class Ast_Base:
    def __init__(self, node):
        if node.__module__ != 'ast':
             raise Exception(f'Expected node.__module__ to be ast, got: {node.__module__}')
        self.node      = node

    def __repr__(self):
        return self.__class__.__name__

    def info(self):
        return {}                   # to be overwritten by calles that uses this base class

    def json_data(self, target):
        if type(target) is dict:
            data = {}
            for key, value in target.items():
                data[key] = self.json_data(value)
            return data
        if type(target) is list:
            data = []
            for item in target:
                data.append(self.json_data(item))
            return data
        if isinstance(target, Ast_Base):
            return self.json_data(target.info())
        return target

    def json(self):
        return self.json_data(self.info())

    def key(self):
        return str(self)

    def obj_data(self, remove_source_info=True):
        data = obj_data(self.node)
        if remove_source_info:
            vars_to_del = ['col_offset', 'end_col_offset', 'lineno', 'end_lineno', 'type_comment']
            for var_to_del in vars_to_del:
                if data.get(var_to_del):
                    del data[var_to_del]
        return data

    def print(self):
        obj_info(self.node)
        return self

    def source_code(self):
        return ast.unparse(self.node)

