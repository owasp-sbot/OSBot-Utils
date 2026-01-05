# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Taxonomy - Tests for taxonomy schema (pure data)
# Note: Taxonomy operations have been moved to Taxonomy__Utils
#
# Updated for Brief 3.7:
#   - taxonomy_id is Obj_Id-based
#   - Added taxonomy_ref for human-readable name
#   - root_category uses Category_Ref (not Category_Id)
#   - categories dict keyed by Category_Ref (Dict__Categories__By_Ref)
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Ref    import Dict__Categories__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Refs         import List__Category_Refs
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                 import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref                import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category    import Schema__Taxonomy__Category
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text            import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version         import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id         import Safe_Str__Id
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe


class test_Schema__Taxonomy(TestCase):                                                  # Test taxonomy schema

    def test__init__(self):                                                             # Test initialization
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        with Schema__Taxonomy(taxonomy_id   = taxonomy_id               ,
                              taxonomy_ref  = Taxonomy_Ref('test')      ,
                              root_category = Category_Ref('root')      ) as _:
            assert type(_)           is Schema__Taxonomy
            assert isinstance(_, Type_Safe)
            assert _.taxonomy_id     == taxonomy_id
            assert str(_.taxonomy_ref) == 'test'

    def test__init__types(self):                                                        # Test attribute types
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        with Schema__Taxonomy(taxonomy_id   = taxonomy_id               ,
                              taxonomy_ref  = Taxonomy_Ref('test')      ,
                              root_category = Category_Ref('root')      ) as _:
            assert type(_.taxonomy_id)   is Taxonomy_Id
            assert type(_.taxonomy_ref)  is Taxonomy_Ref
            assert type(_.version)       is Safe_Str__Version
            assert type(_.description)   is Safe_Str__Text
            assert type(_.root_category) is Category_Ref
            assert type(_.categories)    is Dict__Categories__By_Ref

    def test__init__default_values(self):                                               # Test default values
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        with Schema__Taxonomy(taxonomy_id   = taxonomy_id               ,
                              taxonomy_ref  = Taxonomy_Ref('test')      ,
                              root_category = Category_Ref('root')      ) as _:
            assert str(_.version)     == '1.0.0'
            assert str(_.description) == ''
            assert len(_.categories)  == 0

    def test__init__with_categories(self):                                              # Test with categories
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        root_cat    = Schema__Taxonomy__Category(category_ref = Category_Ref('root')    ,
                                                 name         = Safe_Str__Id('root')    ,
                                                 description  = Safe_Str__Text('')      ,
                                                 parent_ref   = Category_Ref('')        ,
                                                 child_refs   = List__Category_Refs()   )

        categories = Dict__Categories__By_Ref()
        categories[Category_Ref('root')] = root_cat

        with Schema__Taxonomy(taxonomy_id   = taxonomy_id               ,
                              taxonomy_ref  = Taxonomy_Ref('test')      ,
                              root_category = Category_Ref('root')      ,
                              categories    = categories                ) as _:
            assert len(_.categories)                 == 1
            assert Category_Ref('root')              in _.categories
            assert _.categories[Category_Ref('root')] is root_cat

    def test__pure_data_no_methods(self):                                               # Verify no taxonomy operation methods
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        with Schema__Taxonomy(taxonomy_id   = taxonomy_id               ,
                              taxonomy_ref  = Taxonomy_Ref('test')      ,
                              root_category = Category_Ref('root')      ) as _:
            # These methods should NOT exist on the schema (moved to Utils)
            assert not hasattr(_, 'get_category')    or not callable(getattr(_, 'get_category', None))
            assert not hasattr(_, 'get_root')        or not callable(getattr(_, 'get_root', None))
            assert not hasattr(_, 'get_children')    or not callable(getattr(_, 'get_children', None))
            assert not hasattr(_, 'get_parent')      or not callable(getattr(_, 'get_parent', None))
            assert not hasattr(_, 'get_ancestors')   or not callable(getattr(_, 'get_ancestors', None))
            assert not hasattr(_, 'get_descendants') or not callable(getattr(_, 'get_descendants', None))

    def test__json_serialization(self):                                                 # Test JSON round-trip
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy:serial'))
        original    = Schema__Taxonomy(taxonomy_id   = taxonomy_id                      ,
                                       taxonomy_ref  = Taxonomy_Ref('test_taxonomy')    ,
                                       version       = Safe_Str__Version('2.0.0')       ,
                                       description   = Safe_Str__Text('Test taxonomy')  ,
                                       root_category = Category_Ref('root')             )

        json_data = original.json()
        restored  = Schema__Taxonomy.from_json(json_data)

        assert str(restored.taxonomy_id)   == str(original.taxonomy_id)
        assert str(restored.taxonomy_ref)  == str(original.taxonomy_ref)
        assert str(restored.version)       == str(original.version)
        assert str(restored.description)   == str(original.description)
        assert str(restored.root_category) == str(original.root_category)