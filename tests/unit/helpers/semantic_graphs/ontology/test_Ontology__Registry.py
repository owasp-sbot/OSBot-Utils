# ═══════════════════════════════════════════════════════════════════════════════
# Test Ontology__Registry - Tests for ontology registry with typed collections
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
#
# Updated for Brief 3.7:
#   - taxonomy_ref → taxonomy_id
#   - Uses predicate-based edge validation instead of embedded relationships
#   - Removed version parameter from factory methods
# ═══════════════════════════════════════════════════════════════════════════════

import re
import pytest
from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Registry                    import Ontology__Registry
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Utils                       import Ontology__Utils
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Ontologies__By_Id     import Dict__Ontologies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Ontologies__By_Ref    import Dict__Ontologies__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Ontology_Ids          import List__Ontology_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Ontology_Refs         import List__Ontology_Refs
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref               import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                 import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref               import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                 import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology              import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data         import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                             import __
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text            import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed   import Safe_Str__Id__Seed
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                          import type_safe


class test_Ontology__Registry(TestCase):                                                # Test ontology registry

    @classmethod
    def setUpClass(cls):                                                                # Shared test objects (performance)
        cls.test_data      = QA__Semantic_Graphs__Test_Data()
        cls.ontology_utils = Ontology__Utils()

    def setUp(self):                                                                    # Fresh registry for each test
        self.registry = Ontology__Registry()

    def test__init__(self):                                                             # Test basic creation
        with Ontology__Registry() as _:
            assert type(_.ontologies_by_ref) is Dict__Ontologies__By_Ref
            assert type(_.ontologies_by_id)  is Dict__Ontologies__By_Id
            assert len(_.ontologies_by_ref)  == 0
            assert len(_.ontologies_by_id)   == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods - Random ID
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_with__random_id__simple(self):                                     # Test creating with random ID
        with self.registry as _:
            ontology = _.create_with__random_id(ontology_ref = Ontology_Ref('simple'))

            assert type(ontology)             is Schema__Ontology
            assert str(ontology.ontology_ref) == 'simple'
            assert ontology.ontology_id       is not None

    def test__create_with__random_id__full(self):                                       # Test with all parameters
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        with self.registry as _:
            ontology = _.create_with__random_id(ontology_ref = Ontology_Ref('full')                ,
                                                taxonomy_id  = taxonomy_id                         ,
                                                description  = Safe_Str__Text('Full test ontology'))

            assert str(ontology.ontology_ref) == 'full'
            assert ontology.taxonomy_id       == taxonomy_id
            assert str(ontology.description)  == 'Full test ontology'

    def test__create_with__random_id__is_registered(self):                              # Test auto-registration
        with self.registry as _:
            ontology = _.create_with__random_id(ontology_ref = Ontology_Ref('auto_reg'))

            assert _.get_by_ref(Ontology_Ref('auto_reg')) is ontology
            assert _.get_by_id(ontology.ontology_id)      is ontology

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods - Deterministic ID
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_with__deterministic_id(self):                                      # Test creating with deterministic ID
        seed = Safe_Str__Id__Seed('test:ontology:det')

        with self.registry as _:
            ontology = _.create_with__deterministic_id(ontology_ref = Ontology_Ref('deterministic'),
                                                       seed         = seed                          )

            assert type(ontology)             is Schema__Ontology
            assert str(ontology.ontology_ref) == 'deterministic'
            assert ontology.ontology_id_source is not None
            assert str(ontology.ontology_id_source.seed) == 'test:ontology:det'

    def test__create_with__deterministic_id__same_seed_same_id(self):                   # Test deterministic reproducibility
        seed = Safe_Str__Id__Seed('test:ontology:reproducible')

        with Ontology__Registry() as registry_1:
            ontology_1 = registry_1.create_with__deterministic_id(ontology_ref = Ontology_Ref('rep'),
                                                                   seed         = seed               )

        with Ontology__Registry() as registry_2:
            ontology_2 = registry_2.create_with__deterministic_id(ontology_ref = Ontology_Ref('rep'),
                                                                   seed         = seed               )

        assert str(ontology_1.ontology_id) == str(ontology_2.ontology_id)               # Same seed → same ID

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods - Explicit ID
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_with__explicit_id(self):                                           # Test creating with explicit ID
        explicit_id = Ontology_Id(Obj_Id())

        with self.registry as _:
            ontology = _.create_with__explicit_id(ontology_ref = Ontology_Ref('explicit'),
                                                  ontology_id  = explicit_id              )

            assert ontology.ontology_id       == explicit_id
            assert _.get_by_id(explicit_id)   is ontology

    # ═══════════════════════════════════════════════════════════════════════════
    # Registration and Lookup
    # ═══════════════════════════════════════════════════════════════════════════

    def test__register(self):                                                           # Test manual registration
        ontology = Schema__Ontology(ontology_id  = Ontology_Id(Obj_Id())  ,
                                    ontology_ref = Ontology_Ref('manual') )

        with self.registry as _:
            result = _.register(ontology)

            assert result is ontology                                                   # Returns the ontology
            assert _.get_by_ref(Ontology_Ref('manual')) is ontology
            assert _.get_by_id(ontology.ontology_id)    is ontology

    def test__get_by_ref__returns_none_for_unknown(self):                               # Test missing ref lookup
        with self.registry as _:
            assert _.get_by_ref(Ontology_Ref('unknown'))     is None
            assert _.get_by_ref(Ontology_Ref('nonexistent')) is None

    def test__get_by_id__returns_none_for_unknown(self):                                # Test missing ID lookup
        with self.registry as _:
            assert _.get_by_id(Ontology_Id(Obj_Id())) is None

    def test__has_ref(self):                                                            # Test ref existence check
        with self.registry as _:
            _.create_with__random_id(ontology_ref = Ontology_Ref('exists'))

            assert _.has_ref(Ontology_Ref('exists'))     is True
            assert _.has_ref(Ontology_Ref('not_exists')) is False

    def test__has_id(self):                                                             # Test ID existence check
        with self.registry as _:
            ontology = _.create_with__random_id(ontology_ref = Ontology_Ref('has_id'))

            assert _.has_id(ontology.ontology_id)      is True
            assert _.has_id(Ontology_Id(Obj_Id()))     is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Listing Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__all_refs(self):                                                           # Test listing all refs
        with self.registry as _:
            refs = _.all_refs()
            assert type(refs) is List__Ontology_Refs
            assert len(refs)  == 0                                                      # Initially empty

            _.create_with__random_id(Ontology_Ref('ont1'))
            _.create_with__random_id(Ontology_Ref('ont2'))
            _.create_with__random_id(Ontology_Ref('ont3'))

            refs = _.all_refs()
            assert len(refs) == 3

            ref_strs = [str(r) for r in refs]
            assert 'ont1' in ref_strs
            assert 'ont2' in ref_strs
            assert 'ont3' in ref_strs

    def test__all_ids(self):                                                            # Test listing all IDs
        with self.registry as _:
            ids = _.all_ids()
            assert type(ids) is List__Ontology_Ids
            assert len(ids)  == 0                                                       # Initially empty

            _.create_with__random_id(Ontology_Ref('ont1'))
            _.create_with__random_id(Ontology_Ref('ont2'))

            ids = _.all_ids()
            assert len(ids) == 2

    # ═══════════════════════════════════════════════════════════════════════════
    # Overwrite Behavior
    # ═══════════════════════════════════════════════════════════════════════════

    def test__overwrite_existing_ref(self):                                             # Test same ref overwrites
        with self.registry as _:
            v1 = _.create_with__random_id(ontology_ref = Ontology_Ref('versioned'),
                                          description  = Safe_Str__Text('Version 1'))

            assert str(_.get_by_ref(Ontology_Ref('versioned')).description) == 'Version 1'

            v2 = _.create_with__random_id(ontology_ref = Ontology_Ref('versioned'),
                                          description  = Safe_Str__Text('Version 2'))

            assert str(_.get_by_ref(Ontology_Ref('versioned')).description) == 'Version 2'
            assert len(_.all_refs()) == 1                                               # Still just one ref entry

    # ═══════════════════════════════════════════════════════════════════════════
    # Dual Lookup Consistency
    # ═══════════════════════════════════════════════════════════════════════════

    def test__dual_lookup_consistency(self):                                            # Test by_ref and by_id same object
        with self.registry as _:
            ontology = _.create_with__random_id(ontology_ref = Ontology_Ref('dual'))

            by_ref = _.get_by_ref(Ontology_Ref('dual'))
            by_id  = _.get_by_id(ontology.ontology_id)

            assert by_ref is by_id                                                      # Same object
            assert by_ref is ontology

    # ═══════════════════════════════════════════════════════════════════════════
    # Type Safe Decorator Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__type_safe__check_optional_behaviour(self):                                # Test @type_safe optional handling
        @type_safe
        def an_method_1(value: str) -> str:
            return value

        @type_safe
        def an_method_2(value: str=None) -> str:
            return value

        @type_safe
        def an_method_3(value: str) -> str:
            return None

        assert an_method_1('abc') == 'abc'
        assert an_method_2('abc') == 'abc'
        assert an_method_3('abc') is None
        assert an_method_2(None)  is None

        error_message_1 = "Parameter 'value' is not optional but got None"
        with pytest.raises(ValueError, match=error_message_1):
            an_method_1(None)

        error_message_2 = "Parameter 'value' expected type <class 'str'>, but got <class 'int'>"
        with pytest.raises(ValueError, match=re.escape(error_message_2)):
            an_method_1(42)

        with pytest.raises(ValueError, match=re.escape(error_message_2)):
            an_method_3(42)

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with QA Test Data
    # ═══════════════════════════════════════════════════════════════════════════

    def test__register_qa_ontology(self):                                               # Test registering QA-created ontology
        ontology = self.test_data.create_ontology__code_structure()

        with self.registry as _:
            _.register(ontology)

            assert _.get_by_ref(Ontology_Ref('code_structure')) is ontology
            assert _.has_ref(Ontology_Ref('code_structure'))    is True

            refs = _.all_refs()
            ref_strs = [str(r) for r in refs]
            assert 'code_structure' in ref_strs

    def test__qa_ontology__validates_correctly(self):                                   # Test QA ontology with utils
        ontology = self.test_data.create_ontology__code_structure()

        with self.registry as _:
            _.register(ontology)
            retrieved = _.get_by_ref(Ontology_Ref('code_structure'))

            with self.ontology_utils as utils:                                          # Verify edge rules work
                # Use is_valid_edge_by_ref for ref-based validation
                assert utils.is_valid_edge_by_ref(retrieved, Node_Type_Ref('module'), Predicate_Ref('contains'), Node_Type_Ref('class'))    is True
                assert utils.is_valid_edge_by_ref(retrieved, Node_Type_Ref('class') , Predicate_Ref('contains'), Node_Type_Ref('method'))   is True
                assert utils.is_valid_edge_by_ref(retrieved, Node_Type_Ref('method'), Predicate_Ref('calls')   , Node_Type_Ref('function')) is True

                # Test inverse predicate lookup
                contains_pred = utils.get_predicate_by_ref(retrieved, Predicate_Ref('contains'))
                inverse_pred  = utils.get_inverse_predicate(retrieved, contains_pred.predicate_id)
                assert inverse_pred is not None
                assert inverse_pred.predicate_ref == Predicate_Ref('in')

    def test__qa_ontology__dual_lookup(self):                                           # Test QA ontology dual lookup
        ontology = self.test_data.create_ontology__code_structure()

        with self.registry as _:
            _.register(ontology)

            by_ref = _.get_by_ref(Ontology_Ref('code_structure'))
            by_id  = _.get_by_id(ontology.ontology_id)

            assert by_ref is by_id
            assert by_ref is ontology