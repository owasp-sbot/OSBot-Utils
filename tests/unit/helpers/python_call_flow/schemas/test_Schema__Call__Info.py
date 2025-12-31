from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call__Info                import Schema__Call__Info
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type import Enum__Call_Graph__Edge_Type
from osbot_utils.testing.__                                                         import __
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label  import Safe_Str__Label
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt


class test_Schema__Call__Info(TestCase):                                             # Test call info schema

    def test__init__(self):                                                          # Test initialization
        with Schema__Call__Info() as _:
            assert type(_.name)        is Safe_Str__Label
            assert type(_.line_number) is Safe_UInt
            assert _.resolved          is None
            assert _.class_ref         is None

    def test__with_values(self):                                                     # Test with explicit values
        with Schema__Call__Info(name        = Safe_Str__Label('test_method')              ,
                                edge_type   = Enum__Call_Graph__Edge_Type.SELF            ,
                                resolved    = None                                        ,
                                class_ref   = None                                        ,
                                line_number = Safe_UInt(42)                               ) as _:

            assert str(_.name)         == 'test_method'
            assert _.edge_type         == Enum__Call_Graph__Edge_Type.SELF
            assert _.edge_type         == 'self'
            assert int(_.line_number)  == 42

    def test__edge_type__calls(self):                                                # Test CALLS edge type
        with Schema__Call__Info(edge_type=Enum__Call_Graph__Edge_Type.CALLS) as _:
            assert _.edge_type == 'calls'

    def test__edge_type__chain(self):                                                # Test CHAIN edge type
        with Schema__Call__Info(edge_type=Enum__Call_Graph__Edge_Type.CHAIN) as _:
            assert _.edge_type == 'chain'

    def test__with_resolved(self):                                                   # Test with resolved function
        def sample_func():
            pass

        with Schema__Call__Info(name        = Safe_Str__Label('sample_func')              ,
                                edge_type   = Enum__Call_Graph__Edge_Type.CALLS           ,
                                resolved    = sample_func                                 ) as _:
            assert _.resolved is sample_func

    def test__with_class_ref(self):                                                  # Test with class reference
        class SampleClass:
            pass

        with Schema__Call__Info(name        = Safe_Str__Label('method')                   ,
                                edge_type   = Enum__Call_Graph__Edge_Type.SELF            ,
                                class_ref   = SampleClass                                 ) as _:
            assert _.class_ref is SampleClass
