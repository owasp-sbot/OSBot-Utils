# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Rule_Set - Tests for rule set schema (pure data)
# Note: Rule set operations have been moved to Rule_Set__Utils
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Cardinality   import List__Rules__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity  import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id            import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id             import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id             import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set              import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality     import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity    import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb  import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version     import Safe_Str__Version
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class test_Schema__Rule_Set(TestCase):                                               # Test rule set schema

    def test__init__(self):                                                          # Test initialization
        with Schema__Rule_Set(rule_set_id  = Rule_Set_Id('test'),
                              ontology_ref = Ontology_Id('ontology')) as _:
            assert type(_)            is Schema__Rule_Set
            assert isinstance(_, Type_Safe)
            assert str(_.rule_set_id) == 'test'
            assert str(_.version)     == '1.0.0'

    def test__init__types(self):                                                     # Test attribute types
        with Schema__Rule_Set(rule_set_id  = Rule_Set_Id('test'),
                              ontology_ref = Ontology_Id('ontology')) as _:
            assert type(_.rule_set_id)        is Rule_Set_Id
            assert type(_.ontology_ref)       is Ontology_Id
            assert type(_.version)            is Safe_Str__Version
            assert type(_.description)        is Safe_Str__Text
            assert type(_.transitivity_rules) is List__Rules__Transitivity
            assert type(_.cardinality_rules)  is List__Rules__Cardinality

    def test__init__default_values(self):                                            # Test default values
        with Schema__Rule_Set(rule_set_id  = Rule_Set_Id('test'),
                              ontology_ref = Ontology_Id('ontology')) as _:
            assert str(_.version)            == '1.0.0'
            assert str(_.description)        == ''
            assert len(_.transitivity_rules) == 0
            assert len(_.cardinality_rules)  == 0

    def test__init__with_rules(self):                                                # Test with rules
        trans_rule = Schema__Rule__Transitivity(source_type = Node_Type_Id('class'),
                                                verb        = Safe_Str__Ontology__Verb('inherits_from'),
                                                target_type = Node_Type_Id('class'))
        card_rule = Schema__Rule__Cardinality(source_type = Node_Type_Id('method'),
                                              verb        = Safe_Str__Ontology__Verb('in'),
                                              target_type = Node_Type_Id('class'),
                                              min_targets = 1, max_targets = 1, description = '')

        with Schema__Rule_Set(rule_set_id        = Rule_Set_Id('test'),
                              ontology_ref       = Ontology_Id('ontology'),
                              transitivity_rules = [trans_rule]          ,
                              cardinality_rules  = [card_rule]           ) as _:
            assert len(_.transitivity_rules) == 1
            assert len(_.cardinality_rules)  == 1
            assert _.transitivity_rules[0]   is trans_rule
            assert _.cardinality_rules[0]    is card_rule

    def test__pure_data_no_methods(self):                                            # Verify no rule set operation methods
        with Schema__Rule_Set(rule_set_id  = Rule_Set_Id('test'),
                              ontology_ref = Ontology_Id('ontology')) as _:
            # These methods should NOT exist on the schema (moved to Utils)
            assert not hasattr(_, 'is_transitive')   or not callable(getattr(_, 'is_transitive', None))
            assert not hasattr(_, 'get_cardinality') or not callable(getattr(_, 'get_cardinality', None))

    def test__json_serialization(self):                                              # Test JSON round-trip
        original = Schema__Rule_Set(rule_set_id  = Rule_Set_Id('test_rules'),
                                    ontology_ref = Ontology_Id('ontology') ,
                                    version      = '2.0.0'                 ,
                                    description  = 'Test rule set'         )

        json_data = original.json()
        restored  = Schema__Rule_Set.from_json(json_data)

        assert str(restored.rule_set_id)  == str(original.rule_set_id)
        assert str(restored.ontology_ref) == str(original.ontology_ref)
        assert str(restored.version)      == str(original.version)
        assert str(restored.description)  == str(original.description)