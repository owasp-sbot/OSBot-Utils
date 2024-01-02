from osbot_utils.utils.ast.Ast_Load import Ast_Load


class Ast_Data:

    def __init__(self):
        self.ast_load = Ast_Load()
        self.ast_nodes   = self.ast_load.ast_nodes

    def add_file(self, target):
        self.ast_load.load_file(target)
        return self

    def add_files(self, target):
        self.ast_load.load_files(target)
        return self

    def add_target(self, target):
        self.ast_load.load_target(target)
        return self

    def modules(self):
        return self.ast_nodes.get('Ast_Module', [])

    def stats(self):
        return self.ast_load.stats()