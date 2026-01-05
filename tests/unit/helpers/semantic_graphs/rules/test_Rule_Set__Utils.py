# ═══════════════════════════════════════════════════════════════════════════════
# Test Rule_Set__Utils - Tests for rule set utility operations
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase
from osbot_utils.helpers.semantic_graphs.rule.Rule_Set__Utils                       import Rule_Set__Utils
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref           import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref            import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id             import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref            import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set              import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality     import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity    import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb  import Safe_Str__Ontology__Verb
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data     import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                         import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id


class test_Rule_Set__Utils(TestCase):                                               # Test rule set utilities

    @classmethod
    def setUpClass(cls):                                                            # Shared test objects (performance)
        cls.qa       = QA__Semantic_Graphs__Test_Data()
        cls.utils    = Rule_Set__Utils()
        cls.rule_set = cls.create_test_rule_set()                                   # Rich rule set for testing

    @classmethod
    def create_test_rule_set(cls) -> Schema__Rule_Set:                              # Build test rule set
        trans_inheritance = Schema__Rule__Transitivity(source_type = Node_Type_Ref('class')                  ,
                                                       verb        = Safe_Str__Ontology__Verb('inherits_from'),
                                                       target_type = Node_Type_Ref('class')                  )
        trans_containment = Schema__Rule__Transitivity(source_type = Node_Type_Ref('package')                ,
                                                       verb        = Safe_Str__Ontology__Verb('has')         ,
                                                       target_type = Node_Type_Ref('package')                )

        card_method_class = Schema__Rule__Cardinality(source_type = Node_Type_Ref('method')                  ,
                                                      verb        = Safe_Str__Ontology__Verb('in')           ,
                                                      target_type = Node_Type_Ref('class')                   ,
                                                      min_targets = 1                                        ,
                                                      max_targets = 1                                        ,
                                                      description = 'Method in one class'                    )
        card_function_module = Schema__Rule__Cardinality(source_type = Node_Type_Ref('function')             ,
                                                         verb        = Safe_Str__Ontology__Verb('defined_in'),
                                                         target_type = Node_Type_Ref('module')               ,
                                                         min_targets = 1                                     ,
                                                         max_targets = 1                                     ,
                                                         description = 'Function in one module'              )

        return Schema__Rule_Set(rule_set_id        = Rule_Set_Id(Obj_Id())                                   ,
                                rule_set_ref       = Rule_Set_Ref('python_rules')                            ,
                                ontology_ref       = Ontology_Ref('code_structure')                          ,
                                version            = '1.0.0'                                                 ,
                                description        = 'Python structural rules'                               ,
                                transitivity_rules = [trans_inheritance, trans_containment]                  ,
                                cardinality_rules  = [card_method_class, card_function_module]               )

    def test__create_test_rule_set(self):                                           # Verify test rule set structure
        with self.rule_set as _:
            assert type(_) == Schema__Rule_Set
            assert _.obj() == __(version            = '1.0.0'                                                ,
                                 rule_set_id        = __SKIP__                                               ,
                                 rule_set_ref       = 'python_rules'                                         ,
                                 ontology_ref       = 'code_structure'                                       ,
                                 description        = 'Python structural rules'                              ,
                                 transitivity_rules = [__(source_type = 'class'                              ,
                                                         verb        = 'inherits_from'                       ,
                                                         target_type = 'class'                               ),
                                                       __(source_type = 'package'                            ,
                                                         verb        = 'has'                                 ,
                                                         target_type = 'package'                             )],
                                 cardinality_rules  = [__(source_type  = 'method'                            ,
                                                         verb         = 'in'                                 ,
                                                         target_type  = 'class'                              ,
                                                         min_targets  = 1                                    ,
                                                         max_targets  = 1                                    ,
                                                         description  = 'Method in one class'                ),
                                                       __(source_type  = 'function'                          ,
                                                         verb         = 'defined_in'                         ,
                                                         target_type  = 'module'                             ,
                                                         min_targets  = 1                                    ,
                                                         max_targets  = 1                                    ,
                                                         description  = 'Function in one module'             )])

    def test__init__(self):                                                         # Test initialization
        with Rule_Set__Utils() as _:
            assert type(_) is Rule_Set__Utils

    # ═══════════════════════════════════════════════════════════════════════════
    # Transitivity Checks
    # ═══════════════════════════════════════════════════════════════════════════

    def test__is_transitive__returns_true_for_transitive(self):                     # Test transitive check
        assert self.utils.is_transitive(self.rule_set, 'class', 'inherits_from', 'class')   is True
        assert self.utils.is_transitive(self.rule_set, 'package', 'has', 'package')         is True

    def test__is_transitive__returns_false_for_non_transitive(self):                # Test non-transitive check
        assert self.utils.is_transitive(self.rule_set, 'module', 'defines', 'class')  is False
        assert self.utils.is_transitive(self.rule_set, 'method', 'calls', 'method')   is False
        assert self.utils.is_transitive(self.rule_set, 'invalid', 'verb', 'invalid')  is False

    def test__is_transitive__partial_match_is_false(self):                          # Test partial matches don't count
        # Source matches but verb doesn't
        assert self.utils.is_transitive(self.rule_set, 'class', 'has', 'class')       is False
        # Verb matches but source doesn't
        assert self.utils.is_transitive(self.rule_set, 'module', 'inherits_from', 'class') is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Cardinality Lookup
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_cardinality__returns_matching_rule(self):                         # Test cardinality lookup
        method_rule = self.utils.get_cardinality_rule(self.rule_set, 'method', 'in', 'class')

        assert method_rule is not None
        assert int(method_rule.min_targets) == 1
        assert int(method_rule.max_targets) == 1

        function_rule = self.utils.get_cardinality_rule(self.rule_set, 'function', 'defined_in', 'module')

        assert function_rule is not None
        assert int(function_rule.min_targets) == 1

    def test__get_cardinality__returns_none_for_no_match(self):                     # Test missing cardinality
        assert self.utils.get_cardinality_rule(self.rule_set, 'class', 'has', 'method')    is None
        assert self.utils.get_cardinality_rule(self.rule_set, 'invalid', 'verb', 'type')   is None
        assert self.utils.get_cardinality_rule(self.rule_set, 'method', 'wrong', 'class')  is None

    def test__get_cardinality__all_fields_must_match(self):                         # Test all three fields must match
        # Only source_type matches
        assert self.utils.get_cardinality_rule(self.rule_set, 'method', 'wrong', 'wrong')  is None
        # Only verb matches
        assert self.utils.get_cardinality_rule(self.rule_set, 'wrong', 'in', 'wrong')      is None
        # Only target_type matches
        assert self.utils.get_cardinality_rule(self.rule_set, 'wrong', 'wrong', 'class')   is None

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with QA Test Data
    # ═══════════════════════════════════════════════════════════════════════════

    def test__qa_rule_set__transitivity(self):                                      # Test QA rule set transitivity
        rule_set = self.qa.create_rule_set__code_structure()

        # QA rule set has transitivity: method → in → module (via class)
        # Check for the transitivity rule that exists
        assert len(rule_set.transitivity_rules) >= 1

    def test__qa_rule_set__cardinality(self):                                       # Test QA rule set cardinality
        rule_set = self.qa.create_rule_set__code_structure()

        # QA rule set has cardinality: method must be in exactly 1 class
        assert len(rule_set.cardinality_rules) >= 1

        # Find the method → in → class rule
        method_rule = self.utils.get_cardinality_rule(rule_set, 'method', 'in', 'class')
        assert method_rule is not None
        assert int(method_rule.min_targets) == 1
        assert int(method_rule.max_targets) == 1

    def test__qa_rule_set__empty_has_no_rules(self):                                # Test empty QA rule set
        rule_set = self.qa.create_rule_set__empty()

        assert self.utils.is_transitive(rule_set, 'any', 'verb', 'any')     is False
        assert self.utils.get_cardinality_rule(rule_set, 'any', 'verb', 'any')   is None

    def test__qa_rule_set__ontology_ref_matches(self):                              # Test ontology ref is set correctly
        rule_set = self.qa.create_rule_set__code_structure()

        assert str(rule_set.ontology_ref) == 'code_structure'