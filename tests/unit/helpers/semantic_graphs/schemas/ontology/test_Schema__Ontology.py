# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Ontology - Tests for ontology schema (pure data)
# Note: Ontology operations have been moved to Ontology__Utils
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id         import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                    import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                     import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                     import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                  import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type       import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship    import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb          import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version             import Safe_Str__Version
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe


class test_Schema__Ontology(TestCase):                                               # Test ontology schema

    def test__init__(self):                                                          # Test initialization
        with Schema__Ontology(ontology_id = Ontology_Id('test')) as _:
            assert type(_)            is Schema__Ontology
            assert isinstance(_, Type_Safe)
            assert str(_.ontology_id) == 'test'
            assert str(_.version)     == '1.0.0'

    def test__init__types(self):                                                     # Test attribute types
        with Schema__Ontology(ontology_id = Ontology_Id('test')) as _:
            assert type(_.ontology_id)  is Ontology_Id
            assert type(_.version)      is Safe_Str__Version
            assert type(_.description)  is Safe_Str__Text
            assert type(_.taxonomy_ref) is Taxonomy_Id
            assert type(_.node_types)   is Dict__Node_Types__By_Id

    def test__init__default_values(self):                                            # Test default values
        with Schema__Ontology(ontology_id = Ontology_Id('test')) as _:
            assert str(_.version)      == '1.0.0'
            assert str(_.description)  == ''
            assert str(_.taxonomy_ref) == ''
            assert len(_.node_types)   == 0

    def test__init__with_node_types(self):                                           # Test with node types
        class_has = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('in'),
                                                   targets = [Node_Type_Id('method')])
        class_node_type = Schema__Ontology__Node_Type(description   = 'Python class',
                                                      relationships = {'has': class_has})

        with Schema__Ontology(ontology_id = Ontology_Id('test'),
                              node_types  = {'class': class_node_type}) as _:
            assert len(_.node_types)           == 1
            assert 'class'                     in _.node_types
            assert _.node_types['class']       is class_node_type

    def test__pure_data_no_methods(self):                                            # Verify no ontology operation methods
        with Schema__Ontology(ontology_id = Ontology_Id('test')) as _:
            # These methods should NOT exist on the schema (moved to Utils)
            assert not hasattr(_, 'valid_edge')        or not callable(getattr(_, 'valid_edge', None))
            assert not hasattr(_, 'get_inverse_verb')  or not callable(getattr(_, 'get_inverse_verb', None))
            assert not hasattr(_, 'all_valid_edges')   or not callable(getattr(_, 'all_valid_edges', None))
            assert not hasattr(_, 'node_type_ids')     or not callable(getattr(_, 'node_type_ids', None))
            assert not hasattr(_, 'verbs_for_node_type') or not callable(getattr(_, 'verbs_for_node_type', None))

    def test__json_serialization(self):                                              # Test JSON round-trip
        original = Schema__Ontology(ontology_id  = Ontology_Id('test_ontology'),
                                    version      = '2.0.0'                    ,
                                    description  = 'Test ontology'            ,
                                    taxonomy_ref = Taxonomy_Id('taxonomy')    )

        json_data = original.json()
        restored  = Schema__Ontology.from_json(json_data)

        assert str(restored.ontology_id)  == str(original.ontology_id)
        assert str(restored.version)      == str(original.version)
        assert str(restored.description)  == str(original.description)
        assert str(restored.taxonomy_ref) == str(original.taxonomy_ref)