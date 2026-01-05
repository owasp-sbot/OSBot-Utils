# ═══════════════════════════════════════════════════════════════════════════════
# Test Taxonomy__Utils - Tests for taxonomy utility operations
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Refs         import List__Category_Refs
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category    import Schema__Taxonomy__Category
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Utils                       import Taxonomy__Utils
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data         import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                             import __, __SKIP__


class test_Taxonomy__Utils(TestCase):                                                   # Test taxonomy utilities

    @classmethod
    def setUpClass(cls):                                                                # Shared test objects (performance)
        cls.qa       = QA__Semantic_Graphs__Test_Data()
        cls.utils    = Taxonomy__Utils()
        cls.taxonomy = cls.qa.create_taxonomy__code_elements()                          # Reuse across all tests

    def test__init__(self):                                                             # Test initialization
        with Taxonomy__Utils() as _:
            assert type(_) is Taxonomy__Utils

    def test__taxonomy_structure(self):                                                 # Verify test taxonomy structure
        with self.taxonomy as _:
            assert type(_) is Schema__Taxonomy
            assert _.obj() == __(taxonomy_id        = __SKIP__                         ,  # Deterministic ID
                                 taxonomy_id_source = __SKIP__                         ,
                                 taxonomy_ref  = 'code_elements'                       ,
                                 version       = '1.0.0'                               ,
                                 description   = 'Code elements taxonomy'              ,
                                 root_category = 'code_element'                        ,
                                 categories    = __(code_element = __(category_ref = 'code_element'              ,
                                                                      name         = 'code_element'              ,
                                                                      description  = 'Root category'             ,
                                                                      parent_ref   = ''                          ,
                                                                      child_refs   = ['container', 'code_unit'] ),
                                                    container    = __(category_ref = 'container'                 ,
                                                                      name         = 'container'                 ,
                                                                      description  = 'Container elements'        ,
                                                                      parent_ref   = 'code_element'              ,
                                                                      child_refs   = []                         ),
                                                    code_unit    = __(category_ref = 'code_unit'                 ,
                                                                      name         = 'code_unit'                 ,
                                                                      description  = 'Executable code'           ,
                                                                      parent_ref   = 'code_element'              ,
                                                                      child_refs   = ['callable']               ),
                                                    callable     = __(category_ref = 'callable'                  ,
                                                                      name         = 'callable'                  ,
                                                                      description  = 'Callable code'             ,
                                                                      parent_ref   = 'code_unit'                 ,
                                                                      child_refs   = []                         )))

    # ═══════════════════════════════════════════════════════════════════════════
    # Category Retrieval
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_category(self):                                                       # Test category retrieval
        root = self.utils.get_category(self.taxonomy, Category_Ref('code_element'))

        assert root is not None
        assert type(root) is Schema__Taxonomy__Category
        assert str(root.name) == 'code_element'

    def test__get_category__nested(self):                                               # Test nested category retrieval
        container = self.utils.get_category(self.taxonomy, Category_Ref('container'))
        callable_ = self.utils.get_category(self.taxonomy, Category_Ref('callable'))

        assert container is not None
        assert str(container.description) == 'Container elements'
        assert callable_ is not None
        assert str(callable_.parent_ref) == 'code_unit'

    def test__get_category__nonexistent(self):                                          # Test nonexistent category
        result = self.utils.get_category(self.taxonomy, Category_Ref('nonexistent'))

        assert result is None

    def test__has_category(self):                                                       # Test category existence check
        assert self.utils.has_category(self.taxonomy, Category_Ref('code_element')) is True
        assert self.utils.has_category(self.taxonomy, Category_Ref('container'))    is True
        assert self.utils.has_category(self.taxonomy, Category_Ref('nonexistent'))  is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Root and Parent Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_root_category(self):                                                  # Test root category retrieval
        root = self.utils.get_root_category(self.taxonomy)

        assert root is not None
        assert str(root.category_ref) == 'code_element'
        assert str(root.parent_ref)   == ''

    def test__get_parent(self):                                                         # Test parent category retrieval
        container_parent = self.utils.get_parent(self.taxonomy, Category_Ref('container'))
        callable_parent  = self.utils.get_parent(self.taxonomy, Category_Ref('callable'))

        assert container_parent is not None
        assert str(container_parent.name) == 'code_element'

        assert callable_parent is not None
        assert str(callable_parent.name) == 'code_unit'

    def test__get_parent__root_has_no_parent(self):                                     # Test root has no parent
        root_parent = self.utils.get_parent(self.taxonomy, Category_Ref('code_element'))

        assert root_parent is None

    def test__get_parent__nonexistent(self):                                            # Test parent of nonexistent category
        result = self.utils.get_parent(self.taxonomy, Category_Ref('nonexistent'))

        assert result is None

    # ═══════════════════════════════════════════════════════════════════════════
    # Children Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_children(self):                                                       # Test child category retrieval
        root_children = self.utils.get_children(self.taxonomy, Category_Ref('code_element'))

        assert type(root_children) is List__Category_Refs
        assert len(root_children)  == 2
        child_names = [str(c) for c in root_children]
        assert 'container' in child_names
        assert 'code_unit' in child_names

    def test__get_children__single_child(self):                                         # Test category with single child
        code_unit_children = self.utils.get_children(self.taxonomy, Category_Ref('code_unit'))

        assert len(code_unit_children)    == 1
        assert str(code_unit_children[0]) == 'callable'

    def test__get_children__no_children(self):                                          # Test leaf category (no children)
        container_children = self.utils.get_children(self.taxonomy, Category_Ref('container'))
        callable_children  = self.utils.get_children(self.taxonomy, Category_Ref('callable'))

        assert len(container_children) == 0
        assert len(callable_children)  == 0

    def test__get_children__nonexistent(self):                                          # Test children of nonexistent category
        result = self.utils.get_children(self.taxonomy, Category_Ref('nonexistent'))

        assert len(result) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Category Listing
    # ═══════════════════════════════════════════════════════════════════════════

    def test__all_category_refs(self):                                                  # Test listing all category refs
        refs = self.utils.all_category_refs(self.taxonomy)

        assert type(refs) is List__Category_Refs
        assert len(refs)  == 4

        ref_names = [str(r) for r in refs]
        assert 'code_element' in ref_names
        assert 'container'    in ref_names
        assert 'code_unit'    in ref_names
        assert 'callable'     in ref_names

    # ═══════════════════════════════════════════════════════════════════════════
    # Ancestor Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_ancestors__root(self):                                                # Test ancestors of root (none)
        ancestors = self.utils.get_ancestors(self.taxonomy, Category_Ref('code_element'))

        assert len(ancestors) == 0

    def test__get_ancestors__one_level(self):                                           # Test ancestors one level deep
        ancestors = self.utils.get_ancestors(self.taxonomy, Category_Ref('container'))

        assert len(ancestors)    == 1
        assert 'code_element' in [str(a) for a in ancestors]

    def test__get_ancestors__two_levels(self):                                          # Test ancestors two levels deep
        ancestors = self.utils.get_ancestors(self.taxonomy, Category_Ref('callable'))

        assert len(ancestors) == 2
        ancestor_names = [str(a) for a in ancestors]
        assert 'code_unit'    in ancestor_names                                         # Parent
        assert 'code_element' in ancestor_names                                         # Grandparent

    # ═══════════════════════════════════════════════════════════════════════════
    # Descendant Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_descendants__from_root(self):                                         # Test descendants from root
        descendants = self.utils.get_descendants(self.taxonomy, Category_Ref('code_element'))

        assert len(descendants) == 3                                                    # container, code_unit, callable

    def test__get_descendants__from_middle(self):                                       # Test descendants from middle node
        descendants = self.utils.get_descendants(self.taxonomy, Category_Ref('code_unit'))

        assert len(descendants)    == 1
        assert 'callable' in [str(d) for d in descendants]

    def test__get_descendants__from_leaf(self):                                         # Test descendants from leaf (none)
        container_descendants = self.utils.get_descendants(self.taxonomy, Category_Ref('container'))
        callable_descendants  = self.utils.get_descendants(self.taxonomy, Category_Ref('callable'))

        assert len(container_descendants) == 0
        assert len(callable_descendants)  == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Relationship Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__is_ancestor_of(self):                                                     # Test ancestor relationship
        assert self.utils.is_ancestor_of(self.taxonomy, Category_Ref('code_element'), Category_Ref('callable'))    is True
        assert self.utils.is_ancestor_of(self.taxonomy, Category_Ref('code_unit')   , Category_Ref('callable'))    is True
        assert self.utils.is_ancestor_of(self.taxonomy, Category_Ref('callable')    , Category_Ref('code_element')) is False
        assert self.utils.is_ancestor_of(self.taxonomy, Category_Ref('container')   , Category_Ref('callable'))    is False

    def test__is_descendant_of(self):                                                   # Test descendant relationship
        assert self.utils.is_descendant_of(self.taxonomy, Category_Ref('callable')    , Category_Ref('code_element')) is True
        assert self.utils.is_descendant_of(self.taxonomy, Category_Ref('callable')    , Category_Ref('code_unit'))    is True
        assert self.utils.is_descendant_of(self.taxonomy, Category_Ref('code_element'), Category_Ref('callable'))     is False

    def test__depth(self):                                                              # Test depth calculation
        assert self.utils.depth(self.taxonomy, Category_Ref('code_element')) == 0       # Root
        assert self.utils.depth(self.taxonomy, Category_Ref('container'))    == 1       # One level
        assert self.utils.depth(self.taxonomy, Category_Ref('code_unit'))    == 1       # One level
        assert self.utils.depth(self.taxonomy, Category_Ref('callable'))     == 2       # Two levels

    # ═══════════════════════════════════════════════════════════════════════════
    # Minimal Taxonomy Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__minimal_taxonomy(self):                                                   # Test with minimal taxonomy
        minimal = self.qa.create_taxonomy__minimal()

        root = self.utils.get_root_category(minimal)
        assert str(root.category_ref) == 'root'

        refs = self.utils.all_category_refs(minimal)
        assert len(refs) == 1

        ancestors   = self.utils.get_ancestors(minimal, Category_Ref('root'))
        descendants = self.utils.get_descendants(minimal, Category_Ref('root'))
        assert len(ancestors)   == 0
        assert len(descendants) == 0


