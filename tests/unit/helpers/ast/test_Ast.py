import ast
import sys
from unittest                                   import TestCase

import pytest

from osbot_utils.helpers.ast.Ast                import Ast
from osbot_utils.helpers.ast.nodes.Ast_Module   import Ast_Module
from osbot_utils.utils.Env import env__terminal__is__xterm, env__home__is__root


def the_answer():
    return 42    # an comment

class test_Ast(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if env__terminal__is__xterm() or env__home__is__root():
            pytest.skip('Skipping tests that are failing in local docker')  # todo: figure out why multiple of these were failing inside docker
        if sys.version_info < (3, 9):
            pytest.skip("Skipping tests that don't work on 3.8 or lower")

    def setUp(self):
        self.ast = Ast()
        if self.ast.source_code__from(the_answer) is None:
            pytest.skip('Skipping when source_code is not available')

    def test_source_code(self):
        source_code = self.ast.source_code__from(the_answer)
        assert source_code == 'def the_answer():\n    return 42    # an comment'

    def test_ast_module__from_source_code(self):
        source_code = self.ast.source_code__from(the_answer)
        ast_module  = self.ast.ast_module__from_source_code(source_code)
        assert type(ast_module     ) is Ast_Module
        assert type(ast_module.node) is ast.Module

