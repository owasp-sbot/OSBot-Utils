# ═══════════════════════════════════════════════════════════════════════════════
# Test Taxonomy__Utils - Tests for taxonomy utility operations
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
#
# Updated for Brief 3.8:
#   - Categories use Category_Id (not Category_Ref) for lookups
#   - parent_ref → parent_id
#   - child_refs → child_ids
#   - ID-based navigation throughout
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Ids          import List__Category_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                 import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category    import Schema__Taxonomy__Category
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Utils                       import Taxonomy__Utils
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data         import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                             import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id


class test_Taxonomy__Utils(TestCase):                                                   # Test taxonomy utilities

    @classmethod
    def setUpClass(cls):                                                                # Shared test objects (performance)
        cls.test_data = QA__Semantic_Graphs__Test_Data()
        cls.utils     = Taxonomy__Utils()
        cls.taxonomy  = cls.test_data.create_taxonomy()                                 # Brief 3.8 API

        # Cache category IDs for tests
        cls.root_id      = cls.test_data.get_category_id__root()
        cls.callable_id  = cls.test_data.get_category_id__callable()
        cls.container_id = cls.test_data.get_category_id__container()
        cls.data_id      = cls.test_data.get_category_id__data()

    def test__init__(self):                                                             # Test initialization
        with Taxonomy__Utils() as _:
            assert type(_) is Taxonomy__Utils

    def test__taxonomy_structure(self):                                                 # Verify test taxonomy structure
        with self.taxonomy as _:
            assert type(_) is Schema__Taxonomy
            assert type(_.root_id)    is Category_Id                                    # Brief 3.8: root_id
            assert type(_.categories) is Dict__Categories__By_Id                         # Dict__Categories__By_Id

    # ═══════════════════════════════════════════════════════════════════════════
    # Category Retrieval (ID-based per Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_category(self):                                                       # Test category retrieval by ID
        root = self.utils.get_category(self.taxonomy, self.root_id)

        assert root is not None
        assert type(root) is Schema__Taxonomy__Category
        assert type(root.category_id) is Category_Id

    def test__get_category__nested(self):                                               # Test nested category retrieval
        callable_cat = self.utils.get_category(self.taxonomy, self.callable_id)

        assert callable_cat is not None
        assert callable_cat.parent_id is not None                                       # Has parent

    def test__get_category__nonexistent(self):                                          # Test nonexistent category
        unknown_id = Category_Id(Obj_Id())
        result = self.utils.get_category(self.taxonomy, unknown_id)

        assert result is None

    def test__has_category(self):                                                       # Test category existence check
        assert self.utils.has_category(self.taxonomy, self.root_id)      is True
        assert self.utils.has_category(self.taxonomy, self.callable_id)  is True
        assert self.utils.has_category(self.taxonomy, Category_Id(Obj_Id())) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Category Lookup by Ref
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_category_by_ref(self):                                                # Test category retrieval by ref
        root = self.utils.get_category_by_ref(self.taxonomy, Category_Ref('code_element'))

        assert root is not None
        assert root.category_id == self.root_id

    def test__get_category_by_ref__nonexistent(self):                                   # Test nonexistent ref
        result = self.utils.get_category_by_ref(self.taxonomy, Category_Ref('nonexistent'))

        assert result is None

    # ═══════════════════════════════════════════════════════════════════════════
    # Root and Parent Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_root_category(self):                                                  # Test root category retrieval
        root = self.utils.get_root_category(self.taxonomy)

        assert root is not None
        assert root.category_id == self.root_id
        assert root.parent_id   is None                                                 # Brief 3.8: parent_id

    def test__get_parent(self):                                                         # Test parent category retrieval
        callable_parent = self.utils.get_parent(self.taxonomy, self.callable_id)

        assert callable_parent is not None
        assert type(callable_parent) is Schema__Taxonomy__Category

    def test__get_parent__root_has_no_parent(self):                                     # Test root has no parent
        root_parent = self.utils.get_parent(self.taxonomy, self.root_id)

        assert root_parent is None

    def test__get_parent__nonexistent(self):                                            # Test parent of nonexistent category
        unknown_id = Category_Id(Obj_Id())
        result = self.utils.get_parent(self.taxonomy, unknown_id)

        assert result is None

    # ═══════════════════════════════════════════════════════════════════════════
    # Children Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_children(self):                                                       # Test child category retrieval
        root_children = self.utils.get_children(self.taxonomy, self.root_id)

        assert type(root_children) is List__Category_Ids                                # Brief 3.8: IDs not refs
        assert len(root_children)  >= 1                                                 # Root has children

    def test__get_children__no_children(self):                                          # Test leaf category (no children)
        # Data category is a leaf
        data_children = self.utils.get_children(self.taxonomy, self.data_id)

        assert len(data_children) == 0

    def test__get_children__nonexistent(self):                                          # Test children of nonexistent category
        unknown_id = Category_Id(Obj_Id())
        result = self.utils.get_children(self.taxonomy, unknown_id)

        assert len(result) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Category Listing
    # ═══════════════════════════════════════════════════════════════════════════

    def test__all_category_ids(self):                                                   # Test listing all category IDs
        ids = self.utils.all_category_ids(self.taxonomy)

        assert type(ids) is List__Category_Ids
        assert len(ids)  == 4                                                           # root, callable, container, data

        assert self.root_id      in ids
        assert self.callable_id  in ids
        assert self.container_id in ids
        assert self.data_id      in ids

    # ═══════════════════════════════════════════════════════════════════════════
    # Ancestor Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_ancestors__root(self):                                                # Test ancestors of root (none)
        ancestors = self.utils.get_ancestors(self.taxonomy, self.root_id)

        assert len(ancestors) == 0

    def test__get_ancestors__one_level(self):                                           # Test ancestors one level deep
        ancestors = self.utils.get_ancestors(self.taxonomy, self.callable_id)

        assert len(ancestors) >= 1                                                      # At least parent
        assert self.root_id in ancestors                                                # Root is ancestor

    # ═══════════════════════════════════════════════════════════════════════════
    # Descendant Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_descendants__from_root(self):                                         # Test descendants from root
        descendants = self.utils.get_descendants(self.taxonomy, self.root_id)

        assert len(descendants) >= 1                                                    # Has descendants

    def test__get_descendants__from_leaf(self):                                         # Test descendants from leaf (none)
        data_descendants = self.utils.get_descendants(self.taxonomy, self.data_id)

        assert len(data_descendants) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Relationship Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__is_ancestor_of(self):                                                     # Test ancestor relationship
        assert self.utils.is_ancestor_of(self.taxonomy, self.root_id, self.callable_id)     is True
        assert self.utils.is_ancestor_of(self.taxonomy, self.callable_id, self.root_id)     is False

    def test__is_descendant_of(self):                                                   # Test descendant relationship
        assert self.utils.is_descendant_of(self.taxonomy, self.callable_id, self.root_id)   is True
        assert self.utils.is_descendant_of(self.taxonomy, self.root_id, self.callable_id)   is False

    def test__depth(self):                                                              # Test depth calculation
        assert self.utils.depth(self.taxonomy, self.root_id) == 0                       # Root is depth 0

        callable_depth = self.utils.depth(self.taxonomy, self.callable_id)
        assert callable_depth >= 1                                                      # At least one level deep

    # ═══════════════════════════════════════════════════════════════════════════
    # ID ↔ Ref Conversion
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_category_id_by_ref(self):                                             # Test ID lookup by ref
        cat_id = self.utils.get_category_id_by_ref(self.taxonomy, Category_Ref('code_element'))

        assert cat_id == self.root_id

    def test__get_category_id_by_ref__nonexistent(self):                                # Test nonexistent ref
        cat_id = self.utils.get_category_id_by_ref(self.taxonomy, Category_Ref('nonexistent'))

        assert cat_id is None

    def test__get_category_ref_by_id(self):                                             # Test ref lookup by ID
        cat_ref = self.utils.get_category_ref_by_id(self.taxonomy, self.root_id)

        assert type(cat_ref) is Category_Ref
        assert str(cat_ref) == 'code_element'

    def test__get_category_ref_by_id__nonexistent(self):                                # Test nonexistent ID
        unknown_id = Category_Id(Obj_Id())
        cat_ref = self.utils.get_category_ref_by_id(self.taxonomy, unknown_id)

        assert cat_ref is None

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with Complete Fixture
    # ═══════════════════════════════════════════════════════════════════════════

    def test__fixture_taxonomy_navigation(self):                                        # Test full navigation
        fixture  = self.test_data.create_complete_fixture()
        taxonomy = fixture['taxonomy']

        root = self.utils.get_root_category(taxonomy)
        assert root is not None

        children = self.utils.get_children(taxonomy, root.category_id)
        assert type(children) is List__Category_Ids

        all_ids = self.utils.all_category_ids(taxonomy)
        assert len(all_ids) == 4