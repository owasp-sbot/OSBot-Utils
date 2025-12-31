from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.Call_Flow__Edge__Factory                  import Call_Flow__Edge__Factory
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Edge          import Schema__Call_Graph__Edge
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type import Enum__Call_Graph__Edge_Type
from osbot_utils.testing.Graph__Deterministic__Ids                                  import graph_ids_for_tests
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id


class test_Call_Flow__Edge__Factory(TestCase):                                       # Test edge factory

    def test__init__(self):                                                          # Test initialization
        with Call_Flow__Edge__Factory() as _:
            pass                                                                     # Just verify it initializes

    def test__create(self):                                                          # Test generic edge creation
        with graph_ids_for_tests():
            with Call_Flow__Edge__Factory() as factory:
                from_node = Node_Id(Obj_Id())
                to_node   = Node_Id(Obj_Id())

                edge = factory.create(from_node, to_node, Enum__Call_Graph__Edge_Type.CALLS, line_number=42)

                assert type(edge)          is Schema__Call_Graph__Edge
                assert edge.from_node      == from_node
                assert edge.to_node        == to_node
                assert edge.edge_type      == Enum__Call_Graph__Edge_Type.CALLS
                assert int(edge.line_number) == 42

    def test__create_contains(self):                                                 # Test CONTAINS edge creation
        with graph_ids_for_tests():
            with Call_Flow__Edge__Factory() as factory:
                from_node = Node_Id(Obj_Id())
                to_node   = Node_Id(Obj_Id())

                edge = factory.create_contains(from_node, to_node)

                assert edge.edge_type == Enum__Call_Graph__Edge_Type.CONTAINS
                assert edge.edge_type == 'contains'

    def test__create_calls(self):                                                    # Test CALLS edge creation
        with graph_ids_for_tests():
            with Call_Flow__Edge__Factory() as factory:
                from_node = Node_Id(Obj_Id())
                to_node   = Node_Id(Obj_Id())

                edge = factory.create_calls(from_node, to_node)

                assert edge.edge_type == Enum__Call_Graph__Edge_Type.CALLS
                assert edge.edge_type == 'calls'

    def test__create_self(self):                                                     # Test SELF edge creation
        with graph_ids_for_tests():
            with Call_Flow__Edge__Factory() as factory:
                from_node = Node_Id(Obj_Id())
                to_node   = Node_Id(Obj_Id())

                edge = factory.create_self(from_node, to_node)

                assert edge.edge_type == Enum__Call_Graph__Edge_Type.SELF
                assert edge.edge_type == 'self'

    def test__create_chain(self):                                                    # Test CHAIN edge creation
        with graph_ids_for_tests():
            with Call_Flow__Edge__Factory() as factory:
                from_node = Node_Id(Obj_Id())
                to_node   = Node_Id(Obj_Id())

                edge = factory.create_chain(from_node, to_node)

                assert edge.edge_type == Enum__Call_Graph__Edge_Type.CHAIN
                assert edge.edge_type == 'chain'
