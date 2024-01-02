import ast
from unittest import TestCase
from osbot_utils.utils.Dev import pprint as p_print
from osbot_utils.utils.Dev import pprint, jprint
from osbot_utils.utils.Files import file_contents
from osbot_utils.utils.Functions import module_file, python_file
from osbot_utils.utils.Objects import obj_info, print_obj_data_as_dict
from osbot_utils.utils.ast.Ast import Ast
from osbot_utils.utils.ast.Ast_Argument import Ast_Argument
from osbot_utils.utils.ast.Ast_Arguments import Ast_Arguments
from osbot_utils.utils.ast.Ast_Constant import Ast_Constant
from osbot_utils.utils.ast.Ast_Function_Def import Ast_Function_Def
from osbot_utils.utils.ast.Ast_Module import Ast_Module
from osbot_utils.utils.ast.Ast_Node import Ast_Node
from osbot_utils.utils.ast.Ast_Return import Ast_Return


class Base_Class:

    def method_c(self, value=0):
        a = 42
        value += 1
        return a, value

class An_Class(Base_Class):

    def method_a(self, an_param=12345, **kwargs):
        data = {'a': an_param, 'b': kwargs , 'c': 'an_const'}
        print(set(data))
        value = self.method_b()
        return self.method_c(value)

    def method_b(self):
        print(42)
        return 42

def the_answer(aaa):
    return 42    # an comment

