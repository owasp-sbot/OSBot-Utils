import ast
import inspect

from osbot_utils.utils.Str                  import str_dedent
from osbot_utils.utils.ast.nodes.Ast_Module import Ast_Module


class Ast:

    def __init__(self):
        pass

    def source_code__from(self, target):
        source_raw = inspect.getsource(target)
        source     = str_dedent(source_raw)             # remove any training spaces or it won't compile
        return source

    def ast_module__from(self, target):
        source_code = self.source_code__from(target)
        return self.ast_module__from_source_code(source_code)

    def ast_module__from_source_code(self, source_code):
        result = ast.parse(source_code)
        if type(result) is ast.Module:
            return Ast_Module(result)

    def parse(self, source_code):
        return ast.parse(source_code)


