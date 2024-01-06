from unittest import TestCase
from unittest.mock import patch

from osbot_utils.utils.Str import str_dedent
from osbot_utils.utils.ast import Ast_Module
from osbot_utils.utils.ast.Ast_Merge import Ast_Merge


class test_Ast_Merge(TestCase):

    def setUp(self):
        self.ast_merge = Ast_Merge()
        self.module    = self.ast_merge.module

    def test__init__(self):
        assert self.module.json() == {'Ast_Module': {'body': []}}

    # def test_merge_file(self):
    #     Ast_Module(__file__).print()

    def test_merge_module(self):
        code_to_merge   = "a = 42"
        module_to_merge = Ast_Module(code_to_merge)

        assert self.ast_merge.source_code () == ''
        assert module_to_merge.source_code() == code_to_merge
        assert self.ast_merge.merge_module(module_to_merge) is True
        assert self.ast_merge.source_code() == code_to_merge

        code_to_merge_2   = str_dedent("""
                                           def the_answer(value):
                                               print(f'the_answer is {value}')
                                           the_answer(a)
                                           """)
        module_to_merge_2 = Ast_Module(code_to_merge_2)
        assert module_to_merge_2.source_code() == code_to_merge_2
        assert self.ast_merge.merge_module(module_to_merge_2) is True
        assert self.ast_merge.source_code() == (f'{code_to_merge}'
                                                f'\n'
                                                f'\n'
                                                f'{code_to_merge_2}')

        with patch('builtins.print') as mock_print:
            exec(self.ast_merge.source_code())
            mock_print.assert_called_once_with("the_answer is 42")



