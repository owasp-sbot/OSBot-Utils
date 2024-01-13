from unittest import TestCase

import pytest

from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.helpers.ast                    import Ast_Module
from osbot_utils.helpers.ast.Ast_Data           import Ast_Data

class test_Ast_Data(TestCase):

    def setUp(self):
        #self.ast_data = Ast_Data().add_target(Ast_Data)
        self.code = "def the_answer(name): return f'Hi {name}, the answer is 42'"
        self.ast_data = Ast_Data(self.code)

    def test_module(self):
        result = self.ast_data.target.execute_code()
        assert result.get('locals').get('the_answer')('ABC') == 'Hi ABC, the answer is 42'


    # def test_stats(self):
    #     pprint(self.ast_data.stats())

    @pytest.mark.skip("add this capability to one of the Ast classes")
    def test_remove_items_from_ast(self):
        print()
        ast_module = Ast_Module(Kwargs_To_Self)
        class_ast = ast_module.body()[0]
        del class_ast.node.body[0]
        function_ast = ast_module.body()[0].body()[0]
        del function_ast.node.body[0]
        print(function_ast.body())

        print(ast_module.source_code())