class test_Ast_Module(TestCase):
    def setUp(self):
        self.ast         = Ast()
        self.source_code = self.ast.source_code(the_answer)
        self.ast_module  = self.ast.ast_module__from_source_code(self.source_code)

    def test__setUp(self):
        assert type(self.ast_module) is Ast_Module

    def test_all_nodes__the_answer(self):
        nodes = self.ast_module.all_nodes()
        expected_nodes_types = [Ast_Module, Ast_Function_Def, Ast_Arguments, Ast_Return, Ast_Argument,Ast_Constant]
        nodes_types = []
        for node in nodes:
            nodes_types.append(type(node))
        assert nodes_types == expected_nodes_types

    def test_all_nodes__an_class(self):
        an_class    = An_Class
        source_code = self.ast.source_code(an_class)
        module      = self.ast.parse(source_code)
        ast_module  = Ast_Module(module)

        assert type(module)       is ast.Module
        assert ast_module.stats() == {'ast_types': {'Ast_Module': 1, 'Ast_Class_Def': 1, 'Ast_Name': 12, 'Ast_Function_Def': 2, 'Ast_Load': 12,
                                                    'Ast_Arguments': 2, 'Ast_Assign': 2, 'Ast_Expr': 2, 'Ast_Return': 2, 'Ast_Argument': 4,
                                                    'Ast_Constant': 7, 'Ast_Dict': 1, 'Ast_Call': 5, 'Ast_Store': 2, 'Ast_Attribute': 2},
                                      'types'    : {'Module': 1, 'ClassDef': 1, 'Name': 12, 'FunctionDef': 2, 'Load': 12, 'arguments': 2,
                                                    'Assign': 2, 'Expr': 2, 'Return': 2, 'arg': 4, 'Constant': 7, 'Dict': 1, 'Call': 5,
                                                    'Store': 2, 'Attribute': 2}}

    def test_all_nodes__in_source_code(self):
        target_python_file = python_file(TestCase)
        source_code        = file_contents(target_python_file)
        module             = self.ast.parse(source_code)
        ast_module         = Ast_Module(module)

        print('')
        assert type(module) is ast.Module
        assert ast_module.stats() == {'ast_types': {'Ast_Module': 1, 'Ast_Expr': 179, 'Ast_Import': 10, 'Ast_Import_From': 4, 'Ast_Assign': 212, 'Ast_Class_Def': 12,
                                                    'Ast_Function_Def': 109, 'Ast_Constant': 356, 'Ast_Alias': 18, 'Ast_Name': 1420, 'Ast_Call': 413, 'Ast_Arguments': 109,
                                                    'Ast_Return': 71, 'Ast_List': 13, 'Ast_While': 4, 'Ast_If': 113, 'Ast_Attribute': 430, 'Ast_Store': 267, 'Ast_Load': 1685,
                                                    'Ast_Try': 25, 'Ast_Argument': 281, 'Ast_Raise': 26, 'Ast_Unary_Op': 27, 'Ast_Bool_Op': 27, 'Ast_For': 10, 'Ast_Bin_Op': 71,
                                                    'Ast_Pass': 3, 'Ast_Except_Handler': 25, 'Ast_Tuple': 68, 'Ast_Subscript': 12, 'Ast_Not': 27, 'Ast_And': 13, 'Ast_Compare': 78,
                                                    'Ast_With': 6, 'Ast_Mult': 1, 'Ast_Pow': 1, 'Ast_Dict': 2, 'Ast_If_Exp': 1, 'Ast_Aug_Assign': 11, 'Ast_Assert': 1, 'Ast_Yield': 4,
                                                    'Ast_Generator_Exp': 3, 'Ast_Is_Not': 24, 'Ast_With_Item': 6, 'Ast_Is': 16, 'Ast_Keyword': 19, 'Ast_Continue': 2, 'Ast_Mod': 56,
                                                    'Ast_Eq': 15, 'Ast_Or': 14, 'Ast_Starred': 9, 'Ast_Add': 20, 'Ast_Not_In': 3, 'Ast_In': 1, 'Ast_Not_Eq': 8, 'Ast_List_Comp': 1,
                                                    'Ast_Comprehension': 4, 'Ast_Sub': 4, 'Ast_LtE': 3, 'Ast_Break': 3, 'Ast_Gt': 5, 'Ast_Lt': 2, 'Ast_GtE': 1, 'Ast_Slice': 1},
                                      'types'    : {'Module': 1, 'Expr': 179, 'Import': 10, 'ImportFrom': 4, 'Assign': 212, 'ClassDef': 12, 'FunctionDef': 109, 'Constant': 356,
                                                    'alias': 18, 'Name': 1420, 'Call': 413, 'arguments': 109, 'Return': 71, 'List': 13, 'While': 4, 'If': 113, 'Attribute': 430,
                                                    'Store': 267, 'Load': 1685, 'Try': 25, 'arg': 281, 'Raise': 26, 'UnaryOp': 27, 'BoolOp': 27, 'For': 10, 'BinOp': 71, 'Pass': 3,
                                                    'ExceptHandler': 25, 'Tuple': 68, 'Subscript': 12, 'Not': 27, 'And': 13, 'Compare': 78, 'With': 6, 'Mult': 1, 'Pow': 1, 'Dict': 2,
                                                    'IfExp': 1, 'AugAssign': 11, 'Assert': 1, 'Yield': 4, 'GeneratorExp': 3, 'IsNot': 24, 'withitem': 6, 'Is': 16, 'keyword': 19,
                                                    'Continue': 2, 'Mod': 56, 'Eq': 15, 'Or': 14, 'Starred': 9, 'Add': 20, 'NotIn': 3, 'In': 1, 'NotEq': 8, 'ListComp': 1,
                                                    'comprehension': 4, 'Sub': 4, 'LtE': 3, 'Break': 3, 'Gt': 5, 'Lt': 2, 'GtE': 1, 'Slice': 1}}
        #print(ast_module.stats())

        for node in ast_module.all_nodes():
            #if type(node) is Ast_Node:
                assert node
                assert node.info() is not None
                #print(node, node.info())
                #print()


    def test_info(self):
        info = self.ast_module.info()
        assert self.ast_module.source_code() == 'def the_answer(aaa):\n    return 42'
        assert info == { 'Ast_Module': { 'body': [ { 'Ast_Function_Def': { 'args': { 'Ast_Args': { 'args' : [{'Ast_Argument': {'arg': 'aaa'}}]}},
                                                                           'body': [{'Ast_Return': {'value': {'Ast_Constant': {'value': 42}}}}],
                                                                           'name': 'the_answer'}}]}}


    def test_source_code(self):
        assert self.ast_module.source_code() == "def the_answer(aaa):\n    return 42"  # note that we lost the comment (which is a known limitation of the pure python AST classes, LibCST or parso are alternatives which are able to create a CST - Concrete Syntax Tree)