from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                 import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                 import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category    import Schema__Taxonomy__Category


class test_Schema__Taxonomy(TestCase):                                               # Test main taxonomy schema

    @classmethod
    def setUpClass(cls):                                                             # Create test taxonomy once
        cls.taxonomy = cls.create_test_taxonomy()

    @classmethod
    def create_test_taxonomy(cls) -> Schema__Taxonomy:                               # Build hierarchical test taxonomy
        root = Schema__Taxonomy__Category(
            category_id = Category_Id('code_element')                                ,
            name        = 'code_element'                                             ,
            description = 'Root category for all code elements'                      ,
            parent_ref  = Category_Id('')                                            ,
            child_refs  = [Category_Id('container'), Category_Id('code_unit')]       ,
        )

        container = Schema__Taxonomy__Category(
            category_id = Category_Id('container')                                   ,
            name        = 'container'                                                ,
            description = 'Elements that contain other elements'                     ,
            parent_ref  = Category_Id('code_element')                                ,
            child_refs  = []                                                         ,
        )

        code_unit = Schema__Taxonomy__Category(
            category_id = Category_Id('code_unit')                                   ,
            name        = 'code_unit'                                                ,
            description = 'Executable code units'                                    ,
            parent_ref  = Category_Id('code_element')                                ,
            child_refs  = [Category_Id('callable')]                                  ,
        )

        callable_cat = Schema__Taxonomy__Category(
            category_id = Category_Id('callable')                                    ,
            name        = 'callable'                                                 ,
            description = 'Callable code units'                                      ,
            parent_ref  = Category_Id('code_unit')                                   ,
            child_refs  = []                                                         ,
        )

        return Schema__Taxonomy(
            taxonomy_id   = Taxonomy_Id('code_elements')                              ,
            version       = '1.0.0'                                                  ,
            description   = 'Classification for Python code elements'                ,
            root_category = Category_Id('code_element')                              ,
            categories    = {
                'code_element': root                                                 ,
                'container'   : container                                            ,
                'code_unit'   : code_unit                                            ,
                'callable'    : callable_cat                                         ,
            }                                                                        ,
        )

    def test__init__(self):                                                          # Test basic initialization
        with Schema__Taxonomy(taxonomy_id=Taxonomy_Id('empty')) as _:
            assert type(_.taxonomy_id)   is Taxonomy_Id
            assert str(_.taxonomy_id)    == 'empty'
            assert str(_.version)        == '1.0.0'                                  # Default version
            assert str(_.description)    == ''
            assert str(_.root_category)  == ''
            assert _.categories          == {}

    def test__taxonomy_structure(self):                                              # Test full taxonomy structure
        with self.taxonomy as _:
            assert str(_.taxonomy_id)    == 'code_elements'
            assert len(_.categories)     == 4

    def test__get_category(self):                                                    # Test category retrieval
        with self.taxonomy as _:
            root = _.get_category('code_element')
            assert root is not None
            assert str(root.name) == 'code_element'

            container = _.get_category('container')
            assert container is not None
            assert str(container.description) == 'Elements that contain other elements'

            assert _.get_category('nonexistent') is None

    def test__get_root(self):                                                        # Test root category retrieval
        with self.taxonomy as _:
            root = _.get_root()
            assert root is not None
            assert str(root.category_id) == 'code_element'
            assert str(root.parent_ref)  == ''                                       # Root has no parent

    def test__get_children(self):                                                    # Test child category retrieval
        with self.taxonomy as _:
            root_children = _.get_children('code_element')
            assert len(root_children)    == 2
            child_names = [str(c.name) for c in root_children]
            assert 'container' in child_names
            assert 'code_unit' in child_names

            code_unit_children = _.get_children('code_unit')
            assert len(code_unit_children) == 1
            assert str(code_unit_children[0].name) == 'callable'

            container_children = _.get_children('container')                         # Leaf has no children
            assert len(container_children) == 0

            nonexistent_children = _.get_children('nonexistent')                     # Invalid ID
            assert len(nonexistent_children) == 0

    def test__get_parent(self):                                                      # Test parent category retrieval
        with self.taxonomy as _:
            root_parent = _.get_parent('code_element')                               # Root has no parent
            assert root_parent is None

            container_parent = _.get_parent('container')
            assert container_parent is not None
            assert str(container_parent.name) == 'code_element'

            callable_parent = _.get_parent('callable')
            assert callable_parent is not None
            assert str(callable_parent.name) == 'code_unit'

            assert _.get_parent('nonexistent') is None

    def test__get_ancestors(self):                                                   # Test ancestor chain retrieval
        with self.taxonomy as _:
            root_ancestors = _.get_ancestors('code_element')                         # Root has no ancestors
            assert len(root_ancestors) == 0

            container_ancestors = _.get_ancestors('container')                       # Direct child of root
            assert len(container_ancestors) == 1
            assert str(container_ancestors[0].name) == 'code_element'

            callable_ancestors = _.get_ancestors('callable')                         # Two levels deep
            assert len(callable_ancestors) == 2
            ancestor_names = [str(a.name) for a in callable_ancestors]
            assert 'code_unit'    in ancestor_names
            assert 'code_element' in ancestor_names

    def test__get_descendants(self):                                                 # Test descendant retrieval
        with self.taxonomy as _:
            root_descendants = _.get_descendants('code_element')                     # All descendants
            assert len(root_descendants) == 3                                        # container, code_unit, callable

            code_unit_descendants = _.get_descendants('code_unit')
            assert len(code_unit_descendants) == 1                                   # callable
            assert str(code_unit_descendants[0].name) == 'callable'

            container_descendants = _.get_descendants('container')                   # Leaf has no descendants
            assert len(container_descendants) == 0

    def test__category_ids(self):                                                    # Test category ID listing
        with self.taxonomy as _:
            ids = _.category_ids()
            assert len(ids) == 4
            assert 'code_element' in ids
            assert 'container'    in ids
            assert 'code_unit'    in ids
            assert 'callable'     in ids