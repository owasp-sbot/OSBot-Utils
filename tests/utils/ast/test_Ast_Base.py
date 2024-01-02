import ast
from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import obj_info
from osbot_utils.utils.ast import Ast_Module
from osbot_utils.utils.ast.Ast import Ast
from osbot_utils.utils.ast.Ast_Base import Ast_Base


class test_Ast_Base(TestCase):

    def setUp(self):
        # self.ast_module = Ast().ast_module__from(Ast)
        # assert isinstance(self.ast_module, Ast_Base)
        # assert type(self.ast_module) is not Ast_Base
        # assert type(self.ast_module) is Ast_Module
        node            = ast.parse("40+2")
        self.ast_base   = Ast_Base(node)
        assert type(self.ast_base) is Ast_Base

    def test___init__(self):
        with self.assertRaises(Exception) as context:
            Ast_Base(None)

        assert context.exception.args[0]                    == "'NoneType' object has no attribute '__module__'"
        assert context.expected.__name__                    == 'Exception'
        assert context.msg                                  is None
        assert context.obj_name                             is None
        assert context.test_case.ast_base                   is self.ast_base
        assert context.test_case.failureException.__name__  == 'AssertionError'
        assert context.test_case.longMessage                is True
        assert context.test_case.maxDiff                    == 640

        #assert context.test_case is test_Ast_Base.test___init__

    def test___repr__(self):
        assert self.ast_base.__repr__() == "Ast_Base"

    def test_key(self):
        assert self.ast_base.key() == "Ast_Base"

    def test_obj_data(self):
        assert self.ast_base.obj_data() == {'body': str(self.ast_base.node.body), 'type_ignores': '[]'}

    @patch('builtins.print')
    def test_print(self, builtins_print):
        call_args_list = builtins_print.call_args_list
        str_node       = str(self.ast_base.node)
        str_body       = str(self.ast_base.node.body)
        assert self.ast_base.print() == self.ast_base
        assert call_args_list[0]     == call()
        assert call_args_list[1]     == call(f"Members for object:\n\t {str_node} of type:<class 'ast.Module'>")
        assert call_args_list[2]     == call('Settings:\n\t name_width: 30 | value_width: 100 | show_private: False | show_internals: False')
        assert call_args_list[3]     == call()
        assert call_args_list[4]     == call('field                          | value')
        assert call_args_list[5]     == call('----------------------------------------------------------------------------------------------------------------------------------')
        assert call_args_list[6]     == call(f'body                           | {str_body}')
        assert call_args_list[7]     == call('type_ignores                   | []')
        assert len(call_args_list)   == 8

    def test_source_code(self):
        assert self.ast_base.source_code() == '40 + 2'