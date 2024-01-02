import ast
from unittest                                       import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files                        import file_contents
from osbot_utils.utils.Functions                    import python_file
from osbot_utils.utils.ast.Ast                      import Ast
from osbot_utils.utils.ast.nodes.Ast_Argument       import Ast_Argument
from osbot_utils.utils.ast.nodes.Ast_Arguments      import Ast_Arguments
from osbot_utils.utils.ast.nodes.Ast_Constant       import Ast_Constant
from osbot_utils.utils.ast.nodes.Ast_Function_Def   import Ast_Function_Def
from osbot_utils.utils.ast.nodes.Ast_Module         import Ast_Module
from osbot_utils.utils.ast.nodes.Ast_Return         import Ast_Return


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
        nodes = self.ast_module.all_ast_nodes()
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
        target_python_file = python_file(TestCase)
        source_code        = file_contents(target_python_file)
        module             = self.ast.parse(source_code)
        ast_module         = Ast_Module(module)

        print('')
        assert type(module) is ast.Module
        print(ast_module.stats().get('all_values'))
        assert ast_module.stats() == {'all_keys'      : { 'name': 164, 'value': 372, 'asname': 18, 'attr': 430, 'arg': 300, 'cause': 25, 'type': 1, 'exc': 1, 'optional_vars': 6, 'is_async': 4, 'step': 1},
                                      'all_values'    : { 'SkipTest': 1, '_ShouldStop': 1, '_UnexpectedSuccess': 1, '_Outcome': 1, '_id': 1, 'addModuleCleanup': 1, 'doModuleCleanups': 1, 'skip': 1, 'skipIf': 1, 'skipUnless': 1, 'expectedFailure': 7, '_is_subtype': 1,
                                                          '_BaseTestCaseContext': 1, '_AssertRaisesBaseCon': 1, '_AssertRaisesContext': 1, '_AssertWarnsContext': 1, '_OrderedChainMap': 1, 'TestCase': 1, 'FunctionTestCase': 1, '_SubTest': 1, 'Test case implementa': 1, None: 198,
                                                          'sys': 1, 'functools': 1, 'difflib': 1, 'pprint': 1, 're': 1, 'warnings': 3, 'collections': 1, 'contextlib': 1, 'traceback': 1, 'types': 1, 'result': 9, 'strclass': 1, 'safe_repr': 1, '_count_diff_all_purp': 1,
                                                          '_count_diff_hashable': 1, '_common_shorten_repr': 1, True: 16, 'Diff is %s characte': 1, '__init__': 9, 'testPartExecutor': 6, 'decorator': 1, '_raiseFailure': 7, 'handle': 5, '__enter__': 3, '__exit__': 3,
                                                          'ChainMap': 1, '__iter__': 1, 'addTypeEqualityFunc': 7, 'addCleanup': 1, 'addClassCleanup': 1, 'setUp': 4, 'tearDown': 4, 'setUpClass': 1, 'tearDownClass': 1, 'countTestCases': 1, 'defaultTestResult': 2,
                                                          'shortDescription': 4, 'id': 4, '__eq__': 2, '__hash__': 2, '__str__': 3, '__repr__': 2, '_addSkip': 3, 'subTest': 1, '_feedErrorsToResult': 2, '_addExpectedFailure': 2, '_addUnexpectedSucces': 2, '_callSetUp': 3,
                                                          '_callTestMethod': 3, '_callTearDown': 3, '_callCleanup': 3, 'run': 2, 'doCleanups': 2, 'doClassCleanups': 1, '__call__': 1, 'debug': 1, 'skipTest': 1, 'fail': 23, 'assertFalse': 1, 'assertTrue': 1, '_formatMessage': 28,
                                                          'assertRaises': 2, 'assertWarns': 2, 'assertLogs': 1, 'assertNoLogs': 1, '_getAssertEqualityFu': 2, '_baseAssertEqual': 3, 'assertEqual': 1, 'assertNotEqual': 1, 'assertAlmostEqual': 1, 'assertNotAlmostEqual': 1, 'assertSequenceEqual': 3,
                                                          '_truncateMessage': 5, 'assertListEqual': 2, 'assertTupleEqual': 2, 'assertSetEqual': 3, 'assertIn': 1, 'assertNotIn': 1, 'assertIs': 1, 'assertIsNot': 1, 'assertDictEqual': 2, 'assertDictContainsSu': 2, 'assertCountEqual': 1, 'assertMultiLineEqual': 2,
                                                          'assertLess': 1, 'assertLessEqual': 1, 'assertGreater': 1, 'assertGreaterEqual': 1, 'assertIsNone': 1, 'assertIsNotNone': 1, 'assertIsInstance': 5, 'assertNotIsInstance': 1, 'assertRaisesRegex': 2, 'assertWarnsRegex': 2, 'assertRegex': 1,
                                                          'assertNotRegex': 1, '_deprecate': 1, 'runTest': 4, '_subDescription': 3, 'Raise this exce': 1, 'The test should': 1, 'The test was su': 1, 'contextmanager': 2, 'obj': 5, 'function': 5, 'args': 12, 'kwargs': 11, 'Same as addCleanup,': 2,
                                                          'Execute all module c': 1, 'reason': 5, 'Unconditionally': 1, 'condition': 2, 'Skip a test if': 1, 'Skip a test unl': 1, 'test_item': 2, '__unittest_expecting': 3, 'expected': 11, 'basetype': 1, 'A context manager us': 2, 'an exception type or': 1,
                                                          'a warning type or tu': 1, 'A class whose instan': 1, False: 24, 'deprecated_func': 1, 'A test case that wra': 1, 'self': 93, 'expecting_failure': 4, 'result_supports_subt': 3, 'success': 12, 'skipped': 3, 'errors': 6, 'test_case': 14, 'isTest': 3,
                                                          'e': 5, 'append': 16, 'exc': 1, 'skip_wrapper': 1, '__unittest_skip__': 5, '__unittest_skip_why_': 5, 'FunctionType': 1, '': 20, 'standardMsg': 2, 'expected_regex': 10, 'obj_name': 7, 'msg': 37, 'name': 1, 'If args is': 1, 'exc_type': 2, 'exc_value': 2, 'tb': 2,
                                                          'exception': 1, 'GenericAlias': 1, 'warnings_manager': 3, 'maps': 1, 80: 1, 8: 1, 2: 4, 16: 1, 'methodName': 1, 'Create an instance o': 1, '_testMethodName': 9, '_outcome': 10, '_testMethodDoc': 3, 'No test': 1, '_cleanups': 6, '_subtest': 5, '_type_equality_funcs': 3, 'typeobj': 1,
                                                          'Add a type specific': 1, 'Add a function, with': 1, 'cls': 6, 'Hook method for sett': 2, 'Hook method for deco': 2, 'Returns a one-line d': 2, 'other': 2, 'params': 6, 'Return a context man': 1, 'exc_info': 4, 'method': 1, 'Execute all cleanup': 1, 'Execute all class cl': 1,
                                                          'tearDown_exceptions': 2, '_class_cleanups': 3, 'kwds': 1, 'Run the test without': 1, 'Skip this test.': 1, 'Fail immediately, wi': 1, 'expr': 2, 'Check that the expre': 2, 'Honour the longMessa': 1, 'expected_exception': 2, 'Fail unless an excep': 1, 'expected_warning': 2,
                                                          'Fail unless a warnin': 1, 'logger': 2, 'level': 2, 'Fail unless a log me': 1, '_AssertLogsContext': 2, 'Fail unless no log': 1, 'first': 8, 'second': 8, 'Get a detailed compa': 1, 'The default assertEq': 1, 'Fail if the two obje': 4, 'places': 2, 'delta': 2, 'seq1': 1, 'seq2': 1,
                                                          'seq_type': 3, 'An equality assertio': 1, 'message': 3, 'diff': 1, 'maxDiff': 1, 'list1': 1, 'list2': 1, 'A list-specific equa': 1, 'tuple1': 1, 'tuple2': 1, 'A tuple-specific equ': 1, 'set1': 1, 'set2': 1, 'A set-specific equal': 1, 'member': 2, 'container': 2, 'Just like self.asser': 8,
                                                          'expr1': 2, 'expr2': 2, 'd1': 1, 'd2': 1, 'subset': 1, 'dictionary': 1, 'Checks whether dicti': 1, 'Asserts that two ite': 1, 'Assert that two mult': 1, 'a': 4, 'b': 4, 'Same as self.assertT': 2, 'Included for symmetr': 2, 'Asserts that the mes': 2, 'text': 2, 'Fail the test unless': 1,
                                                          'unexpected_regex': 1, 'Fail the test if the': 1, 'original_func': 1, 'testFunc': 1, 'description': 1, '_setUpFunc': 6, '_tearDownFunc': 6, '_testFunc': 9, '_description': 6, '__name__': 7, '__doc__': 2, '_message': 3, 'failureException': 15, 'addSubTest': 2, 'pop': 5, 'with_traceback': 1,
                                                          'catch_warnings': 1, 'record': 1, 'simplefilter': 1, 'always': 1, 'warning': 1, 'filename': 2, 'lineno': 2, 'TestResult': 1, '%s.%s': 1, '%s (%s)': 2, '<%s testMethod=%s>': 1, 'addSkip': 1, 'addExpectedFailure': 1, 'addUnexpectedSuccess': 1, 'startTest': 1, 'longMessage': 1, 'no_logs': 2,
                                                          'sequence': 1, 'join': 9, 'First argument is no': 2, 'Second argument is n': 2, 'warn': 5, 'stacklevel': 1, 'items': 2, 'Element counts were': 1, 'unexpectedly None': 1, 'expected_regex must': 1, 'search': 4, '<%s tec=%s>': 1, 'subtests cannot be r': 1, '(<subtest>)': 1, 'format': 12, 'wraps': 1,
                                                          'compile': 3, 'clear_frames': 1, 'values': 1, '__warningregistry__': 2, 'strip': 4, 'TestResult has no ad': 3, 'addSuccess': 3, 'new_child': 1, 'startTestRun': 1, 'stopTestRun': 1, 'stopTest': 1, '__class__': 11, '%s : %s': 2, 'get': 1, '%s != %s': 3, 'specify delta or pla': 2,
                                                          '%s != %s within %s d': 1, 7: 2, '%s != %s within %r p': 1, '%s == %s within %s d': 1, '%s == %s within %r p': 1, '%ss differ: %s != %s': 1, 'difference': 2, 'Items in the first s': 1, 'Items in the second': 1, '%s not found in %s': 1, '%s unexpectedly foun': 1, '%s is not %s': 1,
                                                          'unexpectedly identic': 1, 'Missing: %s': 1, ';': 1, 'Mismatched values: %': 1, 'Counter': 2, 'splitlines': 6, 'keepends': 2, '%s not less than %s': 1, '%s not less than or': 1, '%s not greater than': 2, '%s is not None': 1, '%s is not an instanc': 1, '%s is an instance of': 1, "Regex didn't match:": 1,
                                                          'Regex matched: %r ma': 1, '{} {}': 2, '_base_type': 1, 'pattern': 4, 'modules': 1, 'failfast': 1, 'clear': 1, '%s is not false': 1, '%s is not true': 1, '%s == %s': 1, 'First %s has no leng': 1, 'First %s contains %': 1, 'ndiff': 3, 'First has %d, Second': 1, '_diffThreshold': 2, ',': 3,
                                                          '%s() arg 1 must be %': 1, '"{}" does not match': 2, '{} not triggered by': 1, '{} not triggered': 1, 'add': 1, 'First sequence is no': 1, 'Second sequence is n': 1, 'Second %s has no len': 1, 'First differing ele': 1, 'First extra element': 2, 'Second %s contains': 1, 'invalid type when at': 2,
                                                          'first argument does': 1, 'second argument does': 1, 'Please use {0} inste': 1, '[{}]': 1, '({})': 1, '_base_type_str': 1, '%r is an invalid key': 1, '{} not raised by {}': 1, '{} not raised': 1, 'no such test method': 1, 'split': 2, 'addFailure': 2, 'addError': 1, 'capitalize': 1,
                                                          'Unable to index ele': 2, 'Unable to index elem': 2, '%s, expected: %s, ac': 1, '{}={!r}': 1, 'pformat': 4, 'start': 1, 'end': 1},
                                      'ast_node_types': { 'Ast_Module': 1, 'Ast_Expr': 179, 'Ast_Import': 10, 'Ast_Import_From': 4, 'Ast_Assign': 212, 'Ast_Class_Def': 12,
                                                          'Ast_Function_Def': 109, 'Ast_Constant': 356, 'Ast_Alias': 18, 'Ast_Name': 1420, 'Ast_Call': 413, 'Ast_Arguments': 109,
                                                          'Ast_Return': 71, 'Ast_List': 13, 'Ast_While': 4, 'Ast_If': 113, 'Ast_Attribute': 430, 'Ast_Store': 267, 'Ast_Load': 1685,
                                                          'Ast_Try': 25, 'Ast_Argument': 281, 'Ast_Raise': 26, 'Ast_Unary_Op': 27, 'Ast_Bool_Op': 27, 'Ast_For': 10, 'Ast_Bin_Op': 71,
                                                          'Ast_Pass': 3, 'Ast_Except_Handler': 25, 'Ast_Tuple': 68, 'Ast_Subscript': 12, 'Ast_Not': 27, 'Ast_And': 13, 'Ast_Compare': 78,
                                                          'Ast_With': 6, 'Ast_Mult': 1, 'Ast_Pow': 1, 'Ast_Dict': 2, 'Ast_If_Exp': 1, 'Ast_Aug_Assign': 11, 'Ast_Assert': 1, 'Ast_Yield': 4,
                                                          'Ast_Generator_Exp': 3, 'Ast_Is_Not': 24, 'Ast_With_Item': 6, 'Ast_Is': 16, 'Ast_Keyword': 19, 'Ast_Continue': 2, 'Ast_Mod': 56,
                                                          'Ast_Eq': 15, 'Ast_Or': 14, 'Ast_Starred': 9, 'Ast_Add': 20, 'Ast_Not_In': 3, 'Ast_In': 1, 'Ast_Not_Eq': 8, 'Ast_List_Comp': 1,
                                                          'Ast_Comprehension': 4, 'Ast_Sub': 4, 'Ast_LtE': 3, 'Ast_Break': 3, 'Ast_Gt': 5, 'Ast_Lt': 2, 'Ast_GtE': 1, 'Ast_Slice': 1},
                                      'node_types'    : { 'Module': 1, 'Expr': 179, 'Import': 10, 'ImportFrom': 4, 'Assign': 212, 'ClassDef': 12, 'FunctionDef': 109, 'Constant': 356,
                                                          'alias': 18, 'Name': 1420, 'Call': 413, 'arguments': 109, 'Return': 71, 'List': 13, 'While': 4, 'If': 113, 'Attribute': 430,
                                                          'Store': 267, 'Load': 1685, 'Try': 25, 'arg': 281, 'Raise': 26, 'UnaryOp': 27, 'BoolOp': 27, 'For': 10, 'BinOp': 71, 'Pass': 3,
                                                          'ExceptHandler': 25, 'Tuple': 68, 'Subscript': 12, 'Not': 27, 'And': 13, 'Compare': 78, 'With': 6, 'Mult': 1, 'Pow': 1, 'Dict': 2,
                                                          'IfExp': 1, 'AugAssign': 11, 'Assert': 1, 'Yield': 4, 'GeneratorExp': 3, 'IsNot': 24, 'withitem': 6, 'Is': 16, 'keyword': 19,
                                                          'Continue': 2, 'Mod': 56, 'Eq': 15, 'Or': 14, 'Starred': 9, 'Add': 20, 'NotIn': 3, 'In': 1, 'NotEq': 8, 'ListComp': 1,
                                                          'comprehension': 4, 'Sub': 4, 'LtE': 3, 'Break': 3, 'Gt': 5, 'Lt': 2, 'GtE': 1, 'Slice': 1}}
        #print(ast_module.stats())

        for node in ast_module.all_ast_nodes():
            #if type(node) is Ast_Node:
                assert node
                assert node.info() is not None
                #print(node, node.info())
                #print()


    def test_info(self):
        info = self.ast_module.info()
        assert self.ast_module.source_code() == 'def the_answer(aaa):\n    return 42'
        assert info == { 'Ast_Module': { 'body': [ { 'Ast_Function_Def': { 'args': { 'Ast_Arguments': { 'args' : [{'Ast_Argument': {'arg': 'aaa'}}]}},
                                                                           'body': [{'Ast_Return': {'value': {'Ast_Constant': {'value': 42}}}}],
                                                                           'name': 'the_answer'}}]}}


    def test_source_code(self):
        assert self.ast_module.source_code() == "def the_answer(aaa):\n    return 42"  # note that we lost the comment (which is a known limitation of the pure python AST classes, LibCST or parso are alternatives which are able to create a CST - Concrete Syntax Tree)