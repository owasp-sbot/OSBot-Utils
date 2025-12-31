from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Edge          import Schema__Call_Graph__Edge
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type import Enum__Call_Graph__Edge_Type
from osbot_utils.testing.Graph__Deterministic__Ids                                  import test_graph_ids
from osbot_utils.testing.__                                                         import __
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt


class test_Schema__Call_Graph__Edge(TestCase):                                       # Test edge schema

    def test__init__(self):                                                          # Test auto-initialization
        with Schema__Call_Graph__Edge() as _:
            assert type(_.edge_id)   is Edge_Id
            assert type(_.from_node) is Node_Id
            assert type(_.to_node)   is Node_Id

    def test__edge_type__values(self):                                               # Test all edge type enum values
        assert Enum__Call_Graph__Edge_Type.CONTAINS.value == 'contains'
        assert Enum__Call_Graph__Edge_Type.CALLS.value    == 'calls'
        assert Enum__Call_Graph__Edge_Type.SELF.value     == 'self'
        assert Enum__Call_Graph__Edge_Type.CHAIN.value    == 'chain'

    def test__with_edge_type__contains(self):                                        # Test CONTAINS edge type
        with Schema__Call_Graph__Edge(edge_type=Enum__Call_Graph__Edge_Type.CONTAINS) as _:
            assert _.edge_type == Enum__Call_Graph__Edge_Type.CONTAINS
            assert _.edge_type == 'contains'

    def test__with_edge_type__calls(self):                                           # Test CALLS edge type
        with Schema__Call_Graph__Edge(edge_type=Enum__Call_Graph__Edge_Type.CALLS) as _:
            assert _.edge_type == Enum__Call_Graph__Edge_Type.CALLS
            assert _.edge_type == 'calls'

    def test__with_edge_type__self(self):                                            # Test SELF edge type
        with Schema__Call_Graph__Edge(edge_type=Enum__Call_Graph__Edge_Type.SELF) as _:
            assert _.edge_type == Enum__Call_Graph__Edge_Type.SELF
            assert _.edge_type == 'self'

    def test__with_edge_type__chain(self):                                           # Test CHAIN edge type
        with Schema__Call_Graph__Edge(edge_type=Enum__Call_Graph__Edge_Type.CHAIN) as _:
            assert _.edge_type == Enum__Call_Graph__Edge_Type.CHAIN
            assert _.edge_type == 'chain'

    def test__with_values(self):                                                     # Test with explicit values
        with test_graph_ids():
            with Schema__Call_Graph__Edge(edge_id        = Edge_Id(Obj_Id())                ,
                                          from_node      = Node_Id(Obj_Id())                ,
                                          to_node        = Node_Id(Obj_Id())                ,
                                          edge_type      = Enum__Call_Graph__Edge_Type.SELF ,
                                          line_number    = Safe_UInt(42)                    ,
                                          is_conditional = True                             ) as _:

                assert _.obj() == __(edge_id        = 'e0000001' ,
                                     from_node      = 'c0000001' ,
                                     to_node        = 'c0000002' ,
                                     edge_type      = 'self'     ,
                                     line_number    = 42         ,
                                     is_conditional = True       )
