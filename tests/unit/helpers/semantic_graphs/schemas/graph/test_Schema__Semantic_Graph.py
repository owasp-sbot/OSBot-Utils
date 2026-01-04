# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Semantic_Graph - Tests for semantic graph schema (pure data)
# Note: Graph operations have been moved to Semantic_Graph__Utils
#
# Updated for Brief 3.7:
#   - ontology_ref → ontology_id (ID-based foreign key)
#   - rule_set_ref → rule_set_id (ID-based foreign key)
#   - Removed version field
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id          import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph           import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                 import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                 import Rule_Set_Id
from osbot_utils.testing.Graph__Deterministic__Ids                                      import graph_ids_for_tests
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                      import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe


class test_Schema__Semantic_Graph(TestCase):                                            # Test semantic graph schema

    def test__init__(self):                                                             # Test initialization
        with graph_ids_for_tests():
            ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
            with Schema__Semantic_Graph(graph_id    = Graph_Id(Obj_Id()),
                                        ontology_id = ontology_id        ) as _:
                assert type(_)            is Schema__Semantic_Graph
                assert isinstance(_, Type_Safe)
                assert str(_.graph_id)    == 'a0000001'
                assert _.ontology_id      == ontology_id

    def test__init__types(self):                                                        # Test attribute types
        with graph_ids_for_tests():
            ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
            with Schema__Semantic_Graph(graph_id    = Graph_Id(Obj_Id()),
                                        ontology_id = ontology_id        ) as _:
                assert type(_.graph_id)    is Graph_Id
                assert type(_.ontology_id) is Ontology_Id
                assert type(_.nodes)       is Dict__Nodes__By_Id
                assert type(_.edges)       is List__Semantic_Graph__Edges

    def test__init__collections_empty(self):                                            # Test empty collections
        with graph_ids_for_tests():
            ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
            with Schema__Semantic_Graph(graph_id    = Graph_Id(Obj_Id()),
                                        ontology_id = ontology_id        ) as _:
                assert len(_.nodes) == 0
                assert len(_.edges) == 0

    def test__init__default_values(self):                                               # Test default values
        with graph_ids_for_tests():
            ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
            with Schema__Semantic_Graph(graph_id    = Graph_Id(Obj_Id()),
                                        ontology_id = ontology_id        ) as _:
                assert _.rule_set_id     is None                                        # Optional, defaults to None
                assert _.graph_id_source is None                                        # Optional, defaults to None

    def test__init__with_rule_set(self):                                                # Test with rule set ID
        with graph_ids_for_tests():
            ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
            rule_set_id = Rule_Set_Id(Obj_Id.from_seed('test:rules'))
            with Schema__Semantic_Graph(graph_id    = Graph_Id(Obj_Id()),
                                        ontology_id = ontology_id        ,
                                        rule_set_id = rule_set_id        ) as _:
                assert _.rule_set_id == rule_set_id

    def test__pure_data_no_methods(self):                                               # Verify no graph operation methods
        with graph_ids_for_tests():
            ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
            with Schema__Semantic_Graph(graph_id    = Graph_Id(Obj_Id()),
                                        ontology_id = ontology_id        ) as _:
                # These methods should NOT exist on the schema (moved to Utils)
                assert not hasattr(_, 'add_node')   or not callable(getattr(_, 'add_node', None))
                assert not hasattr(_, 'add_edge')   or not callable(getattr(_, 'add_edge', None))
                assert not hasattr(_, 'get_node')   or not callable(getattr(_, 'get_node', None))
                assert not hasattr(_, 'node_count') or not callable(getattr(_, 'node_count', None))
                assert not hasattr(_, 'edge_count') or not callable(getattr(_, 'edge_count', None))
                assert not hasattr(_, 'edges_from') or not callable(getattr(_, 'edges_from', None))
                assert not hasattr(_, 'edges_to')   or not callable(getattr(_, 'edges_to', None))
                assert not hasattr(_, 'neighbors')  or not callable(getattr(_, 'neighbors', None))

    def test__json_serialization(self):                                                 # Test JSON round-trip
        with graph_ids_for_tests():
            ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
            rule_set_id = Rule_Set_Id(Obj_Id.from_seed('test:rules'))
            original    = Schema__Semantic_Graph(graph_id    = Graph_Id(Obj_Id()),
                                                 ontology_id = ontology_id        ,
                                                 rule_set_id = rule_set_id        )

            json_data = original.json()
            restored  = Schema__Semantic_Graph.from_json(json_data)

            assert str(restored.graph_id)    == str(original.graph_id)
            assert str(restored.ontology_id) == str(original.ontology_id)
            assert str(restored.rule_set_id) == str(original.rule_set_id)