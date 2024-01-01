from unittest import TestCase

from osbot_utils.utils.Dev import pprint, jprint
from osbot_utils.utils.ast.Ast import Ast
from osbot_utils.utils.ast.Ast_Argument import Ast_Argument
from osbot_utils.utils.ast.Ast_Arguments import Ast_Arguments
from osbot_utils.utils.ast.Ast_Constant import Ast_Constant
from osbot_utils.utils.ast.Ast_Function_Def import Ast_Function_Def
from osbot_utils.utils.ast.Ast_Module import Ast_Module
from osbot_utils.utils.ast.Ast_Return import Ast_Return


class An_Class:
    def method_a(self):
        self.method_b()

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

    def test_all_nodes(self):
        nodes = self.ast_module.all_nodes()
        expected_nodes_types = [Ast_Module, Ast_Function_Def, Ast_Arguments, Ast_Return, Ast_Argument,Ast_Constant]
        nodes_types = []
        for node in nodes:
            nodes_types.append(type(node))
        assert nodes_types == expected_nodes_types
        #
        # pprint(nodes_types)
        # print()
        # print()
        # for node in nodes:
        #     print('----------------------------------------')
        #     print(node, node.info())


    def test_info(self):
        info = self.ast_module.info()

        jprint(info)

        # pass
        # code_2       = self.ast.source_code(test_Ast_Module)
        # ast_module_2 = self.ast.ast_module__from_source_code(code_2)
        # nodes_2      = ast_module_2.all_nodes()

        #for node in nodes_2:
        #    print(node.source_code())
            #print()
            #pass

        #assert len(list(self.ast_module.all_nodes())) == 5

    def test_source_code(self):
        assert self.ast_module.source_code() == "def the_answer(aaa):\n    return 42"  # note that we lost the comment (which is a known limitation of the pure python AST classes, LibCST or parso are alternatives which are able to create a CST - Concrete Syntax Tree)