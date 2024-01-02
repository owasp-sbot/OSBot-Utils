from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.ast.Ast_Data import Ast_Data
from osbot_utils.utils.ast.Ast_Node import Ast_Node
from osbot_utils.utils.ast.Ast_Visitor import Ast_Visitor


class test_Ast_Data(TestCase):

    def setUp(self):
        self.ast_data = Ast_Data().add_target(Ast_Node)

    def test_modules(self):
        #print()
        modules = self.ast_data.modules()
        module  = modules[0]
        assert len(modules) == 1
        #pprint(module.info())

    # def test_stats(self):
    #     pprint(self.ast_data.stats())
