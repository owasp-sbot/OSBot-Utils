from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.ast.Ast import Ast
from osbot_utils.utils.ast.Ast_Visit import Ast_Visit
from tests.testing.test_Profiler import An_Class


class test_Ast_Visit(TestCase):

    def setUp(self):
        self.ast      = Ast()
        self.ast_visit = Ast_Visit()

    def test_vist(self):
        ast_module = self.ast.ast_module__from(An_Class)
        #print()
        #print()
        assert list_set(ast_module.info()) == ['Ast_Module']
