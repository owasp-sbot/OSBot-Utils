from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.Call_Flow__AST__Extractor                 import Call_Flow__AST__Extractor
from osbot_utils.helpers.python_call_flow.Call_Flow__Call__Resolver                 import Call_Flow__Call__Resolver
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call__Info                import Schema__Call__Info
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Config        import Schema__Call_Graph__Config
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type import Enum__Call_Graph__Edge_Type


# ═══════════════════════════════════════════════════════════════════════════════
# Test Fixtures
# ═══════════════════════════════════════════════════════════════════════════════

def function_with_direct_call():                                                     # Direct function call
    helper()


def helper():                                                                        # Helper function
    pass


def function_with_chain_call():                                                      # Chain call (obj.method)
    items = []
    items.append(1)


class Sample__Class:                                                                 # Class with self calls
    def run(self):
        self.helper()
        self.process()

    def helper(self):
        pass

    def process(self):
        return self.helper()


class Sample__Child(Sample__Class):                                                  # Child class for inheritance testing
    def child_method(self):
        self.helper()                                                                # Inherited from parent


# ═══════════════════════════════════════════════════════════════════════════════
# Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_Call_Flow__Call__Resolver(TestCase):                                      # Test call resolver

    @classmethod
    def setUpClass(cls):                                                             # Shared setup
        cls.extractor = Call_Flow__AST__Extractor()

    def test__init__(self):                                                          # Test initialization
        with Call_Flow__Call__Resolver() as _:
            assert type(_.config) is Schema__Call_Graph__Config

    def test__resolve__direct_call(self):                                            # Test resolving direct function call
        with Call_Flow__Call__Resolver() as resolver:
            calls     = self.extractor.extract_calls(function_with_direct_call)
            call_info = resolver.resolve(calls[0])

            assert type(call_info)    is Schema__Call__Info
            assert str(call_info.name) == 'helper'
            assert call_info.edge_type == Enum__Call_Graph__Edge_Type.CALLS

    def test__resolve__chain_call(self):                                             # Test resolving chain call (obj.method)
        with Call_Flow__Call__Resolver() as resolver:
            calls     = self.extractor.extract_calls(function_with_chain_call)
            call_info = resolver.resolve(calls[0])                                   # items.append

            assert type(call_info)     is Schema__Call__Info
            assert call_info.edge_type == Enum__Call_Graph__Edge_Type.CHAIN

    def test__resolve__self_call(self):                                              # Test resolving self.method() call
        with Call_Flow__Call__Resolver() as resolver:
            calls     = self.extractor.extract_calls(Sample__Class.run)
            call_info = resolver.resolve(calls[0], class_context=Sample__Class)      # self.helper()

            assert type(call_info)      is Schema__Call__Info
            assert str(call_info.name)  == 'helper'
            assert call_info.edge_type  == Enum__Call_Graph__Edge_Type.SELF
            assert call_info.class_ref  is Sample__Class
            assert call_info.resolved   is not None                                  # Should resolve to actual method

    def test__resolve__self_call__resolved_method(self):                             # Test self call resolves to actual method
        with Call_Flow__Call__Resolver() as resolver:
            calls     = self.extractor.extract_calls(Sample__Class.run)
            call_info = resolver.resolve(calls[0], class_context=Sample__Class)

            assert call_info.resolved is Sample__Class.helper                        # Should be the actual method

    def test__resolve__self_call__without_context(self):                             # Test self call without class context
        with Call_Flow__Call__Resolver() as resolver:
            calls     = self.extractor.extract_calls(Sample__Class.run)
            call_info = resolver.resolve(calls[0], class_context=None)               # No class context

            assert call_info.edge_type == Enum__Call_Graph__Edge_Type.CHAIN          # Falls back to CHAIN

    def test__resolve__self_call__resolve_disabled(self):                            # Test self call with resolution disabled
        config = Schema__Call_Graph__Config(resolve_self_calls=False)
        with Call_Flow__Call__Resolver(config=config) as resolver:
            calls     = self.extractor.extract_calls(Sample__Class.run)
            call_info = resolver.resolve(calls[0], class_context=Sample__Class)

            assert call_info.edge_type == Enum__Call_Graph__Edge_Type.CHAIN          # Falls back to CHAIN

    def test__resolve_self_method__direct(self):                                     # Test resolve_self_method directly
        with Call_Flow__Call__Resolver() as resolver:
            method = resolver.resolve_self_method('helper', Sample__Class)
            assert method is Sample__Class.helper

    def test__resolve_self_method__inherited(self):                                  # Test resolving inherited method
        with Call_Flow__Call__Resolver() as resolver:
            method = resolver.resolve_self_method('helper', Sample__Child)           # helper is in parent
            assert method is Sample__Class.helper                                    # Should find in parent

    def test__resolve_self_method__not_found(self):                                  # Test method not found
        with Call_Flow__Call__Resolver() as resolver:
            method = resolver.resolve_self_method('nonexistent', Sample__Class)
            assert method is None

    def test__extract_call_name(self):                                               # Test call name extraction
        with Call_Flow__Call__Resolver() as resolver:
            calls = self.extractor.extract_calls(function_with_direct_call)
            name  = resolver.extract_call_name(calls[0])

            assert name == 'helper'

    def test__extract_func_node(self):                                               # Test func node extraction
        with Call_Flow__Call__Resolver() as resolver:
            calls     = self.extractor.extract_calls(function_with_direct_call)
            func_node = resolver.extract_func_node(calls[0])

            assert func_node is not None
            assert type(func_node).__name__ == 'Ast_Name'                            # Direct call is Ast_Name

    def test__extract_func_node__attribute(self):                                    # Test func node for attribute call
        with Call_Flow__Call__Resolver() as resolver:
            calls     = self.extractor.extract_calls(Sample__Class.run)
            func_node = resolver.extract_func_node(calls[0])                         # self.helper()

            assert func_node is not None
            assert type(func_node).__name__ == 'Ast_Attribute'                       # self.x is Ast_Attribute

    def test__extract_line_number(self):                                             # Test line number extraction
        with Call_Flow__Call__Resolver() as resolver:
            calls       = self.extractor.extract_calls(function_with_direct_call)
            line_number = resolver.extract_line_number(calls[0])

            assert type(line_number) is int
            assert line_number > 0

    def test__resolve__returns_line_number(self):                                    # Test resolved call has line number
        with Call_Flow__Call__Resolver() as resolver:
            calls     = self.extractor.extract_calls(function_with_direct_call)
            call_info = resolver.resolve(calls[0])

            assert int(call_info.line_number) > 0


    def test__edge_type__calls(self):                                                # Test CALLS edge type
        with Call_Flow__Call__Resolver() as resolver:
            calls     = self.extractor.extract_calls(function_with_direct_call)
            call_info = resolver.resolve(calls[0])

            assert call_info.edge_type == Enum__Call_Graph__Edge_Type.CALLS
            assert call_info.edge_type == 'calls'

    def test__edge_type__self(self):                                                 # Test SELF edge type
        with Call_Flow__Call__Resolver() as resolver:
            calls     = self.extractor.extract_calls(Sample__Class.run)
            call_info = resolver.resolve(calls[0], class_context=Sample__Class)

            assert call_info.edge_type == Enum__Call_Graph__Edge_Type.SELF
            assert call_info.edge_type == 'self'

    def test__edge_type__chain(self):                                                # Test CHAIN edge type
        with Call_Flow__Call__Resolver() as resolver:
            calls     = self.extractor.extract_calls(function_with_chain_call)
            call_info = resolver.resolve(calls[0])

            assert call_info.edge_type == Enum__Call_Graph__Edge_Type.CHAIN
            assert call_info.edge_type == 'chain'