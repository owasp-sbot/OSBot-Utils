# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Taxonomy - Tests for taxonomy schema (pure data)
# Note: Taxonomy operations have been moved to Taxonomy__Utils
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id     import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                 import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                 import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category    import Schema__Taxonomy__Category
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text            import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version         import Safe_Str__Version
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe


class test_Schema__Taxonomy(TestCase):                                               # Test taxonomy schema

    def test__init__(self):                                                          # Test initialization
        with Schema__Taxonomy(taxonomy_id   = Taxonomy_Id('test'),
                              root_category = Category_Id('root')) as _:
            assert type(_)            is Schema__Taxonomy
            assert isinstance(_, Type_Safe)
            assert str(_.taxonomy_id) == 'test'
            assert str(_.version)     == '1.0.0'

    def test__init__types(self):                                                     # Test attribute types
        with Schema__Taxonomy(taxonomy_id   = Taxonomy_Id('test'),
                              root_category = Category_Id('root')) as _:
            assert type(_.taxonomy_id)   is Taxonomy_Id
            assert type(_.version)       is Safe_Str__Version
            assert type(_.description)   is Safe_Str__Text
            assert type(_.root_category) is Category_Id
            assert type(_.categories)    is Dict__Categories__By_Id

    def test__init__default_values(self):                                            # Test default values
        with Schema__Taxonomy(taxonomy_id   = Taxonomy_Id('test'),
                              root_category = Category_Id('root')) as _:
            assert str(_.version)     == '1.0.0'
            assert str(_.description) == ''
            assert len(_.categories)  == 0

    def test__init__with_categories(self):                                           # Test with categories
        root_cat = Schema__Taxonomy__Category(category_id = Category_Id('root'),
                                              name        = 'root'             ,
                                              parent_ref  = Category_Id('')    ,
                                              child_refs  = []                 )

        with Schema__Taxonomy(taxonomy_id   = Taxonomy_Id('test'),
                              root_category = Category_Id('root'),
                              categories    = {'root': root_cat}) as _:
            assert len(_.categories) == 1
            assert 'root' in _.categories
            assert _.categories['root'] is root_cat

    def test__pure_data_no_methods(self):                                            # Verify no taxonomy operation methods
        with Schema__Taxonomy(taxonomy_id   = Taxonomy_Id('test'),
                              root_category = Category_Id('root')) as _:
            # These methods should NOT exist on the schema (moved to Utils)
            assert not hasattr(_, 'get_category')   or not callable(getattr(_, 'get_category', None))
            assert not hasattr(_, 'get_root')       or not callable(getattr(_, 'get_root', None))
            assert not hasattr(_, 'get_children')   or not callable(getattr(_, 'get_children', None))
            assert not hasattr(_, 'get_parent')     or not callable(getattr(_, 'get_parent', None))
            assert not hasattr(_, 'get_ancestors')  or not callable(getattr(_, 'get_ancestors', None))
            assert not hasattr(_, 'get_descendants') or not callable(getattr(_, 'get_descendants', None))

    def test__json_serialization(self):                                              # Test JSON round-trip
        original = Schema__Taxonomy(taxonomy_id   = Taxonomy_Id('test_taxonomy'),
                                    version       = '2.0.0'                    ,
                                    description   = 'Test taxonomy'            ,
                                    root_category = Category_Id('root')        )

        json_data = original.json()
        restored  = Schema__Taxonomy.from_json(json_data)

        assert str(restored.taxonomy_id)   == str(original.taxonomy_id)
        assert str(restored.version)       == str(original.version)
        assert str(restored.description)   == str(original.description)
        assert str(restored.root_category) == str(original.root_category)