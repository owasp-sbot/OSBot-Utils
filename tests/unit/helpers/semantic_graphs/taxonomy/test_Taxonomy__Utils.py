# ═══════════════════════════════════════════════════════════════════════════════
# Test Taxonomy__Utils - Tests for taxonomy utility operations
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Utils                       import Taxonomy__Utils
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                 import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                 import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category    import Schema__Taxonomy__Category
from osbot_utils.testing.__ import __


# todo:
#     :
#       - move create_test_taxonomy to a helper QA__Semantic_Graph__Test_Data utils class
#       - add util to create visualisation of these schema in mermaid since these note only these are nice graphs,
#               that will help with creating, editing and visualising these taxonomies


class test_Taxonomy__Utils(TestCase):                                                # Test taxonomy utilities

    @classmethod
    def setUpClass(cls):                                                             # Create shared test taxonomy
        cls.utils    = Taxonomy__Utils()
        cls.taxonomy = cls.create_test_taxonomy()

    @classmethod
    def create_test_taxonomy(cls) -> Schema__Taxonomy:                               # Build hierarchical test taxonomy
        root = Schema__Taxonomy__Category(category_id = Category_Id('code_element'),
                                          name        = 'code_element'             ,
                                          description = 'Root category'            ,
                                          parent_ref  = Category_Id('')            ,
                                          child_refs  = [Category_Id('container'),
                                                         Category_Id('code_unit')])

        container = Schema__Taxonomy__Category(category_id = Category_Id('container'),
                                               name        = 'container'             ,
                                               description = 'Container elements'    ,
                                               parent_ref  = Category_Id('code_element'),
                                               child_refs  = []                      )

        code_unit = Schema__Taxonomy__Category(category_id = Category_Id('code_unit'),
                                               name        = 'code_unit'             ,
                                               description = 'Executable code'       ,
                                               parent_ref  = Category_Id('code_element'),
                                               child_refs  = [Category_Id('callable')])

        callable_cat = Schema__Taxonomy__Category(category_id = Category_Id('callable'),
                                                  name        = 'callable'             ,
                                                  description = 'Callable code'        ,
                                                  parent_ref  = Category_Id('code_unit'),
                                                  child_refs  = []                     )

        return Schema__Taxonomy(taxonomy_id   = Taxonomy_Id('code_elements'),
                                version       = '1.0.0'                    ,
                                description   = 'Test taxonomy'            ,
                                root_category = Category_Id('code_element'),
                                categories    = {'code_element': root      ,
                                                 'container'   : container ,
                                                 'code_unit'   : code_unit ,
                                                 'callable'    : callable_cat})

    def test__create_test_taxonomy(self):
        with self.taxonomy as _:
            assert type(_) is Schema__Taxonomy
            assert _.obj() == __(version      = '1.0.0'                             ,
                                 taxonomy_id  = 'code_elements'                     ,
                                 description  = 'Test taxonomy'                     ,
                                 root_category= 'code_element'                      ,
                                 categories   = __(code_element = __(category_id  = 'code_element'       ,
                                                                     name         = 'code_element'       ,
                                                                     description  = 'Root category'      ,
                                                                     parent_ref   = ''                   ,
                                                                     child_refs   = ['container', 'code_unit']),
                                                   container    = __(category_id  = 'container'          ,
                                                                     name         = 'container'          ,
                                                                     description  = 'Container elements' ,
                                                                     parent_ref   = 'code_element'       ,
                                                                     child_refs   = []                  ),
                                                   code_unit    = __(category_id  = 'code_unit'          ,
                                                                     name         = 'code_unit'          ,
                                                                     description  = 'Executable code'    ,
                                                                     parent_ref   = 'code_element'       ,
                                                                     child_refs   = ['callable']        ),
                                                   callable     = __(category_id  = 'callable'           ,
                                                                     name         = 'callable'           ,
                                                                     description  = 'Callable code'      ,
                                                                     parent_ref   = 'code_unit'          ,
                                                                     child_refs   = []                  )))


    def test__init__(self):                                                          # Test initialization
        with Taxonomy__Utils() as _:
            assert type(_) is Taxonomy__Utils

    def test__get_category(self):                                                    # Test category retrieval
        root = self.utils.get_category(self.taxonomy, 'code_element')
        assert root is not None
        assert str(root.name) == 'code_element'

        container = self.utils.get_category(self.taxonomy, 'container')
        assert container is not None
        assert str(container.description) == 'Container elements'

        assert self.utils.get_category(self.taxonomy, 'nonexistent') is None

    def test__get_root(self):                                                        # Test root category retrieval
        root = self.utils.get_root(self.taxonomy)

        assert root is not None
        assert str(root.category_id) == 'code_element'
        assert str(root.parent_ref)  == ''

    def test__category_ids(self):                                                    # Test category ID listing
        ids = self.utils.category_ids(self.taxonomy)

        assert len(ids) == 4
        assert 'code_element' in ids
        assert 'container'    in ids
        assert 'code_unit'    in ids
        assert 'callable'     in ids

    def test__get_children(self):                                                    # Test child category retrieval
        root_children = self.utils.get_children(self.taxonomy, 'code_element')
        assert len(root_children) == 2
        child_names = [str(c.name) for c in root_children]
        assert 'container' in child_names
        assert 'code_unit' in child_names

        code_unit_children = self.utils.get_children(self.taxonomy, 'code_unit')
        assert len(code_unit_children) == 1
        assert str(code_unit_children[0].name) == 'callable'

        container_children = self.utils.get_children(self.taxonomy, 'container')
        assert len(container_children) == 0

        nonexistent_children = self.utils.get_children(self.taxonomy, 'nonexistent')
        assert len(nonexistent_children) == 0

    def test__get_parent(self):                                                      # Test parent category retrieval
        root_parent = self.utils.get_parent(self.taxonomy, 'code_element')
        assert root_parent is None

        container_parent = self.utils.get_parent(self.taxonomy, 'container')
        assert container_parent is not None
        assert str(container_parent.name) == 'code_element'

        callable_parent = self.utils.get_parent(self.taxonomy, 'callable')
        assert callable_parent is not None
        assert str(callable_parent.name) == 'code_unit'

        assert self.utils.get_parent(self.taxonomy, 'nonexistent') is None

    def test__get_ancestors(self):                                                   # Test ancestor chain retrieval
        root_ancestors = self.utils.get_ancestors(self.taxonomy, 'code_element')
        assert len(root_ancestors) == 0

        container_ancestors = self.utils.get_ancestors(self.taxonomy, 'container')
        assert len(container_ancestors) == 1
        assert str(container_ancestors[0].name) == 'code_element'

        callable_ancestors = self.utils.get_ancestors(self.taxonomy, 'callable')
        assert len(callable_ancestors) == 2
        ancestor_names = [str(a.name) for a in callable_ancestors]
        assert 'code_unit'    in ancestor_names
        assert 'code_element' in ancestor_names

    def test__get_descendants(self):                                                 # Test descendant retrieval
        root_descendants = self.utils.get_descendants(self.taxonomy, 'code_element')
        assert len(root_descendants) == 3                                            # container, code_unit, callable

        code_unit_descendants = self.utils.get_descendants(self.taxonomy, 'code_unit')
        assert len(code_unit_descendants) == 1
        assert str(code_unit_descendants[0].name) == 'callable'

        container_descendants = self.utils.get_descendants(self.taxonomy, 'container')
        assert len(container_descendants) == 0