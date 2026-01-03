from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Node          import Schema__Call_Graph__Node
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Node_Type import Enum__Call_Graph__Node_Type
from osbot_utils.testing.Graph__Deterministic__Ids                                  import graph_deterministic_ids, graph_ids_for_tests
from osbot_utils.testing.__                                                         import __
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label  import Safe_Str__Label


class test_Schema__Call_Graph__Node(TestCase):                                       # Test node schema

    def test__init__(self):                                                          # Test auto-initialization
        with Schema__Call_Graph__Node() as _:
            assert type(_.node_id)     is Node_Id
            assert type(_.name)        is Safe_Str__Label
            assert type(_.depth)       is Safe_UInt
            assert len(_.calls)        == 0                                          # Type_Safe__List behaves like list
            assert len(_.called_by)    == 0
            assert _.is_entry          is False
            assert _.is_external       is False

    def test__node_type__values(self):                                               # Test all node type enum values
        assert Enum__Call_Graph__Node_Type.CLASS.value    == 'class'
        assert Enum__Call_Graph__Node_Type.METHOD.value   == 'method'
        assert Enum__Call_Graph__Node_Type.FUNCTION.value == 'function'
        assert Enum__Call_Graph__Node_Type.MODULE.value   == 'module'

    def test__with_values(self):                                                     # Test with explicit values

        with graph_deterministic_ids():
            node_id = Node_Id(Obj_Id())

        with Schema__Call_Graph__Node(node_id   = node_id                            ,
                                      name      = Safe_Str__Label('test')            ,
                                      full_name = Safe_Str__Label('module.test')     ,
                                      node_type = Enum__Call_Graph__Node_Type('function'),
                                      depth     = Safe_UInt(2)                       ) as _:
            assert node_id          == 'c0000001'
            assert str(_.node_id)   == 'c0000001'
            assert str(_.name)      == 'test'
            assert str(_.full_name) == 'module.test'
            assert str(_.node_type) == 'Enum__Call_Graph__Node_Type.FUNCTION'
            assert _.node_type      == 'function'
            assert _.node_type      == Enum__Call_Graph__Node_Type.FUNCTION
            assert int(_.depth)     == 2

            assert _.obj() == __(is_entry     = False          ,
                                 is_external  = False          ,
                                 is_recursive = False          ,
                                 node_id      = 'c0000001'     ,
                                 name         = 'test'         ,
                                 full_name    = 'module.test'  ,
                                 node_type    = 'function'     ,
                                 module       = ''             ,
                                 file_path    = ''             ,
                                 depth        = 2              ,
                                 calls        = []             ,
                                 called_by    = []             ,
                                 source_code  = ''             ,
                                 line_number  = 0              )

    def test__with_node_type__class(self):                                           # Test CLASS node type
        with Schema__Call_Graph__Node(node_type = Enum__Call_Graph__Node_Type.CLASS ,
                                      is_entry  = True                              ) as _:
            assert _.node_type == Enum__Call_Graph__Node_Type.CLASS
            assert _.node_type == 'class'
            assert _.is_entry  is True

    def test__with_node_type__method(self):                                          # Test METHOD node type
        with Schema__Call_Graph__Node(node_type=Enum__Call_Graph__Node_Type.METHOD) as _:
            assert _.node_type == Enum__Call_Graph__Node_Type.METHOD
            assert _.node_type == 'method'

    def test__calls_and_called_by(self):                                             # Test call relationship lists
        with graph_ids_for_tests():
            with Schema__Call_Graph__Node() as _:
                _.calls.append(Node_Id(Obj_Id()))
                _.calls.append(Node_Id(Obj_Id()))
                _.called_by.append(Node_Id(Obj_Id()))

                assert len(_.calls)        == 2
                assert len(_.called_by)    == 1
                assert str(_.calls[0])     == 'c0000001'
                assert str(_.calls[1])     == 'c0000002'
                assert str(_.called_by[0]) == 'c0000003'
