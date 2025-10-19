import ast
import sys
import types
import pytest
from unittest                           import TestCase
from unittest.mock                      import patch, call
from osbot_utils.testing.Catch          import Catch
from osbot_utils.utils.Misc             import list_set, random_string
from osbot_utils.utils.Objects          import obj_data
from osbot_utils.helpers.ast            import Ast_Module
from osbot_utils.helpers.ast.Ast_Base   import Ast_Base


class test_Ast_Base(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if sys.version_info > (3, 12):
            pytest.skip("Skipping tests that don't work on 3.13 or higher")
        if sys.version_info < (3, 9):
            pytest.skip("Skipping tests that need FIXING on 3.8 or lower")

    def setUp(self):
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

    def test_dump(self):
        assert Ast_Module(ast.parse("42"     )).dump() == ( 'Module(\n'
                                                             '    body=[\n'
                                                             '        Expr(\n'
                                                             '            value=Constant(value=42))],\n'
                                                             '    type_ignores=[])')
        assert Ast_Module(ast.parse("aa"     )).dump()  == ( 'Module(\n'
                                                             '    body=[\n'
                                                             '        Expr(\n'
                                                             "            value=Name(id='aa', ctx=Load()))],\n"
                                                             '    type_ignores=[])')
        assert Ast_Module(ast.parse("aa=42"   )).dump() == ( 'Module(\n'
                                                             '    body=[\n'
                                                             '        Assign(\n'
                                                             '            targets=[\n'
                                                             "                Name(id='aa', ctx=Store())],\n"
                                                             '            value=Constant(value=42))],\n'
                                                             '    type_ignores=[])')
        assert Ast_Module(ast.parse("a(42)"   )).dump() == ( 'Module(\n'
                                                             '    body=[\n'
                                                             '        Expr(\n'
                                                             '            value=Call(\n'
                                                             "                func=Name(id='a', ctx=Load()),\n"
                                                             '                args=[\n'
                                                             '                    Constant(value=42)],\n'
                                                             '                keywords=[]))],\n'
                                                             '    type_ignores=[])')
    def test_execute_code(self):
        namespace = {'__builtins__': globals().get('__builtins__')}
        #namespace = {'__builtins__': {}}
        assert self.ast_base.execute_code()                      == {'error': None, 'locals': {}, 'namespace': namespace, 'status': 'ok'}
        assert self.ast_base.execute_code(exec_locals={'a': 42}) == {'error': None, 'locals': {'a': 42}, 'namespace': namespace, 'status': 'ok'}
        assert Ast_Module("b=42").execute_code()                 == {'error': None, 'locals': {'b': 42}, 'namespace': namespace, 'status': 'ok'}
        assert Ast_Module("c=42").execute_code().get('locals')   == {'c': 42}
        assert type(Ast_Module("def answer():pass").execute_code().get('locals').get('answer')) == types.FunctionType

        ast_base = Ast_Module(Ast_Base).execute_code().get('locals').get('Ast_Base')
        assert list_set(obj_data(ast_base)) == list_set(obj_data(Ast_Base))
        assert str(ast_base)                == "<class 'Ast_Base'>"
        assert str(Ast_Base)                == "<class 'osbot_utils.helpers.ast.Ast_Base.Ast_Base'>"

        expected_error = "Catch: <class 'NameError'> : name 'ast' is not defined"
        with Catch(expected_error=expected_error):
            ast_base(ast.parse('a')).print_dump()

        the_answer_code = "def the_answer(name): return f'Hi {name}, the answer is 42'"
        sample_name     = random_string()
        expected_answer = f'Hi {sample_name}, the answer is 42'
        assert Ast_Module(the_answer_code).execute_code().get('locals').get('the_answer')(sample_name) == expected_answer

    def test_json(self):
        assert self.ast_base.json() == {}
        assert Ast_Module(ast.parse("42"   )).json() == { 'Ast_Module': { 'body': [{ 'Ast_Expr'  : { 'value'  : { 'Ast_Constant': { 'value': 42}}}}]}}
        assert Ast_Module(ast.parse("aa"   )).json() == { 'Ast_Module': { 'body': [{ 'Ast_Expr'  : { 'value'  : { 'Ast_Name'    : {'ctx': {'Ast_Load': {}}}, 'id'  : 'aa'}           }}]}}
        assert Ast_Module(ast.parse("aa=42")).json() == { 'Ast_Module': { 'body': [{ 'Ast_Assign': { 'targets': [{'Ast_Name'    : {'ctx': {'Ast_Store': {}}}, 'id': 'aa'}], 'value': {'Ast_Constant': {'value': 42}}}}]}}
        assert Ast_Module(ast.parse("a(42)")).json() == { 'Ast_Module': { 'body': [{ 'Ast_Expr'  : { 'value'  : { 'Ast_Call'    : {'args': [{'Ast_Constant': {'value': 42}}], 'func': {'Ast_Name': {'ctx': {'Ast_Load': {}}}, 'id': 'a'}, 'keywords': []}}}}]}}

    def test_key(self):
        assert self.ast_base.key() == "Ast_Base"

    def test_obj_data(self):
        assert self.ast_base.obj_data() == {'body': str(self.ast_base.node.body), 'type_ignores': '[]'}

    @patch('builtins.print')
    def test_print(self, builtins_print):
        assert self.ast_base.print() == self.ast_base
        assert builtins_print.call_args_list == [call('Module('
                                                      '\n    body=['
                                                      '\n        Expr('
                                                      '\n            value=BinOp('
                                                      '\n                left=Constant(value=40),'
                                                      '\n                op=Add(),'
                                                      '\n                right=Constant(value=2)))],'
                                                      '\n    type_ignores=[])')]

    @patch('builtins.print')
    def test_print_obj_info(self, builtins_print):
        call_args_list = builtins_print.call_args_list
        str_node       = str(self.ast_base.node)
        str_body       = str(self.ast_base.node.body)
        assert self.ast_base.print_obj_info() == self.ast_base
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

    # def test_visit(self):
    #
    #     print()
    #     result =