from osbot_utils.utils.Files import is_file, file_contents
from osbot_utils.helpers.ast import Ast_Module
from osbot_utils.helpers.ast.Ast_Data import Ast_Data


class Ast_Merge:

    def __init__(self):
        self.module = Ast_Module("")                    # create an empty Ast_Module
        self.ast_data = Ast_Data(self.module)

    def merge_file(self, file_to_merge):
        if is_file(file_to_merge):
            ast_module = Ast_Module(file_to_merge)
            return self.merge_module(ast_module)
        return False

    def merge_module(self, module_to_merge):
        if type(module_to_merge) is Ast_Module:
            nodes_to_add = module_to_merge.node.body
            self.module.node.body.extend(nodes_to_add)
            return True
        return False

    def source_code(self):
        return self.module.source_code()