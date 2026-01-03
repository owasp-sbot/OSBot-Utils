from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Registry                    import Taxonomy__Registry
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                   import Type_Safe__Dict


class test_Taxonomy__Registry(TestCase):                                             # Test taxonomy registry

    def setUp(self):                                                                 # Fresh registry for each test
        self.registry = Taxonomy__Registry()

    def test__init__(self):                                                          # Test basic creation
        with Taxonomy__Registry() as _:
            assert type(_.cache) is Type_Safe__Dict
            assert _.cache       == {}

    def test__load_from_dict(self):                                                  # Test loading from dictionary
        data = {
            'taxonomy_id'  : 'test_taxonomy'                                         ,
            'version'      : '1.0.0'                                                 ,
            'description'  : 'Test taxonomy'                                         ,
            'root_category': 'root'                                                  ,
            'categories'   : {
                'root': {
                    'category_id': 'root'                                            ,
                    'name'       : 'root'                                            ,
                    'description': 'Root category'                                   ,
                    'parent_ref' : ''                                                ,
                    'child_refs' : ['child1', 'child2']                              ,
                }                                                                    ,
                'child1': {
                    'category_id': 'child1'                                          ,
                    'name'       : 'child1'                                          ,
                    'description': 'First child'                                     ,
                    'parent_ref' : 'root'                                            ,
                    'child_refs' : []                                                ,
                }                                                                    ,
                'child2': {
                    'category_id': 'child2'                                          ,
                    'name'       : 'child2'                                          ,
                    'description': 'Second child'                                    ,
                    'parent_ref' : 'root'                                            ,
                    'child_refs' : []                                                ,
                }                                                                    ,
            }
        }

        with self.registry as _:
            taxonomy = _.load_from_dict(data)

            assert type(taxonomy)           is Schema__Taxonomy
            assert str(taxonomy.taxonomy_id) == 'test_taxonomy'
            assert len(taxonomy.categories)  == 3

            root = taxonomy.get_root()
            assert root is not None
            assert len(taxonomy.get_children('root')) == 2

    def test__clear(self):                                                           # Test cache clearing
        with self.registry as _:
            _.load_from_dict({'taxonomy_id': 'tax', 'root_category': '', 'categories': {}})
            assert len(_.cache) == 1

            _.clear()
            assert len(_.cache) == 0

    def test__get_and_list(self):                                                    # Test get and list operations
        with self.registry as _:
            assert _.get('unknown') is None
            assert _.list_taxonomies() == []

            _.load_from_dict({'taxonomy_id': 'tax1', 'root_category': '', 'categories': {}})
            _.load_from_dict({'taxonomy_id': 'tax2', 'root_category': '', 'categories': {}})

            assert _.get('tax1') is not None
            assert _.get('tax2') is not None
            assert len(_.list_taxonomies()) == 2
