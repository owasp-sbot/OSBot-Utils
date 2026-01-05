# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Ontology__Node_Type - Tests for ontology node type schema
#
# Updated for Brief 3.8:
#   - Added category_id (Category_Id) linking to taxonomy category
#   - Node types are categorized in taxonomy hierarchy
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                     import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                    import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                   import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type       import Schema__Ontology__Node_Type
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id


class test_Schema__Ontology__Node_Type(TestCase):                                           # Test node type schema

    def test__init__(self):                                                                 # Test initialization
        node_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:class'))
        category_id  = Category_Id(Obj_Id.from_seed('test:cat:callable'))
        with Schema__Ontology__Node_Type(node_type_id  = node_type_id          ,
                                         node_type_ref = Node_Type_Ref('class'),
                                         category_id   = category_id           ) as _:
            assert _.node_type_id       == node_type_id
            assert str(_.node_type_ref) == 'class'
            assert _.category_id        == category_id                                      # Brief 3.8

    def test__init__types(self):                                                            # Test attribute types
        node_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:class'))
        category_id  = Category_Id(Obj_Id.from_seed('test:cat:callable'))
        with Schema__Ontology__Node_Type(node_type_id  = node_type_id          ,
                                         node_type_ref = Node_Type_Ref('class'),
                                         category_id   = category_id           ) as _:
            assert type(_.node_type_id)  is Node_Type_Id
            assert type(_.node_type_ref) is Node_Type_Ref
            assert type(_.category_id)   is Category_Id                                     # Brief 3.8

    def test__init__default_values(self):                                                   # Test default values
        node_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:class'))
        category_id  = Category_Id(Obj_Id.from_seed('test:cat:callable'))
        with Schema__Ontology__Node_Type(node_type_id  = node_type_id          ,
                                         node_type_ref = Node_Type_Ref('class'),
                                         category_id   = category_id           ) as _:
            assert _.node_type_id_source is None                                            # Optional


    def test__category_id__links_to_taxonomy(self):                                         # Brief 3.8: category link
        node_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:method'))
        category_id  = Category_Id(Obj_Id.from_seed('test:cat:callable'))

        with Schema__Ontology__Node_Type(node_type_id  = node_type_id           ,
                                         node_type_ref = Node_Type_Ref('method'),
                                         category_id   = category_id            ) as _:
            # category_id is a foreign key to taxonomy
            assert type(_.category_id) is Category_Id
            assert _.category_id       == category_id

    def test__json_serialization(self):                                                     # Test JSON round-trip
        node_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:method'))
        category_id  = Category_Id(Obj_Id.from_seed('test:cat:callable'))
        original     = Schema__Ontology__Node_Type(node_type_id  = node_type_id              ,
                                                   node_type_ref = Node_Type_Ref('method')   ,
                                                   category_id   = category_id               )

        json_data = original.json()
        restored  = Schema__Ontology__Node_Type.from_json(json_data)

        assert str(restored.node_type_id)  == str(original.node_type_id)
        assert str(restored.node_type_ref) == str(original.node_type_ref)
        assert str(restored.category_id)   == str(original.category_id)                     # Brief 3.8