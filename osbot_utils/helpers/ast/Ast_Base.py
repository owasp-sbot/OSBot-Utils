import ast
import inspect

from osbot_utils.utils.Dev          import pprint, jprint
from osbot_utils.utils.Exceptions   import syntax_error
from osbot_utils.utils.Files        import is_file, file_contents
from osbot_utils.utils.Objects      import obj_data, obj_info
from osbot_utils.utils.Str          import str_dedent


class Ast_Base:
    def __init__(self, node):
        if node.__module__ != 'ast':
             raise Exception(f'Expected node.__module__ to be ast, got: {node.__module__}')
        self.node      = node

    def __repr__(self):
        return self.__class__.__name__

    def is_ast(self, target):
        if hasattr(target, "__module__"):
            if target.__module__ == 'ast':
                return True
        return False

    def is_not_ast(self, target):
        return self.is_ast(target) is False

    def dump(self):
        return ast.dump(self.node, indent=4)

    def execute_code(self, exec_locals=None, exec_namespace=None):
        exec_locals    = exec_locals    or {}
        #exec_namespace = exec_namespace or {'__builtins__': {}}        # this has quite a lot of side effects
        exec_namespace = exec_namespace or {}
        exec_error  = None
        try:
            exec(self.source_code(), exec_namespace, exec_locals)
            status = 'ok'
        except Exception as error:
            status = 'error'
            exec_error = str(error)
        return { 'status'    : status         ,
                 'error'     : exec_error     ,
                 'locals'    : exec_locals    ,
                 'namespace' : exec_namespace }

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

    def jprint(self):
        return self.jprint_json()

    def jprint_json(self):
        jprint(self.json())

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

    def parse(self, target):
        try:
            if type(target) is str:
                if is_file(target):
                    source = file_contents(target)
                else:
                    source = target
            else:
                source = inspect.getsource(target)
            code = str_dedent(source)                         # remove any training spaces or it won't compile
            return ast.parse(code)
        except SyntaxError as error:
            raise syntax_error(error) from None

    def print(self):
        return self.print_dump()

    def print_dump(self):
        print(self.dump())
        return self

    def print_json(self):
        pprint(self.json())
        return self

    def print_obj_info(self):
        obj_info(self.node)
        return self

    def print_source_code(self):
        print(self.source_code())
        return self

    def source_code(self):
        return ast.unparse(self.node)



