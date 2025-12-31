from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.Call_Flow__AST__Extractor                 import Call_Flow__AST__Extractor


# ═══════════════════════════════════════════════════════════════════════════════
# Test Fixtures
# ═══════════════════════════════════════════════════════════════════════════════

def simple_function():                                                               # Function with no calls
    x = 1
    return x


def function_with_calls():                                                           # Function with multiple calls
    print("hello")
    len([1, 2, 3])
    result = str(42)
    return result


def function_with_method_calls():                                                    # Function with method calls
    items = []
    items.append(1)
    items.extend([2, 3])
    return items


class Sample__Class:                                                                 # Class for testing method extraction
    def method_with_self_calls(self):
        self.helper()
        self.process()

    def helper(self):
        pass

    def process(self):
        self.helper()


# ═══════════════════════════════════════════════════════════════════════════════
# Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_Call_Flow__AST__Extractor(TestCase):                                      # Test AST extractor

    def test__init__(self):                                                          # Test initialization
        with Call_Flow__AST__Extractor() as _:
            pass                                                                     # Just verify it initializes

    def test__extract_calls__no_calls(self):                                         # Test function with no calls
        with Call_Flow__AST__Extractor() as extractor:
            calls = extractor.extract_calls(simple_function)

            assert type(calls) is list
            assert len(calls)  == 0

    def test__extract_calls__with_calls(self):                                       # Test function with calls
        with Call_Flow__AST__Extractor() as extractor:
            calls = extractor.extract_calls(function_with_calls)

            assert len(calls) == 3                                                   # print, len, str
            call_names = [c.name() for c in calls]
            assert 'print' in call_names
            assert 'len'   in call_names
            assert 'str'   in call_names

    def test__extract_calls__method_calls(self):                                     # Test function with method calls
        with Call_Flow__AST__Extractor() as extractor:
            calls = extractor.extract_calls(function_with_method_calls)

            assert len(calls) >= 2                                                   # append, extend
            call_names = [c.name() for c in calls]
            assert 'items.append' in call_names or 'append' in call_names
            assert 'items.extend' in call_names or 'extend' in call_names

    def test__extract_calls__self_calls(self):                                       # Test method with self.x() calls
        with Call_Flow__AST__Extractor() as extractor:
            method = Sample__Class.method_with_self_calls
            calls  = extractor.extract_calls(method)

            assert len(calls) == 2                                                   # self.helper, self.process

    def test__extract_calls__nested_self_calls(self):                                # Test nested self calls
        with Call_Flow__AST__Extractor() as extractor:
            method = Sample__Class.process
            calls  = extractor.extract_calls(method)

            assert len(calls) == 1                                                   # self.helper

    def test__extract_calls__builtin_no_source(self):                                # Test builtin (no source available)
        with Call_Flow__AST__Extractor() as extractor:
            calls = extractor.extract_calls(print)                                   # Builtin has no source

            assert calls == []                                                       # Should return empty list

    def test__can_parse__valid_function(self):                                       # Test can_parse with valid function
        with Call_Flow__AST__Extractor() as extractor:
            assert extractor.can_parse(simple_function)      is True
            assert extractor.can_parse(function_with_calls)  is True

    def test__can_parse__builtin(self):                                              # Test can_parse with builtin
        with Call_Flow__AST__Extractor() as extractor:
            assert extractor.can_parse(print) is False                               # Builtins have no source
            assert extractor.can_parse(len)   is False

    def test__can_parse__class_method(self):                                         # Test can_parse with class method
        with Call_Flow__AST__Extractor() as extractor:
            assert extractor.can_parse(Sample__Class.helper)  is True
            assert extractor.can_parse(Sample__Class.process) is True

    def test__extract_calls__returns_ast_call_objects(self):                         # Test return type is Ast_Call
        with Call_Flow__AST__Extractor() as extractor:
            calls = extractor.extract_calls(function_with_calls)

            for call in calls:
                assert type(call).__name__ == 'Ast_Call'                             # Should be Ast_Call objects
                assert hasattr(call, 'name')                                         # Has name method
                assert hasattr(call, 'func')                                         # Has func method