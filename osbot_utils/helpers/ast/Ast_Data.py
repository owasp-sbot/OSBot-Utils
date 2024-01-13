from osbot_utils.helpers.ast import Ast_Module

class Ast_Data:

    def __init__(self, target):
        if type(target) is Ast_Module:
            self.target = target
        else:
            self.target = Ast_Module(target)
        self.ast_visit = None

    # def add_file(self, target):
    #     self.ast_load.load_file(target)
    #     return self
    #
    # def add_files(self, target):
    #     self.ast_load.load_files(target)
    #     return self
    #
    # def add_target(self, target):
    #     self.ast_load.load_target(target)
    #     return self
    #
    # def module(self):
    #     return self.target
    #
    # def stats(self):
    #     return self.ast_load.stats()