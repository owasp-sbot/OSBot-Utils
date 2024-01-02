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
        self.node       = ast.parse("40+2")
        self.ast_base   = Ast_Base(self.node)
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

        with self.assertRaises(Exception) as context_2:
            Ast_Base("an string")
        assert context_2.exception.args[0]                    == "'str' object has no attribute '__module__'"

    def test___repr__(self):
        assert self.ast_base.__repr__() == "Ast_Base"

    def test_json(self):
        assert self.ast_base.json() == {}
        #ast_module = Ast().ast_module__from(Ast)
        assert Ast_Module(ast.parse("42"   )).json() == { 'Ast_Module': { 'body': [{ 'Ast_Expr'  : { 'value'  : { 'Ast_Constant': { 'value': 42}}}}]}}
        assert Ast_Module(ast.parse("aa"   )).json() == { 'Ast_Module': { 'body': [{ 'Ast_Expr'  : { 'value'  : { 'Ast_Name'    : {'ctx': {'Ast_Load': {}}}, 'id'  : 'aa'}           }}]}}
        assert Ast_Module(ast.parse("aa=42")).json() == { 'Ast_Module': { 'body': [{ 'Ast_Assign': { 'targets': [{'Ast_Name'    : {'ctx': {'Ast_Store': {}}}, 'id': 'aa'}], 'value': {'Ast_Constant': {'value': 42}}}}]}}
        assert Ast_Module(ast.parse("a(42)")).json() == { 'Ast_Module': { 'body': [{ 'Ast_Expr'  : { 'value'  : { 'Ast_Call'    : {'args': [{'Ast_Constant': {'value': 42}}], 'func': {'Ast_Name': {'ctx': {'Ast_Load': {}}}, 'id': 'a'}, 'keywords': []}}}}]}}
        #tree = ast.parse("aa")
        #print(ast.dump(tree, indent=4))

        # print()
        # print()
        # result = ast_module.json()
        # pprint(result)

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