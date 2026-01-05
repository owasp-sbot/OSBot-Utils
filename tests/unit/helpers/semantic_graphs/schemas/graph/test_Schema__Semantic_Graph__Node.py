# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Semantic_Graph__Node - Tests for semantic graph node schema
#
# Updated for Brief 3.7:
#   - node_type → node_type_id (foreign key to ontology node type)
#   - name uses Safe_Str__Id type
#   - Removed line_number field
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node  import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.testing.Graph__Deterministic__Ids                                   import graph_ids_for_tests
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id      import Safe_Str__Id


class test_Schema__Semantic_Graph__Node(TestCase):                                   # Test semantic graph node schema

    def test__init__(self):                                                          # Test initialization
        with graph_ids_for_tests():
            node_type_id = Node_Type_Id(Obj_Id.from_seed('test:node_type:class'))
            with Schema__Semantic_Graph__Node(node_id      = Node_Id(Obj_Id())    ,
                                              node_type_id = node_type_id         ,
                                              name         = Safe_Str__Id('MyClass')) as _:
                assert str(_.node_id)    == 'c0000001'
                assert _.node_type_id    == node_type_id
                assert str(_.name)       == 'MyClass'

    def test__init__types(self):                                                     # Test attribute types
        with graph_ids_for_tests():
            node_type_id = Node_Type_Id(Obj_Id.from_seed('test:node_type:class'))
            with Schema__Semantic_Graph__Node(node_id      = Node_Id(Obj_Id())    ,
                                              node_type_id = node_type_id         ,
                                              name         = Safe_Str__Id('MyClass')) as _:
                assert type(_.node_id)      is Node_Id
                assert type(_.node_type_id) is Node_Type_Id
                assert type(_.name)         is Safe_Str__Id

    def test__init__default_values(self):                                            # Test default values
        with graph_ids_for_tests():
            node_type_id = Node_Type_Id(Obj_Id.from_seed('test:node_type:class'))
            with Schema__Semantic_Graph__Node(node_id      = Node_Id(Obj_Id())    ,
                                              node_type_id = node_type_id         ,
                                              name         = Safe_Str__Id('MyClass')) as _:
                assert _.node_id_source is None                                      # Optional, defaults to None

    def test__json_serialization(self):                                              # Test JSON round-trip
        with graph_ids_for_tests():
            node_type_id = Node_Type_Id(Obj_Id.from_seed('test:node_type:class'))
            original     = Schema__Semantic_Graph__Node(node_id      = Node_Id(Obj_Id())    ,
                                                        node_type_id = node_type_id         ,
                                                        name         = Safe_Str__Id('MyClass'))

            json_data = original.json()
            restored  = Schema__Semantic_Graph__Node.from_json(json_data)

            assert str(restored.node_id)      == str(original.node_id)
            assert str(restored.node_type_id) == str(original.node_type_id)
            assert str(restored.name)         == str(original.name)