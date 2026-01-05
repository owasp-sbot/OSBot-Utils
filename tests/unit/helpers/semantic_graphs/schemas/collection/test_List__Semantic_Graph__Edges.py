# ═══════════════════════════════════════════════════════════════════════════════
# Test List__Semantic_Graph__Edges - Tests for edge list typed collection
#
# Updated for Brief 3.7:
#   - from_node → from_node_id
#   - to_node → to_node_id
#   - verb → predicate_id (Obj_Id-based foreign key)
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge     import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                import Predicate_Id
from osbot_utils.testing.Graph__Deterministic__Ids                                      import graph_ids_for_tests
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                       import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                       import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                   import Type_Safe__List


class test_List__Semantic_Graph__Edges(TestCase):                                       # Test edge list collection

    @classmethod
    def setUpClass(cls):                                                                # Cache predicate IDs for tests
        cls.has_pred_id   = Predicate_Id(Obj_Id.from_seed('test:pred:has'))
        cls.calls_pred_id = Predicate_Id(Obj_Id.from_seed('test:pred:calls'))

    def test__init__(self):                                                             # Test initialization
        with List__Semantic_Graph__Edges() as _:
            assert type(_)           is List__Semantic_Graph__Edges
            assert isinstance(_, Type_Safe__List)
            assert _.expected_type   is Schema__Semantic_Graph__Edge
            assert len(_)            == 0

    def test__append_and_retrieve(self):                                                # Test appending and retrieving edges
        with graph_ids_for_tests():
            with List__Semantic_Graph__Edges() as _:
                edge = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()),
                                                    from_node_id = Node_Id(Obj_Id()),
                                                    predicate_id = self.has_pred_id ,
                                                    to_node_id   = Node_Id(Obj_Id()))
                _.append(edge)

                assert len(_)  == 1
                assert _[0]    is edge

    def test__multiple_edges(self):                                                     # Test multiple edge operations
        with graph_ids_for_tests():
            with List__Semantic_Graph__Edges() as _:
                edge1 = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()),
                                                     from_node_id = Node_Id(Obj_Id()),
                                                     predicate_id = self.has_pred_id ,
                                                     to_node_id   = Node_Id(Obj_Id()))
                edge2 = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()),
                                                     from_node_id = Node_Id(Obj_Id()),
                                                     predicate_id = self.calls_pred_id,
                                                     to_node_id   = Node_Id(Obj_Id()))
                _.append(edge1)
                _.append(edge2)

                assert len(_) == 2
                assert _[0]   is edge1
                assert _[1]   is edge2

    def test__iteration(self):                                                          # Test iteration over edges
        with graph_ids_for_tests():
            with List__Semantic_Graph__Edges() as _:
                edge1 = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()),
                                                     from_node_id = Node_Id(Obj_Id()),
                                                     predicate_id = self.has_pred_id ,
                                                     to_node_id   = Node_Id(Obj_Id()))
                edge2 = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()),
                                                     from_node_id = Node_Id(Obj_Id()),
                                                     predicate_id = self.calls_pred_id,
                                                     to_node_id   = Node_Id(Obj_Id()))
                _.append(edge1)
                _.append(edge2)

                edges = list(_)
                assert len(edges) == 2
                assert edge1 in edges
                assert edge2 in edges

    def test__extend(self):                                                             # Test extend operation
        with graph_ids_for_tests():
            with List__Semantic_Graph__Edges() as _:
                edge1 = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()),
                                                     from_node_id = Node_Id(Obj_Id()),
                                                     predicate_id = self.has_pred_id ,
                                                     to_node_id   = Node_Id(Obj_Id()))
                edge2 = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()),
                                                     from_node_id = Node_Id(Obj_Id()),
                                                     predicate_id = self.calls_pred_id,
                                                     to_node_id   = Node_Id(Obj_Id()))
                _.extend([edge1, edge2])

                assert len(_) == 2

    def test__contains(self):                                                           # Test membership check
        with graph_ids_for_tests():
            with List__Semantic_Graph__Edges() as _:
                edge1 = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()),
                                                     from_node_id = Node_Id(Obj_Id()),
                                                     predicate_id = self.has_pred_id ,
                                                     to_node_id   = Node_Id(Obj_Id()))
                edge2 = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id()),
                                                     from_node_id = Node_Id(Obj_Id()),
                                                     predicate_id = self.calls_pred_id,
                                                     to_node_id   = Node_Id(Obj_Id()))
                _.append(edge1)

                assert edge1 in _
                assert edge2 not in _