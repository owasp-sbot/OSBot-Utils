# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Semantic_Graph__Edge - Tests for semantic graph edge schema
#
# Updated for Brief 3.7:
#   - from_node → from_node_id (foreign key to node)
#   - to_node → to_node_id (foreign key to node)
#   - verb → predicate_id (foreign key to ontology predicate)
#   - Removed line_number field
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge  import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id             import Predicate_Id
from osbot_utils.testing.Graph__Deterministic__Ids                                   import graph_ids_for_tests
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                    import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id


class test_Schema__Semantic_Graph__Edge(TestCase):                                   # Test semantic graph edge schema

    def test__init__(self):                                                          # Test initialization
        with graph_ids_for_tests():
            predicate_id = Predicate_Id(Obj_Id.from_seed('test:predicate:contains'))
            with Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()) ,
                                              from_node_id = Node_Id(Obj_Id()) ,
                                              predicate_id = predicate_id      ,
                                              to_node_id   = Node_Id(Obj_Id()) ) as _:
                assert str(_.edge_id)      == 'e0000001'
                assert str(_.from_node_id) == 'c0000001'
                assert _.predicate_id      == predicate_id
                assert str(_.to_node_id)   == 'c0000002'

    def test__init__types(self):                                                     # Test attribute types
        with graph_ids_for_tests():
            predicate_id = Predicate_Id(Obj_Id.from_seed('test:predicate:contains'))
            with Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()) ,
                                              from_node_id = Node_Id(Obj_Id()) ,
                                              predicate_id = predicate_id      ,
                                              to_node_id   = Node_Id(Obj_Id()) ) as _:
                assert type(_.edge_id)      is Edge_Id
                assert type(_.from_node_id) is Node_Id
                assert type(_.predicate_id) is Predicate_Id
                assert type(_.to_node_id)   is Node_Id

    def test__init__default_values(self):                                            # Test default values
        with graph_ids_for_tests():
            predicate_id = Predicate_Id(Obj_Id.from_seed('test:predicate:contains'))
            with Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()) ,
                                              from_node_id = Node_Id(Obj_Id()) ,
                                              predicate_id = predicate_id      ,
                                              to_node_id   = Node_Id(Obj_Id()) ) as _:
                assert _.edge_id_source is None                                      # Optional, defaults to None

    def test__json_serialization(self):                                              # Test JSON round-trip
        with graph_ids_for_tests():
            predicate_id = Predicate_Id(Obj_Id.from_seed('test:predicate:contains'))
            original     = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()) ,
                                                        from_node_id = Node_Id(Obj_Id()) ,
                                                        predicate_id = predicate_id      ,
                                                        to_node_id   = Node_Id(Obj_Id()) )

            json_data = original.json()
            restored  = Schema__Semantic_Graph__Edge.from_json(json_data)

            assert str(restored.edge_id)      == str(original.edge_id)
            assert str(restored.from_node_id) == str(original.from_node_id)
            assert str(restored.predicate_id) == str(original.predicate_id)
            assert str(restored.to_node_id)   == str(original.to_node_id)