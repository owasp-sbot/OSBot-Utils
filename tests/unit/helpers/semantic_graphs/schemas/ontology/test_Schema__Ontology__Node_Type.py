# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Ontology__Node_Type - Tests for ontology node type schema
#
# Updated for Brief 3.7:
#   - Now has node_type_id (Obj_Id-based) and node_type_ref (human-readable)
#   - Removed relationships dict (now at ontology level via edge_rules)
#   - Removed taxonomy_ref field
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                    import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                   import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type       import Schema__Ontology__Node_Type
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id


class test_Schema__Ontology__Node_Type(TestCase):                                           # Test node type schema

    def test__init__(self):                                                                 # Test initialization
        node_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:class'))
        with Schema__Ontology__Node_Type(node_type_id  = node_type_id         ,
                                         node_type_ref = Node_Type_Ref('class')) as _:
            assert _.node_type_id  == node_type_id
            assert str(_.node_type_ref) == 'class'

    def test__init__types(self):                                                            # Test attribute types
        node_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:class'))
        with Schema__Ontology__Node_Type(node_type_id  = node_type_id         ,
                                         node_type_ref = Node_Type_Ref('class')) as _:
            assert type(_.node_type_id)  is Node_Type_Id
            assert type(_.node_type_ref) is Node_Type_Ref

    def test__init__default_values(self):                                                   # Test default values
        node_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:class'))
        with Schema__Ontology__Node_Type(node_type_id  = node_type_id         ,
                                         node_type_ref = Node_Type_Ref('class')) as _:
            assert _.node_type_id_source is None                                            # Optional
            assert _.description is None or str(_.description) == ''                        # Optional

    def test__with_description(self):                                                       # Test with description
        node_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:module'))
        with Schema__Ontology__Node_Type(node_type_id  = node_type_id               ,
                                         node_type_ref = Node_Type_Ref('module')    ,
                                         description   = Safe_Str__Text('Python module')) as _:
            assert str(_.node_type_ref) == 'module'
            assert str(_.description)   == 'Python module'

    def test__json_serialization(self):                                                     # Test JSON round-trip
        node_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:method'))
        original     = Schema__Ontology__Node_Type(node_type_id  = node_type_id              ,
                                                   node_type_ref = Node_Type_Ref('method')   ,
                                                   description   = Safe_Str__Text('A method'))

        json_data = original.json()
        restored  = Schema__Ontology__Node_Type.from_json(json_data)

        assert str(restored.node_type_id)  == str(original.node_type_id)
        assert str(restored.node_type_ref) == str(original.node_type_ref)
        assert str(restored.description)   == str(original.description)