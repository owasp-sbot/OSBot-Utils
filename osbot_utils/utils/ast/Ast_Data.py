from osbot_utils.utils.Misc import wait_for
from osbot_utils.utils.ast.Ast_Visitor import Ast_Visitor


class Ast_Data:

    def __init__(self):
        self.ast_visitor = Ast_Visitor()
        self.ast_nodes   = self.ast_visitor.ast_nodes

    def add_file(self, target):
        self.ast_visitor.add_file(target)
        return self

    def add_files(self, target):
        self.ast_visitor.add_files(target)
        return self

    def add_target(self, target):
        self.ast_visitor.add_target(target)
        return self

    def modules(self):
        return self.ast_nodes.get('Ast_Module', [])

    def stats(self):
        return self.ast_visitor.stats()