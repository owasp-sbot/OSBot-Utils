from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Data import Ast_Data
from osbot_utils.utils.ast.Ast_Node import Ast_Node

class test_Ast_Data(TestCase):

    def setUp(self):
        self.ast_data = Ast_Data().add_target(Ast_Data)

    def test_modules(self):
        print()
        modules = self.ast_data.modules()
        #module  = modules[0]
        assert len(modules) == 1

    # def test_stats(self):
    #     pprint(self.ast_data.stats())
