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
        assert ast_module.stats() == { 'ast_types': { 'Ast_Argument'    : 4 ,
                                                      'Ast_Arguments'   : 2 ,
                                                      'Ast_Assign'      : 2 ,
                                                      'Ast_Attribute'   : 2 ,
                                                      'Ast_Call'        : 5 ,
                                                      'Ast_Class_Def'   : 1 ,
                                                      'Ast_Constant'    : 7 ,
                                                      'Ast_Dict'        : 1 ,
                                                      'Ast_Expr'        : 2 ,
                                                      'Ast_Function_Def': 2 ,
                                                      'Ast_Load'        : 12,
                                                      'Ast_Module'      : 1 ,
                                                      'Ast_Name'        : 12,
                                                      'Ast_Return'      : 2 ,
                                                      'Ast_Store'       : 2 },
                                       'types': { 'Assign'      : 2 ,
                                                  'Attribute'   : 2 ,
                                                  'Call'        : 5 ,
                                                  'ClassDef'    : 1 ,
                                                  'Constant'    : 7 ,
                                                  'Dict'        : 1 ,
                                                  'Expr'        : 2 ,
                                                  'FunctionDef' : 2 ,
                                                  'Load'        : 12,
                                                  'Module'      : 1 ,
                                                  'Name'        : 12,
                                                  'Return'      : 2 ,
                                                  'Store'       : 2 ,
                                                  'arg'         : 4 ,
                                                  'arguments'   : 2}}

    def test_all_nodes__in_source_code(self):
        print('----')
        target_python_file = python_file(TestCase)

        source_code  = file_contents(target_python_file)
        module       = self.ast.parse(source_code)
        ast_module   = Ast_Module(module)

        print('')
        assert type(module) is ast.Module
        # assert ast_module.stats() == {'ast_types': { 'Ast_Add': 1,
        #                                              'Ast_Alias': 16,
        #                                              'Ast_Argument': 14,
        #                                              'Ast_Arguments': 11,
        #                                              'Ast_Assert': 9,
        #                                              'Ast_Assign': 18,
        #                                              'Ast_Attribute': 32,
        #                                              'Ast_Aug_Assign': 1,
        #                                              'Ast_Call': 30,
        #                                              'Ast_Class_Def': 3,
        #                                              'Ast_Compare': 9,
        #                                              'Ast_Constant': 93,
        #                                              'Ast_Dict': 17,
        #                                              'Ast_Eq': 6,
        #                                              'Ast_Expr': 6,
        #                                              'Ast_For': 2,
        #                                              'Ast_Function_Def': 11,
        #                                              'Ast_Import': 1,
        #                                              'Ast_Import_From': 13,
        #                                              'Ast_Is': 3,
        #                                              'Ast_List': 5,
        #                                              'Ast_Load': 104,
        #                                              'Ast_Module': 1,
        #                                              'Ast_Name': 87,
        #                                              'Ast_Return': 4,
        #                                              'Ast_Store': 21,
        #                                              'Ast_Tuple': 1},
        #                                 'types'  : { 'Add': 1,
        #                                              'Assert': 9,
        #                                              'Assign': 18,
        #                                              'Attribute': 32,
        #                                              'AugAssign': 1,
        #                                              'Call': 30,
        #                                              'ClassDef': 3,
        #                                              'Compare': 9,
        #                                              'Constant': 93,
        #                                              'Dict': 17,
        #                                              'Eq': 6,
        #                                              'Expr': 6,
        #                                              'For': 2,
        #                                              'FunctionDef': 11,
        #                                              'Import': 1,
        #                                              'ImportFrom': 13,
        #                                              'Is': 3,
        #                                              'List': 5,
        #                                              'Load': 104,
        #                                              'Module': 1,
        #                                              'Name': 87,
        #                                              'Return': 4,
        #                                              'Store': 21,
        #                                              'Tuple': 1,
        #                                              'alias': 16,
        #                                              'arg': 14,
        #                                              'arguments': 11}}
        #pprint(ast_module.stats())
        #an_class = An_Class
        #source_code = self.ast.source_code(an_class)
        #module = self.ast.parse(source_code)
        #ast_module = Ast_Module(module)

        for node in ast_module.all_nodes():
            if type(node) is Ast_Node:
                assert node
                #print(node, node.info())
                #print()
        #
        # pprint(nodes_types)
        # print()
        # print()
        # for node in nodes:
        #     print('----------------------------------------')
        #     print(node, node.info())


    def test_info(self):
        info = self.ast_module.info()
        assert self.ast_module.source_code() == 'def the_answer(aaa):\n    return 42'
        assert info == { 'Ast_Module': { 'body': [ { 'Ast_Function_Def': { 'args': { 'Ast_Args': { 'args' : [{'Ast_Argument': {'arg': 'aaa'}}]}},
                                                                           'body': [{'Ast_Return': {'value': {'Ast_Constant': {'value': 42}}}}],
                                                                           'name': 'the_answer'}}]}}


    def test_source_code(self):
        assert self.ast_module.source_code() == "def the_answer(aaa):\n    return 42"  # note that we lost the comment (which is a known limitation of the pure python AST classes, LibCST or parso are alternatives which are able to create a CST - Concrete Syntax Tree)