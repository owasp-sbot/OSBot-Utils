# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Rule_Set - Tests for rule set schema (pure data)
# Note: Rule set operations have been moved to Rule_Set__Utils
#
# Updated for Brief 3.8:
#   - ontology_ref → ontology_id (Ontology_Id)
#   - Added required_node_properties (List__Rules__Required_Node_Property)
#   - Added required_edge_properties (List__Rules__Required_Edge_Property)
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                   import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Cardinality            import List__Rules__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Required_Edge_Property import List__Rules__Required_Edge_Property
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Required_Node_Property import List__Rules__Required_Node_Property
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity           import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                        import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                         import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                        import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id                    import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                         import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref                        import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                          import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Edge_Property      import Schema__Rule__Required_Edge_Property
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Node_Property      import Schema__Rule__Required_Node_Property
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                    import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version                 import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe


class test_Schema__Rule_Set(TestCase):                                                 # Test rule set schema

    def test__init__(self):                                                            # Test initialization
        rule_set_id = Rule_Set_Id(Obj_Id.from_seed('test:rules'))
        ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        with Schema__Rule_Set(rule_set_id  = rule_set_id                  ,
                              rule_set_ref = Rule_Set_Ref('test')         ,
                              ontology_id  = ontology_id                  ) as _:
            assert type(_)             is Schema__Rule_Set
            assert isinstance(_, Type_Safe)
            assert _.rule_set_id       == rule_set_id
            assert str(_.rule_set_ref) == 'test'
            assert _.ontology_id       == ontology_id                                  # Brief 3.8

    def test__init__types(self):                                                       # Test attribute types
        rule_set_id = Rule_Set_Id(Obj_Id.from_seed('test:rules'))
        ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        with Schema__Rule_Set(rule_set_id  = rule_set_id                  ,
                              rule_set_ref = Rule_Set_Ref('test')         ,
                              ontology_id  = ontology_id                  ) as _:
            assert type(_.rule_set_id)              is Rule_Set_Id
            assert type(_.rule_set_ref)             is Rule_Set_Ref
            assert type(_.ontology_id)              is Ontology_Id                     # Brief 3.8
            assert type(_.version)                  is Safe_Str__Version
            assert type(_.transitivity_rules)       is List__Rules__Transitivity
            assert type(_.cardinality_rules)        is List__Rules__Cardinality
            assert type(_.required_node_properties) is List__Rules__Required_Node_Property  # Brief 3.8
            assert type(_.required_edge_properties) is List__Rules__Required_Edge_Property  # Brief 3.8

    def test__init__default_values(self):                                              # Test default values
        rule_set_id = Rule_Set_Id(Obj_Id.from_seed('test:rules'))
        ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        with Schema__Rule_Set(rule_set_id  = rule_set_id                  ,
                              rule_set_ref = Rule_Set_Ref('test')         ,
                              ontology_id  = ontology_id                  ) as _:
            assert str(_.version)                  == '1.0.0'
            assert len(_.transitivity_rules)       == 0
            assert len(_.cardinality_rules)        == 0
            assert len(_.required_node_properties) == 0                                # Brief 3.8
            assert len(_.required_edge_properties) == 0                                # Brief 3.8

    def test__init__with_property_rules(self):                                         # Brief 3.8: property rules
        rule_set_id    = Rule_Set_Id(Obj_Id.from_seed('test:rules'))
        ontology_id    = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        method_id      = Node_Type_Id(Obj_Id.from_seed('test:nt:method'))
        calls_id       = Predicate_Id(Obj_Id.from_seed('test:pred:calls'))
        line_number_id = Property_Name_Id(Obj_Id.from_seed('test:pn:line_number'))
        call_count_id  = Property_Name_Id(Obj_Id.from_seed('test:pn:call_count'))

        node_prop_rule = Schema__Rule__Required_Node_Property(node_type_id     = method_id      ,
                                                              property_name_id = line_number_id ,
                                                              required         = True           )

        edge_prop_rule = Schema__Rule__Required_Edge_Property(predicate_id     = calls_id      ,
                                                              property_name_id = call_count_id ,
                                                              required         = False         )

        required_node_properties = List__Rules__Required_Node_Property()
        required_node_properties.append(node_prop_rule)

        required_edge_properties = List__Rules__Required_Edge_Property()
        required_edge_properties.append(edge_prop_rule)

        with Schema__Rule_Set(rule_set_id              = rule_set_id              ,
                              rule_set_ref             = Rule_Set_Ref('test')     ,
                              ontology_id              = ontology_id              ,
                              required_node_properties = required_node_properties ,
                              required_edge_properties = required_edge_properties ) as _:
            assert len(_.required_node_properties) == 1
            assert len(_.required_edge_properties) == 1
            assert _.required_node_properties[0]   is node_prop_rule
            assert _.required_edge_properties[0]   is edge_prop_rule
            assert _.required_node_properties[0].required is True
            assert _.required_edge_properties[0].required is False

    def test__pure_data_no_methods(self):                                              # Verify no rule set operation methods
        rule_set_id = Rule_Set_Id(Obj_Id.from_seed('test:rules'))
        ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        with Schema__Rule_Set(rule_set_id  = rule_set_id                  ,
                              rule_set_ref = Rule_Set_Ref('test')         ,
                              ontology_id  = ontology_id                  ) as _:
            # These methods should NOT exist on the schema (moved to Utils)
            assert not hasattr(_, 'is_transitive')            or not callable(getattr(_, 'is_transitive', None))
            assert not hasattr(_, 'get_cardinality')          or not callable(getattr(_, 'get_cardinality', None))
            assert not hasattr(_, 'get_required_node_property') or not callable(getattr(_, 'get_required_node_property', None))

    def test__json_serialization(self):                                                # Test JSON round-trip
        rule_set_id = Rule_Set_Id(Obj_Id.from_seed('test:rules:serial'))
        ontology_id = Ontology_Id(Obj_Id.from_seed('test:ontology'))
        original    = Schema__Rule_Set(rule_set_id  = rule_set_id                         ,
                                       rule_set_ref = Rule_Set_Ref('test_rules')          ,
                                       ontology_id  = ontology_id                         ,
                                       version      = Safe_Str__Version('2.0.0')          )

        json_data = original.json()
        restored  = Schema__Rule_Set.from_json(json_data)

        assert str(restored.rule_set_id)  == str(original.rule_set_id)
        assert str(restored.rule_set_ref) == str(original.rule_set_ref)
        assert str(restored.ontology_id)  == str(original.ontology_id)                 # Brief 3.8
        assert str(restored.version)      == str(original.version)