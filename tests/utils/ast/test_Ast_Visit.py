from unittest import TestCase

from osbot_utils.utils.Dev import pprint, jprint
from osbot_utils.utils.Functions import python_file
from osbot_utils.utils.ast import Ast_Module
from osbot_utils.utils.ast.Ast_Visit import Ast_Visit

def an_method():
    print(40)
    print('plus')
    print(2)
    return 42


class test_Ast_Visit(TestCase):


    def test__init__(self):
        module = Ast_Module("4")
        assert Ast_Visit(module).ast_node == module


    def test__visit(self):
        module = Ast_Module(TestCase)
        self.ast_visit = Ast_Visit(module)

        def assert_len(nodes, size):
            assert len(nodes) == size

        self.ast_visit.capture          ('Ast_Module'        , lambda modules  : assert_len(modules  , 1 ))
        self.ast_visit.capture          ('Ast_Function_Def'  , lambda functions: assert_len(functions, 72))
        self.ast_visit.capture_modules  (lambda modules  : assert_len(modules  , 1 ))
        self.ast_visit.capture_functions(lambda functions: assert_len(functions, 72))
        self.ast_visit.capture_calls    (lambda calls    : assert_len(calls    , 366))
        self.ast_visit.visit()

    def test_capture_calls(self):
        ast_visit = Ast_Visit(python_file(TestCase))
        ast_visit.capture_calls().capture_imports().capture_modules().capture_functions()
        ast_visit.visit()
        assert ast_visit.stats() == { 'Ast_Call'        : 469 ,
                                      'Ast_Function_Def': 109 ,
                                      'Ast_Import'      :  10 ,
                                      'Ast_Import_From' :   4 ,
                                      'Ast_Module'      :   1 }
        captured_nodes = ast_visit.captured_nodes()
        assert len(captured_nodes.get('Ast_Call'        )) == 469
        assert len(captured_nodes.get('Ast_Function_Def')) == 109
        assert len(captured_nodes.get('Ast_Import'      )) ==  10
        assert len(captured_nodes.get('Ast_Import_From' )) ==   4
        assert len(captured_nodes.get('Ast_Module'      )) ==   1

    def test_register_node_handler(self):

        with Ast_Visit("an_method()") as _:
            def on_call(node):
                assert node.name() == 'an_method'
            _.register_node_handler('Ast_Call', on_call)
            _.visit()

        with Ast_Visit("an_class.an_object.an_method()") as _:
            def on_call(node):
                assert node.name() == 'an_method'
            _.register_node_handler('Ast_Call', on_call)
            _.visit()

    def test_stats(self):
        assert Ast_Visit("42"           )                    .visit().stats() == {}
        assert Ast_Visit("42"           ).capture_calls    ().visit().stats() == {'Ast_Call'        : 0 }
        assert Ast_Visit("aa()"         ).capture_calls    ().visit().stats() == {'Ast_Call'        : 1 }
        assert Ast_Visit("aa()"         ).capture_functions().visit().stats() == {'Ast_Function_Def': 0 }
        assert Ast_Visit("def aa():pass").capture_functions().visit().stats() == {'Ast_Function_Def': 1 }
        assert Ast_Visit("def aa():pass").capture_imports  ().visit().stats() == {'Ast_Import'      : 0 , 'Ast_Import_From': 0}
        assert Ast_Visit("import abcd; ").capture_imports  ().visit().stats() == {'Ast_Import'      : 1 , 'Ast_Import_From': 0}
