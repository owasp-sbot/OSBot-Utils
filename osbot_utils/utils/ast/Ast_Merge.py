from osbot_utils.utils.ast import Ast_Module


class Ast_Merge:

    def __init__(self):
        self.module = Ast_Module("")                    # create an empty Ast_Module

    def merge_module(self, module_to_merge):
        if type(module_to_merge) is Ast_Module:
            nodes_to_add = module_to_merge.node.body
            self.module.node.body.extend(nodes_to_add)
            return True
        return False

    def source_code(self):
        return self.module.source_code()