# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Semantic_Graph - Tests for semantic graph schema (pure data)
# Note: Graph operations have been moved to Semantic_Graph__Utils
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id       import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph        import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id              import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id              import Rule_Set_Id
from osbot_utils.testing.Graph__Deterministic__Ids                                   import graph_ids_for_tests
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version      import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                   import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe


class test_Schema__Semantic_Graph(TestCase):                                         # Test semantic graph schema

    def test__init__(self):                                                          # Test initialization
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                        ontology_ref = Ontology_Id('test')) as _:
                assert type(_)             is Schema__Semantic_Graph
                assert isinstance(_, Type_Safe)
                assert str(_.graph_id)     == 'a0000001'
                assert str(_.ontology_ref) == 'test'
                assert str(_.version)      == '1.0.0'

    def test__init__types(self):                                                     # Test attribute types
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                        ontology_ref = Ontology_Id('test')) as _:
                assert type(_.graph_id)     is Graph_Id
                assert type(_.version)      is Safe_Str__Version
                assert type(_.ontology_ref) is Ontology_Id
                assert type(_.rule_set_ref) is Rule_Set_Id
                assert type(_.nodes)        is Dict__Nodes__By_Id
                assert type(_.edges)        is List__Semantic_Graph__Edges

    def test__init__collections_empty(self):                                         # Test empty collections
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                        ontology_ref = Ontology_Id('test')) as _:
                assert len(_.nodes) == 0
                assert len(_.edges) == 0

    def test__init__default_values(self):                                            # Test default values
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                        ontology_ref = Ontology_Id('test')) as _:
                assert str(_.version)      == '1.0.0'                                # Default version
                assert str(_.rule_set_ref) == ''                                     # Empty rule set ref

    def test__init__with_rule_set(self):                                             # Test with rule set ref
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                        ontology_ref = Ontology_Id('test'),
                                        rule_set_ref = Rule_Set_Id('rules')) as _:
                assert str(_.rule_set_ref) == 'rules'

    def test__pure_data_no_methods(self):                                            # Verify no graph operation methods
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                        ontology_ref = Ontology_Id('test')) as _:
                # These methods should NOT exist on the schema (moved to Utils)
                assert not hasattr(_, 'add_node')       or not callable(getattr(_, 'add_node', None))
                assert not hasattr(_, 'add_edge')       or not callable(getattr(_, 'add_edge', None))
                assert not hasattr(_, 'get_node')       or not callable(getattr(_, 'get_node', None))
                assert not hasattr(_, 'node_count')     or not callable(getattr(_, 'node_count', None))
                assert not hasattr(_, 'edge_count')     or not callable(getattr(_, 'edge_count', None))
                assert not hasattr(_, 'edges_from')     or not callable(getattr(_, 'edges_from', None))
                assert not hasattr(_, 'edges_to')       or not callable(getattr(_, 'edges_to', None))
                assert not hasattr(_, 'neighbors')      or not callable(getattr(_, 'neighbors', None))

    def test__json_serialization(self):                                              # Test JSON round-trip
        with graph_ids_for_tests():
            original = Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                              ontology_ref = Ontology_Id('test'),
                                              rule_set_ref = Rule_Set_Id('rules'))

            json_data   = original.json()
            restored    = Schema__Semantic_Graph.from_json(json_data)

            assert str(restored.graph_id)     == str(original.graph_id)
            assert str(restored.ontology_ref) == str(original.ontology_ref)
            assert str(restored.rule_set_ref) == str(original.rule_set_ref)
            assert str(restored.version)      == str(original.version)