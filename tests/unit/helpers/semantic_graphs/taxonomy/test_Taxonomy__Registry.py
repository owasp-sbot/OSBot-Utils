# ═══════════════════════════════════════════════════════════════════════════════
# Test Taxonomy__Registry - Tests for taxonomy registry with typed collections
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Taxonomies__By_Id     import Dict__Taxonomies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                 import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                 import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Registry                    import Taxonomy__Registry

# todo:
#     :
#       - the dict from test__load_from_dict below should come from the QA_...testing... file

class test_Taxonomy__Registry(TestCase):                                             # Test taxonomy registry

    def setUp(self):                                                                 # Fresh registry for each test
        self.registry = Taxonomy__Registry()

    def test__init__(self):                                                          # Test basic creation
        with Taxonomy__Registry() as _:
            assert type(_.cache) is Dict__Taxonomies__By_Id
            assert len(_.cache)  == 0

    def test__load_from_dict(self):                                                  # Test loading from dictionary
        data = {'taxonomy_id'  : 'test_taxonomy'                                     ,
                'version'      : '1.0.0'                                             ,
                'description'  : 'Test taxonomy'                                     ,
                'root_category': 'root'                                              ,
                'categories'   : {
                    'root': {'category_id': 'root'                                   ,
                             'name'       : 'root'                                   ,
                             'description': 'Root category'                          ,
                             'parent_ref' : ''                                       ,
                             'child_refs' : ['child1', 'child2']                     },
                    'child1': {'category_id': 'child1'                               ,
                               'name'       : 'child1'                               ,
                               'description': 'First child'                          ,
                               'parent_ref' : 'root'                                 ,
                               'child_refs' : []                                     },
                    'child2': {'category_id': 'child2'                               ,
                               'name'       : 'child2'                               ,
                               'description': 'Second child'                         ,
                               'parent_ref' : 'root'                                 ,
                               'child_refs' : []                                     }}}

        with self.registry as _:
            taxonomy = _.load_from_dict(data)

            assert type(taxonomy)            is Schema__Taxonomy
            assert str(taxonomy.taxonomy_id) == 'test_taxonomy'
            assert len(taxonomy.categories)  == 3

    def test__get_and_register(self):                                                # Test get and register operations
        with self.registry as _:
            assert _.get('unknown') is None

            taxonomy = Schema__Taxonomy(taxonomy_id   = Taxonomy_Id('manual'),
                                        root_category = Category_Id('root') ,
                                        categories    = {}                  )
            _.register(taxonomy)

            assert _.get('manual') is taxonomy

    def test__list_taxonomies(self):                                                 # Test listing taxonomies
        with self.registry as _:
            assert _.list_taxonomies() == []

            _.load_from_dict({'taxonomy_id': 'tax1', 'root_category': '', 'categories': {}})
            _.load_from_dict({'taxonomy_id': 'tax2', 'root_category': '', 'categories': {}})

            taxonomies = _.list_taxonomies()
            assert len(taxonomies) == 2
            assert 'tax1' in taxonomies
            assert 'tax2' in taxonomies

    def test__clear(self):                                                           # Test cache clearing
        with self.registry as _:
            _.load_from_dict({'taxonomy_id': 'tax', 'root_category': '', 'categories': {}})
            assert len(_.cache) == 1

            _.clear()
            assert len(_.cache) == 0

    def test__cache_type(self):                                                      # Test cache is properly typed
        with self.registry as _:
            _.load_from_dict({'taxonomy_id': 'test', 'root_category': 'root',
                             'categories': {'root': {'category_id': 'root', 'name': 'root',
                                                     'parent_ref': '', 'child_refs': []}}})

            assert type(_.cache) is Dict__Taxonomies__By_Id
            assert type(_.cache['test']) is Schema__Taxonomy