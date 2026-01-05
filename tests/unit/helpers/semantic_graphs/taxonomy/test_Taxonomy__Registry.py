# ═══════════════════════════════════════════════════════════════════════════════
# Test Taxonomy__Registry - Tests for taxonomy registry with typed collections
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Ref    import Dict__Categories__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Taxonomies__By_Id     import Dict__Taxonomies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Taxonomies__By_Ref    import Dict__Taxonomies__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Taxonomy_Ids          import List__Taxonomy_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Taxonomy_Refs         import List__Taxonomy_Refs
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                 import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref                import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Registry                    import Taxonomy__Registry
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data         import QA__Semantic_Graphs__Test_Data
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text            import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version         import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed   import Safe_Str__Id__Seed


class test_Taxonomy__Registry(TestCase):                                                # Test taxonomy registry

    @classmethod
    def setUpClass(cls):                                                                # Shared test objects (performance)
        cls.qa = QA__Semantic_Graphs__Test_Data()

    def setUp(self):                                                                    # Fresh registry for each test
        self.registry = Taxonomy__Registry()

    def test__init__(self):                                                             # Test basic creation
        with Taxonomy__Registry() as _:
            assert type(_.taxonomies_by_ref) is Dict__Taxonomies__By_Ref
            assert type(_.taxonomies_by_id)  is Dict__Taxonomies__By_Id
            assert len(_.taxonomies_by_ref)  == 0
            assert len(_.taxonomies_by_id)   == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods - Random ID
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_with__random_id__simple(self):                                     # Test creating with random ID
        with self.registry as _:
            taxonomy = _.create_with__random_id(taxonomy_ref  = Taxonomy_Ref('simple'),
                                                root_category = Category_Ref('')      )

            assert type(taxonomy)             is Schema__Taxonomy
            assert str(taxonomy.taxonomy_ref) == 'simple'
            assert taxonomy.taxonomy_id       is not None

    def test__create_with__random_id__full(self):                                       # Test with all parameters
        with self.registry as _:
            taxonomy = _.create_with__random_id(taxonomy_ref  = Taxonomy_Ref('full')               ,
                                                root_category = Category_Ref('root')               ,
                                                description   = Safe_Str__Text('Full test taxonomy'),
                                                version       = Safe_Str__Version('2.0.0')         )

            assert str(taxonomy.taxonomy_ref)  == 'full'
            assert str(taxonomy.root_category) == 'root'
            assert str(taxonomy.description)   == 'Full test taxonomy'
            assert str(taxonomy.version)       == '2.0.0'

    def test__create_with__random_id__with_categories(self):                            # Test with categories
        categories = Dict__Categories__By_Ref()                                         # Would populate with actual categories

        with self.registry as _:
            taxonomy = _.create_with__random_id(taxonomy_ref  = Taxonomy_Ref('with_cats'),
                                                root_category = Category_Ref('root')     ,
                                                categories    = categories               )

            assert type(taxonomy.categories) is Dict__Categories__By_Ref

    def test__create_with__random_id__is_registered(self):                              # Test auto-registration
        with self.registry as _:
            taxonomy = _.create_with__random_id(taxonomy_ref  = Taxonomy_Ref('auto_reg'),
                                                root_category = Category_Ref('')        )

            assert _.get_by_ref(Taxonomy_Ref('auto_reg')) is taxonomy
            assert _.get_by_id(taxonomy.taxonomy_id)      is taxonomy

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods - Deterministic ID
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_with__deterministic_id(self):                                      # Test creating with deterministic ID
        seed = Safe_Str__Id__Seed('test:taxonomy:det')

        with self.registry as _:
            taxonomy = _.create_with__deterministic_id(taxonomy_ref  = Taxonomy_Ref('deterministic'),
                                                       root_category = Category_Ref('')              ,
                                                       seed          = seed                          )

            assert type(taxonomy)             is Schema__Taxonomy
            assert str(taxonomy.taxonomy_ref) == 'deterministic'
            assert taxonomy.taxonomy_id_source is not None
            assert str(taxonomy.taxonomy_id_source.seed) == 'test:taxonomy:det'

    def test__create_with__deterministic_id__same_seed_same_id(self):                   # Test deterministic reproducibility
        seed = Safe_Str__Id__Seed('test:taxonomy:reproducible')

        with Taxonomy__Registry() as registry_1:
            taxonomy_1 = registry_1.create_with__deterministic_id(taxonomy_ref  = Taxonomy_Ref('rep'),
                                                                   root_category = Category_Ref('')   ,
                                                                   seed          = seed               )

        with Taxonomy__Registry() as registry_2:
            taxonomy_2 = registry_2.create_with__deterministic_id(taxonomy_ref  = Taxonomy_Ref('rep'),
                                                                   root_category = Category_Ref('')   ,
                                                                   seed          = seed               )

        assert str(taxonomy_1.taxonomy_id) == str(taxonomy_2.taxonomy_id)               # Same seed → same ID

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods - Explicit ID
    # ═══════════════════════════════════════════════════════════════════════════

    def test__create_with__explicit_id(self):                                           # Test creating with explicit ID
        explicit_id = Taxonomy_Id(Obj_Id())

        with self.registry as _:
            taxonomy = _.create_with__explicit_id(taxonomy_ref  = Taxonomy_Ref('explicit'),
                                                  root_category = Category_Ref('')         ,
                                                  taxonomy_id   = explicit_id              )

            assert taxonomy.taxonomy_id      == explicit_id
            assert _.get_by_id(explicit_id)  is taxonomy

    # ═══════════════════════════════════════════════════════════════════════════
    # Registration and Lookup
    # ═══════════════════════════════════════════════════════════════════════════

    def test__register(self):                                                           # Test manual registration
        taxonomy = Schema__Taxonomy(taxonomy_id   = Taxonomy_Id(Obj_Id())               ,
                                    taxonomy_ref  = Taxonomy_Ref('manual')              ,
                                    root_category = Category_Ref('root')                )

        with self.registry as _:
            result = _.register(taxonomy)

            assert result is taxonomy                                                   # Returns the taxonomy
            assert _.get_by_ref(Taxonomy_Ref('manual')) is taxonomy
            assert _.get_by_id(taxonomy.taxonomy_id)    is taxonomy

    def test__get_by_ref__returns_none_for_unknown(self):                               # Test missing ref lookup
        with self.registry as _:
            assert _.get_by_ref(Taxonomy_Ref('unknown'))     is None
            assert _.get_by_ref(Taxonomy_Ref('nonexistent')) is None

    def test__get_by_id__returns_none_for_unknown(self):                                # Test missing ID lookup
        with self.registry as _:
            assert _.get_by_id(Taxonomy_Id(Obj_Id())) is None

    def test__has_ref(self):                                                            # Test ref existence check
        with self.registry as _:
            _.create_with__random_id(taxonomy_ref  = Taxonomy_Ref('exists'),
                                     root_category = Category_Ref('')      )

            assert _.has_ref(Taxonomy_Ref('exists'))     is True
            assert _.has_ref(Taxonomy_Ref('not_exists')) is False

    def test__has_id(self):                                                             # Test ID existence check
        with self.registry as _:
            taxonomy = _.create_with__random_id(taxonomy_ref  = Taxonomy_Ref('has_id'),
                                                root_category = Category_Ref('')      )

            assert _.has_id(taxonomy.taxonomy_id)      is True
            assert _.has_id(Taxonomy_Id(Obj_Id()))     is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Listing Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__all_refs(self):                                                           # Test listing all refs
        with self.registry as _:
            refs = _.all_refs()
            assert type(refs) is List__Taxonomy_Refs
            assert len(refs)  == 0                                                      # Initially empty

            _.create_with__random_id(Taxonomy_Ref('tax1'), Category_Ref(''))
            _.create_with__random_id(Taxonomy_Ref('tax2'), Category_Ref(''))
            _.create_with__random_id(Taxonomy_Ref('tax3'), Category_Ref(''))

            refs = _.all_refs()
            assert len(refs) == 3

            ref_strs = [str(r) for r in refs]
            assert 'tax1' in ref_strs
            assert 'tax2' in ref_strs
            assert 'tax3' in ref_strs

    def test__all_ids(self):                                                            # Test listing all IDs
        with self.registry as _:
            ids = _.all_ids()
            assert type(ids) is List__Taxonomy_Ids
            assert len(ids)  == 0                                                       # Initially empty

            _.create_with__random_id(Taxonomy_Ref('tax1'), Category_Ref(''))
            _.create_with__random_id(Taxonomy_Ref('tax2'), Category_Ref(''))

            ids = _.all_ids()
            assert len(ids) == 2

    # ═══════════════════════════════════════════════════════════════════════════
    # Overwrite Behavior
    # ═══════════════════════════════════════════════════════════════════════════

    def test__overwrite_existing_ref(self):                                             # Test same ref overwrites
        with self.registry as _:
            v1 = _.create_with__random_id(taxonomy_ref  = Taxonomy_Ref('versioned'),
                                          root_category = Category_Ref('')          ,
                                          version       = Safe_Str__Version('1.0.0'))

            assert str(_.get_by_ref(Taxonomy_Ref('versioned')).version) == '1.0.0'

            v2 = _.create_with__random_id(taxonomy_ref  = Taxonomy_Ref('versioned'),
                                          root_category = Category_Ref('')          ,
                                          version       = Safe_Str__Version('2.0.0'))

            assert str(_.get_by_ref(Taxonomy_Ref('versioned')).version) == '2.0.0'
            assert len(_.all_refs()) == 1                                               # Still just one ref entry

    # ═══════════════════════════════════════════════════════════════════════════
    # Dual Lookup Consistency
    # ═══════════════════════════════════════════════════════════════════════════

    def test__dual_lookup_consistency(self):                                            # Test by_ref and by_id same object
        with self.registry as _:
            taxonomy = _.create_with__random_id(taxonomy_ref  = Taxonomy_Ref('dual'),
                                                root_category = Category_Ref('')    )

            by_ref = _.get_by_ref(Taxonomy_Ref('dual'))
            by_id  = _.get_by_id(taxonomy.taxonomy_id)

            assert by_ref is by_id                                                      # Same object
            assert by_ref is taxonomy

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with QA Test Data
    # ═══════════════════════════════════════════════════════════════════════════

    def test__register_qa_taxonomy(self):                                               # Test registering QA-created taxonomy
        taxonomy = self.qa.create_taxonomy__code_elements()

        with self.registry as _:
            _.register(taxonomy)

            assert _.get_by_ref(Taxonomy_Ref('code_elements')) is taxonomy
            assert _.has_ref(Taxonomy_Ref('code_elements'))    is True

            refs = _.all_refs()
            ref_strs = [str(r) for r in refs]
            assert 'code_elements' in ref_strs

    def test__qa_taxonomy__has_categories(self):                                        # Test QA taxonomy has expected categories
        taxonomy = self.qa.create_taxonomy__code_elements()

        assert len(taxonomy.categories) == 4                                            # code_element, container, code_unit, callable

        category_refs = [str(k) for k in taxonomy.categories.keys()]
        assert 'code_element' in category_refs
        assert 'container'    in category_refs
        assert 'code_unit'    in category_refs
        assert 'callable'     in category_refs

    def test__qa_taxonomy__minimal(self):                                               # Test minimal QA taxonomy
        taxonomy = self.qa.create_taxonomy__minimal()

        with self.registry as _:
            _.register(taxonomy)

            retrieved = _.get_by_ref(Taxonomy_Ref('minimal'))
            assert len(retrieved.categories) == 1
            assert str(retrieved.root_category) == 'root'

    def test__qa_taxonomy__hierarchy(self):                                             # Test QA taxonomy hierarchy
        taxonomy = self.qa.create_taxonomy__code_elements()

        # Check root
        assert str(taxonomy.root_category) == 'code_element'

        # Check parent-child relationships
        root = taxonomy.categories[Category_Ref('code_element')]
        assert 'container' in [str(c) for c in root.child_refs]
        assert 'code_unit' in [str(c) for c in root.child_refs]

        container = taxonomy.categories[Category_Ref('container')]
        assert str(container.parent_ref) == 'code_element'

    def test__qa_taxonomy__dual_lookup(self):                                           # Test QA taxonomy dual lookup
        taxonomy = self.qa.create_taxonomy__code_elements()

        with self.registry as _:
            _.register(taxonomy)

            by_ref = _.get_by_ref(Taxonomy_Ref('code_elements'))
            by_id  = _.get_by_id(taxonomy.taxonomy_id)

            assert by_ref is by_id
            assert by_ref is taxonomy