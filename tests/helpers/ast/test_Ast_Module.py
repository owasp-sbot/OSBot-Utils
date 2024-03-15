import ast
from json import JSONDecoder
from unittest                                           import TestCase
from osbot_utils.utils.Exceptions                       import syntax_error
from osbot_utils.utils.Files                            import file_contents
from osbot_utils.utils.Functions                        import python_file
from osbot_utils.utils.Misc                             import list_set
from osbot_utils.helpers.ast.Ast                        import Ast
from osbot_utils.helpers.ast.nodes.Ast_Argument         import Ast_Argument
from osbot_utils.helpers.ast.nodes.Ast_Arguments        import Ast_Arguments
from osbot_utils.helpers.ast.nodes.Ast_Constant         import Ast_Constant
from osbot_utils.helpers.ast.nodes.Ast_Function_Def     import Ast_Function_Def
from osbot_utils.helpers.ast.nodes.Ast_Module           import Ast_Module
from osbot_utils.helpers.ast.nodes.Ast_Return           import Ast_Return


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
        self.source_code = self.ast.source_code__from           (the_answer      )
        self.ast_module  = self.ast.ast_module__from_source_code(self.source_code)

    def test__setUp(self):
        assert type(self.ast_module) is Ast_Module

    def test_all_nodes__the_answer(self):
        nodes = self.ast_module.all_ast_nodes()
        expected_nodes_types = [Ast_Module, Ast_Function_Def, Ast_Arguments, Ast_Return, Ast_Argument,Ast_Constant]
        nodes_types = []
        for node in nodes:
            nodes_types.append(type(node))
        assert nodes_types == expected_nodes_types

    def test_all_nodes__an_class(self):
        an_class    = An_Class
        source_code = self.ast.source_code__from(an_class)
        module      = self.ast.parse(source_code)
        ast_module  = Ast_Module(module)

        assert type(module)       is ast.Module
        assert ast_module.stats() == {'all_keys'      : {'arg': 4, 'attr': 2, 'name': 3, 'value': 7} ,
                                      'all_values'    : { 42: 2, 12345: 1, 'An_Class': 1, 'a': 1, 'an_const': 1, 'an_param': 1, 'b': 1,
                                                          'c': 1, 'kwargs': 1, 'method_a': 1, 'method_b': 2, 'method_c': 1, 'self': 2},
                                      'ast_node_types': { 'Ast_Module': 1, 'Ast_Class_Def': 1, 'Ast_Name': 12, 'Ast_Function_Def': 2, 'Ast_Load': 12,
                                                          'Ast_Arguments': 2, 'Ast_Assign': 2, 'Ast_Expr': 2, 'Ast_Return': 2, 'Ast_Argument': 4,
                                                          'Ast_Constant': 7, 'Ast_Dict': 1, 'Ast_Call': 5, 'Ast_Store': 2, 'Ast_Attribute': 2},
                                      'node_types'    : { 'Module': 1, 'ClassDef': 1, 'Name': 12, 'FunctionDef': 2, 'Load': 12, 'arguments': 2,
                                                          'Assign': 2, 'Expr': 2, 'Return': 2, 'arg': 4, 'Constant': 7, 'Dict': 1, 'Call': 5,
                                                          'Store': 2, 'Attribute': 2}}
        #print('-------')
        #pprint(ast_module.stats())
        #pprint(ast_module.info())

    def test_all_nodes__in_source_code(self):
        target_python_file = python_file(JSONDecoder)
        source_code        = file_contents(target_python_file)
        module             = self.ast.parse(source_code)
        ast_module         = Ast_Module(module)

        assert type(module) is ast.Module
        assert ast_module.stats() == { 'all_keys'       : {'arg': 38, 'asname': 3, 'attr': 58, 'cause': 10, 'level': 2, 'module': 2, 'name': 24, 'step': 11, 'value': 142},
                                       'all_values'     : {None: 47, 0: 6, True: 38, 2: 1, 4: 1, 5: 2, 6: 1, 10: 1, 16: 1, 55296: 2, 56319: 1, 56320: 2, 57343: 1, 65536: 1, '': 9, '\x08': 1, '"': 6, '%s: line %d column %': 1, '(.*?)(["\\\\\\x00-\\x1f]': 1, ',': 2, '-Infinity': 1, '-inf': 1, '/': 2, ':': 2, 'DOTALL': 1, 'Decode a JSON docume': 1, "Expecting ',' delimi": 2, "Expecting ':' delimi": 1, 'Expecting property n': 2, 'Expecting value': 3, 'Extra data': 1, 'Implementation of JS': 1, 'Infinity': 1, 'Invalid \\escape: {0!': 1, 'Invalid \\uXXXX escap': 1, 'Invalid control char': 1, 'JSONArray': 1, 'JSONDecodeError': 2, 'JSONDecoder': 2, 'JSONObject': 1, 'MULTILINE': 1, 'NaN': 1, 'Return the Python re': 1, 'Scan the string s fo': 1, 'Simple JSON <https:/': 1, 'Subclass of ValueErr': 1, 'Unterminated string': 2, 'VERBOSE': 1, '[ \\t\\n\\r]*': 1, '\\': 3, '\\u': 1, ']': 2, '__class__': 1, '__getitem__': 1, '__init__': 3, '__reduce__': 1, '_b': 1, '_decode_uXXXX': 1, '_json': 1, '_m': 1, '_w': 3, '_ws': 2, '``object_hook``, if': 1, 'append': 3, 'b': 1, 'c_scanstring': 1, 'colno': 1, 'compile': 2, 'count': 1, 'decode': 1, 'doc': 3, 'end': 12, 'err': 3, 'f': 1, 'format': 2, 'groups': 1, 'idx': 2, 'inf': 1, 'join': 1, 'json': 1, 'lineno': 1, 'make_scanner': 1, 'match': 4, 'memo': 2, 'msg': 3, 'n': 1, 'nan': 1, 'object_hook': 3, 'object_pairs_hook': 3, 'parse_array': 1, 'parse_constant': 2, 'parse_float': 2, 'parse_int': 2, 'parse_object': 1, 'parse_string': 1, 'pos': 4, 'py_scanstring': 1, 'r': 1, 'raw_decode': 2, 're': 1, 'rfind': 1, 's': 4, 's_and_end': 2, 'scan_once': 4, 'scanner': 1, 'scanstring': 1, 'self': 5, 'setdefault': 1, 'strict': 4, 't': 1, 'u': 1, 'value': 3, 'xX': 1, '}': 2},
                                       'ast_node_types' : {'Ast_Add': 33, 'Ast_Alias': 3, 'Ast_And': 2, 'Ast_Argument': 37, 'Ast_Arguments': 9, 'Ast_Assign': 86, 'Ast_Attribute': 58, 'Ast_Aug_Assign': 10, 'Ast_Bin_Op': 35, 'Ast_Bool_Op': 6, 'Ast_Break': 3, 'Ast_Call': 71, 'Ast_Class_Def': 2, 'Ast_Compare': 34, 'Ast_Constant': 142, 'Ast_Continue': 1, 'Ast_Dict': 5, 'Ast_Eq': 7, 'Ast_Except_Handler': 10, 'Ast_Expr': 13, 'Ast_Function_Def': 9, 'Ast_If': 34, 'Ast_Import': 1, 'Ast_Import_From': 2, 'Ast_In': 8, 'Ast_Is': 2, 'Ast_Is_Not': 4, 'Ast_Keyword': 1, 'Ast_List': 4, 'Ast_Load': 408, 'Ast_LtE': 4, 'Ast_Mod': 1, 'Ast_Module': 1, 'Ast_Name': 418, 'Ast_Node': 4, 'Ast_Not_Eq': 10, 'Ast_Not_In': 1, 'Ast_Or': 4, 'Ast_Pass': 3, 'Ast_Raise': 14, 'Ast_Return': 11, 'Ast_Slice': 11, 'Ast_Store': 112, 'Ast_Sub': 7, 'Ast_Subscript': 20, 'Ast_Try': 10, 'Ast_Tuple': 20, 'Ast_While': 3},
                                       'node_types'     : {'Add': 33, 'And': 2, 'Assign': 86, 'Attribute': 58, 'AugAssign': 10, 'BinOp': 35, 'BitOr': 3, 'BoolOp': 6, 'Break': 3, 'Call': 71, 'ClassDef': 2, 'Compare': 34, 'Constant': 142, 'Continue': 1, 'Dict': 5, 'Eq': 7, 'ExceptHandler': 10, 'Expr': 13, 'FunctionDef': 9, 'If': 34, 'Import': 1, 'ImportFrom': 2, 'In': 8, 'Is': 2, 'IsNot': 4, 'LShift': 1, 'List': 4, 'Load': 408, 'LtE': 4, 'Mod': 1, 'Module': 1, 'Name': 418, 'NotEq': 10, 'NotIn': 1, 'Or': 4, 'Pass': 3, 'Raise': 14, 'Return': 11, 'Slice': 11, 'Store': 112, 'Sub': 7, 'Subscript': 20, 'Try': 10, 'Tuple': 20, 'While': 3, 'alias': 3, 'arg': 37, 'arguments': 9, 'keyword': 1}} != {}

        for node in ast_module.all_ast_nodes():
            assert node
            assert node.info() is not None


    def test_info(self):
        info = self.ast_module.info()
        assert self.ast_module.source_code() == 'def the_answer(aaa):\n    return 42'

        assert list_set(info) == ['Ast_Module']
        #assert info == {'Ast_Module': {'body': ['[Ast_Node][Ast_Function_Def]']}}
        # assert info == { 'Ast_Module': { 'body': [ { 'Ast_Function_Def': { 'args': { 'Ast_Arguments': { 'args' : [{'Ast_Argument': {'arg': 'aaa'}}]}},
        #                                                                    'body': [{'Ast_Return': {'value': {'Ast_Constant': {'value': 42}}}}],
        #                                                                    'name': 'the_answer'}}]}}


    def test_source_code(self):
        assert self.ast_module.source_code() == "def the_answer(aaa):\n    return 42"  # note that we lost the comment (which is a known limitation of the pure python AST classes, LibCST or parso are alternatives which are able to create a CST - Concrete Syntax Tree)

    def test_syntax_error(self):
        with self.assertRaises(Exception) as context:
            Ast_Module("import ...")
        assert str(context.exception) == ('[SyntaxError] '
                                          '\n'
                                          '\nError parsing code: invalid syntax in <unknown> at line 1 column 8'
                                          '\n'
                                          '\n    import ...'
                                          '\n           ^')

        with self.assertRaises(Exception) as context_2:
            raise syntax_error('an error')
        assert str(context_2.exception) == 'an error'