# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Ontology - Tests for ontology schema (pure data)
# Note: Ontology operations have been moved to Ontology__Utils
#
# Updated for Brief 3.7:
#   - ontology_id is Obj_Id-based (not string)
#   - ontology_ref is the human-readable name
#   - taxonomy_ref → taxonomy_id (foreign key)
#   - Removed version field
#   - node_types keyed by Node_Type_Id (not string)
#   - Added predicates dict and edge_rules list
#   - Removed embedded relationships (now in edge_rules)
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id         import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicates__By_Id         import Dict__Predicates__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Edge_Rules                import List__Edge_Rules
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                    import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                   import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                     import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                    import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                    import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref                   import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                     import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                  import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Edge_Rule       import Schema__Ontology__Edge_Rule
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type       import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Predicate       import Schema__Ontology__Predicate
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe


class test_Schema__Ontology(TestCase):                                                      # Test ontology schema

    def test__init__(self):                                                                 # Test initialization
        ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        with Schema__Ontology(ontology_id  = ontology_id              ,
                              ontology_ref = Ontology_Ref('test')     ) as _:
            assert type(_)            is Schema__Ontology
            assert isinstance(_, Type_Safe)
            assert _.ontology_id      == ontology_id
            assert str(_.ontology_ref) == 'test'

    def test__init__types(self):                                                            # Test attribute types
        ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        with Schema__Ontology(ontology_id  = ontology_id              ,
                              ontology_ref = Ontology_Ref('test')     ) as _:
            assert type(_.ontology_id)  is Ontology_Id
            assert type(_.ontology_ref) is Ontology_Ref
            assert type(_.node_types)   is Dict__Node_Types__By_Id
            assert type(_.predicates)   is Dict__Predicates__By_Id
            assert type(_.edge_rules)   is List__Edge_Rules

    def test__init__default_values(self):                                                   # Test default values
        ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        with Schema__Ontology(ontology_id  = ontology_id              ,
                              ontology_ref = Ontology_Ref('test')     ) as _:
            assert _.description is None or str(_.description) == ''
            assert _.taxonomy_id is None
            assert len(_.node_types) == 0
            assert len(_.predicates) == 0
            assert len(_.edge_rules) == 0

    def test__init__with_node_types(self):                                                  # Test with node types
        ontology_id   = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        class_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:class'))

        class_node_type = Schema__Ontology__Node_Type(node_type_id  = class_type_id         ,
                                                      node_type_ref = Node_Type_Ref('class'),
                                                      description   = Safe_Str__Text('Python class'))

        node_types = Dict__Node_Types__By_Id()
        node_types[class_type_id] = class_node_type

        with Schema__Ontology(ontology_id  = ontology_id              ,
                              ontology_ref = Ontology_Ref('test')     ,
                              node_types   = node_types               ) as _:
            assert len(_.node_types)            == 1
            assert class_type_id                in _.node_types
            assert _.node_types[class_type_id]  is class_node_type

    def test__init__with_predicates(self):                                                  # Test with predicates
        ontology_id   = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        contains_id   = Predicate_Id(Obj_Id.from_seed('test:pred:contains'))
        in_id         = Predicate_Id(Obj_Id.from_seed('test:pred:in'))

        contains_pred = Schema__Ontology__Predicate(predicate_id  = contains_id               ,
                                                    predicate_ref = Predicate_Ref('contains') ,
                                                    inverse_id    = in_id                     )
        in_pred       = Schema__Ontology__Predicate(predicate_id  = in_id                     ,
                                                    predicate_ref = Predicate_Ref('in')       ,
                                                    inverse_id    = contains_id               )

        predicates = Dict__Predicates__By_Id()
        predicates[contains_id] = contains_pred
        predicates[in_id]       = in_pred

        with Schema__Ontology(ontology_id  = ontology_id              ,
                              ontology_ref = Ontology_Ref('test')     ,
                              predicates   = predicates               ) as _:
            assert len(_.predicates)         == 2
            assert contains_id               in _.predicates
            assert _.predicates[contains_id] is contains_pred

    def test__init__with_edge_rules(self):                                                  # Test with edge rules
        ontology_id   = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        class_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:class'))
        method_type_id= Node_Type_Id(Obj_Id.from_seed('test:nt:method'))
        contains_id   = Predicate_Id(Obj_Id.from_seed('test:pred:contains'))

        edge_rules = List__Edge_Rules()
        edge_rules.append(Schema__Ontology__Edge_Rule(source_type_id = class_type_id ,
                                                      predicate_id   = contains_id   ,
                                                      target_type_id = method_type_id))

        with Schema__Ontology(ontology_id  = ontology_id              ,
                              ontology_ref = Ontology_Ref('test')     ,
                              edge_rules   = edge_rules               ) as _:
            assert len(_.edge_rules) == 1
            assert _.edge_rules[0].source_type_id == class_type_id
            assert _.edge_rules[0].predicate_id   == contains_id
            assert _.edge_rules[0].target_type_id == method_type_id

    def test__pure_data_no_methods(self):                                                   # Verify no ontology operation methods
        ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        with Schema__Ontology(ontology_id  = ontology_id              ,
                              ontology_ref = Ontology_Ref('test')     ) as _:
            # These methods should NOT exist on the schema (moved to Utils)
            assert not hasattr(_, 'valid_edge')          or not callable(getattr(_, 'valid_edge', None))
            assert not hasattr(_, 'get_inverse_verb')    or not callable(getattr(_, 'get_inverse_verb', None))
            assert not hasattr(_, 'all_valid_edges')     or not callable(getattr(_, 'all_valid_edges', None))
            assert not hasattr(_, 'node_type_ids')       or not callable(getattr(_, 'node_type_ids', None))
            assert not hasattr(_, 'verbs_for_node_type') or not callable(getattr(_, 'verbs_for_node_type', None))

    def test__json_serialization(self):                                                     # Test JSON round-trip
        ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        original    = Schema__Ontology(ontology_id  = ontology_id                       ,
                                       ontology_ref = Ontology_Ref('test_ontology')     ,
                                       description  = Safe_Str__Text('Test ontology')   ,
                                       taxonomy_id  = taxonomy_id                       )

        json_data = original.json()
        restored  = Schema__Ontology.from_json(json_data)

        assert str(restored.ontology_id)  == str(original.ontology_id)
        assert str(restored.ontology_ref) == str(original.ontology_ref)
        assert str(restored.description)  == str(original.description)
        assert str(restored.taxonomy_id)  == str(original.taxonomy_id)