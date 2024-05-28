import ast
import inspect
from osbot_utils.utils.Files                    import file_contents
from osbot_utils.utils.Str                      import str_dedent
from osbot_utils.helpers.ast.nodes.Ast_Module   import Ast_Module


class Ast:

    def __init__(self):
        pass

    def source_code__from(self, target):
        try:
            source_raw = inspect.getsource(target)
            source     = str_dedent(source_raw)             # remove any training spaces or it won't compile
            return source
        except:
            return None

    def ast_module__from(self, target):
        source_code = self.source_code__from(target)
        ast_module = self.ast_module__from_source_code(source_code)
        return ast_module

    def ast_module__from_file(self, path_file):
        source_code = file_contents(path_file)
        return self.ast_module__from_source_code(source_code)

    def ast_module__from_source_code(self, source_code):
        result = ast.parse(source_code)
        if type(result) is ast.Module:
            return Ast_Module(result)

    def parse(self, source_code):
        return ast.parse(source_code)


