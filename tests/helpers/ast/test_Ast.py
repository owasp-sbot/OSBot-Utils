import ast
from unittest                                   import TestCase
from osbot_utils.helpers.ast.Ast                import Ast
from osbot_utils.helpers.ast.nodes.Ast_Module   import Ast_Module


def the_answer():
    return 42    # an comment

class test_Ast(TestCase):

    def setUp(self):
        self.ast = Ast()

    def test_source_code(self):
        source_code = self.ast.source_code__from(the_answer)
        assert source_code == 'def the_answer():\n    return 42    # an comment'

    def test_ast_module__from_source_code(self):
        source_code = self.ast.source_code__from(the_answer)
        ast_module  = self.ast.ast_module__from_source_code(source_code)
        assert type(ast_module     ) is Ast_Module
        assert type(ast_module.node) is ast.Module

