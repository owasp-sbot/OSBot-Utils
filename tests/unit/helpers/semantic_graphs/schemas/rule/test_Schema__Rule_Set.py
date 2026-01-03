from unittest                                                                       import TestCase
from osbot_utils.helpers.semantic_graphs.rules.Rule__Engine                         import Rule__Engine
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id            import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id             import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id             import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set              import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality     import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity    import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb  import Safe_Str__Ontology__Verb


class test_Schema__Rule_Set(TestCase):                                               # Test rule set schema

    @classmethod
    def setUpClass(cls):                                                             # Create test rule set once
        cls.rule_set = cls.create_test_rule_set()

    @classmethod
    def create_test_rule_set(cls) -> Schema__Rule_Set:                               # Build test rule set
        trans_inheritance = Schema__Rule__Transitivity(
            source_type = Node_Type_Id('class')                                      ,
            verb        = Safe_Str__Ontology__Verb('inherits_from')                  ,
            target_type = Node_Type_Id('class')                                      ,
        )
        trans_containment = Schema__Rule__Transitivity(
            source_type = Node_Type_Id('package')                                    ,
            verb        = Safe_Str__Ontology__Verb('has')                            ,
            target_type = Node_Type_Id('package')                                    ,
        )

        card_method_class = Schema__Rule__Cardinality(
            source_type = Node_Type_Id('method')                                     ,
            verb        = Safe_Str__Ontology__Verb('in')                             ,
            target_type = Node_Type_Id('class')                                      ,
            min_targets = 1                                                          ,
            max_targets = 1                                                          ,
            description = 'Method belongs to exactly one class'                      ,
        )
        card_function_module = Schema__Rule__Cardinality(
            source_type = Node_Type_Id('function')                                   ,
            verb        = Safe_Str__Ontology__Verb('defined_in')                     ,
            target_type = Node_Type_Id('module')                                     ,
            min_targets = 1                                                          ,
            max_targets = 1                                                          ,
            description = 'Function defined in exactly one module'                   ,
        )

        return Schema__Rule_Set(
            rule_set_id        = Rule_Set_Id('python_rules')                          ,
            ontology_ref       = Ontology_Id('code_structure')                        ,
            version            = '1.0.0'                                             ,
            description        = 'Python-specific structural rules'                  ,
            transitivity_rules = [trans_inheritance, trans_containment]              ,
            cardinality_rules  = [card_method_class, card_function_module]           ,
        )

    def test__init__(self):                                                          # Test basic initialization
        with Schema__Rule_Set(rule_set_id=Rule_Set_Id('empty')) as _:
            assert type(_.rule_set_id)  is Rule_Set_Id
            assert str(_.rule_set_id)   == 'empty'
            assert str(_.version)       == '1.0.0'
            assert _.transitivity_rules == []
            assert _.cardinality_rules  == []

    def test__rule_set_structure(self):                                              # Test full rule set structure
        with self.rule_set as _:
            assert str(_.rule_set_id)        == 'python_rules'
            assert str(_.ontology_ref)       == 'code_structure'
            assert len(_.transitivity_rules) == 2
            assert len(_.cardinality_rules)  == 2

    def test__is_transitive__returns_true_for_transitive(self):                      # Test transitive check
        with self.rule_set as _:
            assert _.is_transitive('class', 'inherits_from', 'class')   is True
            assert _.is_transitive('package', 'has', 'package')         is True

    def test__is_transitive__returns_false_for_non_transitive(self):                 # Test non-transitive check
        with self.rule_set as _:
            assert _.is_transitive('module', 'defines', 'class')        is False
            assert _.is_transitive('method', 'calls', 'method')         is False
            assert _.is_transitive('invalid', 'verb', 'invalid')        is False

    def test__get_cardinality__returns_matching_rule(self):                          # Test cardinality lookup
        with self.rule_set as _:
            method_rule = _.get_cardinality('method', 'in', 'class')
            assert method_rule is not None
            assert int(method_rule.min_targets) == 1
            assert int(method_rule.max_targets) == 1

            function_rule = _.get_cardinality('function', 'defined_in', 'module')
            assert function_rule is not None
            assert int(function_rule.min_targets) == 1

    def test__get_cardinality__returns_none_for_no_match(self):                      # Test missing cardinality
        with self.rule_set as _:
            assert _.get_cardinality('class', 'has', 'method') is None
            assert _.get_cardinality('invalid', 'verb', 'type') is None

