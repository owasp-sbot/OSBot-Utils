# ═══════════════════════════════════════════════════════════════════════════════
# Test Rule__Engine - Tests for rule engine with typed collections
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.rule.Rule__Engine                              import Rule__Engine
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Rule_Sets__By_Id      import Dict__Rule_Sets__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Rule_Sets__By_Ref     import Dict__Rule_Sets__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rule_Set_Ids          import List__Rule_Set_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rule_Set_Refs         import List__Rule_Set_Refs
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Cardinality    import List__Rules__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity   import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                 import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref                import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                  import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data         import QA__Semantic_Graphs__Test_Data
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text            import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version         import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed   import Safe_Str__Id__Seed


class test_Rule__Engine(TestCase):                                                      # Test rule engine

    @classmethod
    def setUpClass(cls):                                                                # Shared test objects (performance)
        cls.qa = QA__Semantic_Graphs__Test_Data()

    def setUp(self):                                                                    # Fresh engine for each test
        self.engine = Rule__Engine()

    def test__init__(self):                                                             # Test basic creation
        with Rule__Engine() as _:
            assert type(_.rule_sets_by_ref) is Dict__Rule_Sets__By_Ref
            assert type(_.rule_sets_by_id)  is Dict__Rule_Sets__By_Id
            assert len(_.rule_sets_by_ref)  == 0
            assert len(_.rule_sets_by_id)   == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods - Random ID
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_with__random_id__simple(self):                                     # Test creating with random ID
        with self.engine as _:
            rule_set = _.create_with__random_id(rule_set_ref = Rule_Set_Ref('simple'),
                                                ontology_ref = Ontology_Ref('test')  )

            assert type(rule_set)             is Schema__Rule_Set
            assert str(rule_set.rule_set_ref) == 'simple'
            assert rule_set.rule_set_id       is not None

    def test__create_with__random_id__full(self):                                       # Test with all parameters
        with self.engine as _:
            rule_set = _.create_with__random_id(rule_set_ref = Rule_Set_Ref('full')                ,
                                                ontology_ref = Ontology_Ref('code_structure')      ,
                                                description  = Safe_Str__Text('Full test rule set'),
                                                version      = Safe_Str__Version('2.0.0')          )

            assert str(rule_set.rule_set_ref) == 'full'
            assert str(rule_set.ontology_ref) == 'code_structure'
            assert str(rule_set.description)  == 'Full test rule set'
            assert str(rule_set.version)      == '2.0.0'

    def test__create_with__random_id__with_rules(self):                                 # Test with rules
        transitivity_rules = List__Rules__Transitivity()
        cardinality_rules  = List__Rules__Cardinality()

        with self.engine as _:
            rule_set = _.create_with__random_id(rule_set_ref       = Rule_Set_Ref('with_rules'),
                                                ontology_ref       = Ontology_Ref('test')       ,
                                                transitivity_rules = transitivity_rules         ,
                                                cardinality_rules  = cardinality_rules          )

            assert type(rule_set.transitivity_rules) is List__Rules__Transitivity
            assert type(rule_set.cardinality_rules)  is List__Rules__Cardinality

    def test__create_with__random_id__is_registered(self):                              # Test auto-registration
        with self.engine as _:
            rule_set = _.create_with__random_id(rule_set_ref = Rule_Set_Ref('auto_reg'),
                                                ontology_ref = Ontology_Ref('test')    )

            assert _.get_by_ref(Rule_Set_Ref('auto_reg')) is rule_set
            assert _.get_by_id(rule_set.rule_set_id)      is rule_set

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods - Deterministic ID
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_with__deterministic_id(self):                                      # Test creating with deterministic ID
        seed = Safe_Str__Id__Seed('test:rule_set:det')

        with self.engine as _:
            rule_set = _.create_with__deterministic_id(rule_set_ref = Rule_Set_Ref('deterministic'),
                                                       ontology_ref = Ontology_Ref('test')          ,
                                                       seed         = seed                          )

            assert type(rule_set)             is Schema__Rule_Set
            assert str(rule_set.rule_set_ref) == 'deterministic'
            assert rule_set.rule_set_id_source is not None
            assert str(rule_set.rule_set_id_source.seed) == 'test:rule_set:det'

    def test__create_with__deterministic_id__same_seed_same_id(self):                   # Test deterministic reproducibility
        seed = Safe_Str__Id__Seed('test:rule_set:reproducible')

        with Rule__Engine() as engine_1:
            rule_set_1 = engine_1.create_with__deterministic_id(rule_set_ref = Rule_Set_Ref('rep'),
                                                                 ontology_ref = Ontology_Ref('test'),
                                                                 seed         = seed                )

        with Rule__Engine() as engine_2:
            rule_set_2 = engine_2.create_with__deterministic_id(rule_set_ref = Rule_Set_Ref('rep'),
                                                                 ontology_ref = Ontology_Ref('test'),
                                                                 seed         = seed                )

        assert str(rule_set_1.rule_set_id) == str(rule_set_2.rule_set_id)               # Same seed → same ID

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods - Explicit ID
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_with__explicit_id(self):                                           # Test creating with explicit ID
        explicit_id = Rule_Set_Id(Obj_Id())

        with self.engine as _:
            rule_set = _.create_with__explicit_id(rule_set_ref = Rule_Set_Ref('explicit'),
                                                  ontology_ref = Ontology_Ref('test')     ,
                                                  rule_set_id  = explicit_id              )

            assert rule_set.rule_set_id      == explicit_id
            assert _.get_by_id(explicit_id)  is rule_set

    # ═══════════════════════════════════════════════════════════════════════════
    # Registration and Lookup
    # ═══════════════════════════════════════════════════════════════════════════

    def test__register(self):                                                           # Test manual registration
        rule_set = Schema__Rule_Set(rule_set_id  = Rule_Set_Id(Obj_Id())                ,
                                    rule_set_ref = Rule_Set_Ref('manual')               ,
                                    ontology_ref = Ontology_Ref('test')                 )

        with self.engine as _:
            result = _.register(rule_set)

            assert result is rule_set                                                   # Returns the rule_set
            assert _.get_by_ref(Rule_Set_Ref('manual')) is rule_set
            assert _.get_by_id(rule_set.rule_set_id)    is rule_set

    def test__get_by_ref__returns_none_for_unknown(self):                               # Test missing ref lookup
        with self.engine as _:
            assert _.get_by_ref(Rule_Set_Ref('unknown'))     is None
            assert _.get_by_ref(Rule_Set_Ref('nonexistent')) is None

    def test__get_by_id__returns_none_for_unknown(self):                                # Test missing ID lookup
        with self.engine as _:
            assert _.get_by_id(Rule_Set_Id(Obj_Id())) is None

    def test__has_ref(self):                                                            # Test ref existence check
        with self.engine as _:
            _.create_with__random_id(rule_set_ref = Rule_Set_Ref('exists'),
                                     ontology_ref = Ontology_Ref('test')  )

            assert _.has_ref(Rule_Set_Ref('exists'))     is True
            assert _.has_ref(Rule_Set_Ref('not_exists')) is False

    def test__has_id(self):                                                             # Test ID existence check
        with self.engine as _:
            rule_set = _.create_with__random_id(rule_set_ref = Rule_Set_Ref('has_id'),
                                                ontology_ref = Ontology_Ref('test')  )

            assert _.has_id(rule_set.rule_set_id)      is True
            assert _.has_id(Rule_Set_Id(Obj_Id()))     is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Listing Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__all_refs(self):                                                           # Test listing all refs
        with self.engine as _:
            refs = _.all_refs()
            assert type(refs) is List__Rule_Set_Refs
            assert len(refs)  == 0                                                      # Initially empty

            _.create_with__random_id(Rule_Set_Ref('rs1'), Ontology_Ref('o1'))
            _.create_with__random_id(Rule_Set_Ref('rs2'), Ontology_Ref('o2'))
            _.create_with__random_id(Rule_Set_Ref('rs3'), Ontology_Ref('o3'))

            refs = _.all_refs()
            assert len(refs) == 3

            ref_strs = [str(r) for r in refs]
            assert 'rs1' in ref_strs
            assert 'rs2' in ref_strs
            assert 'rs3' in ref_strs

    def test__all_ids(self):                                                            # Test listing all IDs
        with self.engine as _:
            ids = _.all_ids()
            assert type(ids) is List__Rule_Set_Ids
            assert len(ids)  == 0                                                       # Initially empty

            _.create_with__random_id(Rule_Set_Ref('rs1'), Ontology_Ref('o1'))
            _.create_with__random_id(Rule_Set_Ref('rs2'), Ontology_Ref('o2'))

            ids = _.all_ids()
            assert len(ids) == 2

    # ═══════════════════════════════════════════════════════════════════════════
    # Overwrite Behavior
    # ═══════════════════════════════════════════════════════════════════════════

    def test__overwrite_existing_ref(self):                                             # Test same ref overwrites
        with self.engine as _:
            v1 = _.create_with__random_id(rule_set_ref = Rule_Set_Ref('versioned'),
                                          ontology_ref = Ontology_Ref('test')     ,
                                          version      = Safe_Str__Version('1.0.0'))

            assert str(_.get_by_ref(Rule_Set_Ref('versioned')).version) == '1.0.0'

            v2 = _.create_with__random_id(rule_set_ref = Rule_Set_Ref('versioned'),
                                          ontology_ref = Ontology_Ref('test')     ,
                                          version      = Safe_Str__Version('2.0.0'))

            assert str(_.get_by_ref(Rule_Set_Ref('versioned')).version) == '2.0.0'
            assert len(_.all_refs()) == 1                                               # Still just one ref entry

    # ═══════════════════════════════════════════════════════════════════════════
    # Dual Lookup Consistency
    # ═══════════════════════════════════════════════════════════════════════════

    def test__dual_lookup_consistency(self):                                            # Test by_ref and by_id same object
        with self.engine as _:
            rule_set = _.create_with__random_id(rule_set_ref = Rule_Set_Ref('dual'),
                                                ontology_ref = Ontology_Ref('test'))

            by_ref = _.get_by_ref(Rule_Set_Ref('dual'))
            by_id  = _.get_by_id(rule_set.rule_set_id)

            assert by_ref is by_id                                                      # Same object
            assert by_ref is rule_set

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with QA Test Data
    # ═══════════════════════════════════════════════════════════════════════════

    def test__register_qa_rule_set(self):                                               # Test registering QA-created rule set
        rule_set = self.qa.create_rule_set__code_structure()

        with self.engine as _:
            _.register(rule_set)

            assert _.get_by_ref(Rule_Set_Ref('code_structure_rules')) is rule_set
            assert _.has_ref(Rule_Set_Ref('code_structure_rules'))    is True

            refs = _.all_refs()
            ref_strs = [str(r) for r in refs]
            assert 'code_structure_rules' in ref_strs

    def test__qa_rule_set__has_rules(self):                                             # Test QA rule set has expected rules
        rule_set = self.qa.create_rule_set__code_structure()

        assert len(rule_set.transitivity_rules) >= 1                                    # Has transitivity rules
        assert len(rule_set.cardinality_rules)  >= 1                                    # Has cardinality rules

    def test__qa_rule_set__empty(self):                                                 # Test empty QA rule set
        rule_set = self.qa.create_rule_set__empty()

        with self.engine as _:
            _.register(rule_set)

            retrieved = _.get_by_ref(Rule_Set_Ref('empty_rules'))
            assert len(retrieved.transitivity_rules) == 0
            assert len(retrieved.cardinality_rules)  == 0

    def test__qa_rule_set__dual_lookup(self):                                           # Test QA rule_set dual lookup
        rule_set = self.qa.create_rule_set__code_structure()

        with self.engine as _:
            _.register(rule_set)

            by_ref = _.get_by_ref(Rule_Set_Ref('code_structure_rules'))
            by_id  = _.get_by_id(rule_set.rule_set_id)

            assert by_ref is by_id
            assert by_ref is rule_set