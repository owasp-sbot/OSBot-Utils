# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Taxonomy - Tests for taxonomy schema (pure data)
# Note: Taxonomy operations have been moved to Taxonomy__Utils
#
# Updated for Brief 3.8:
#   - root_category (Category_Ref) → root_id (Category_Id)
#   - Dict__Categories__By_Ref → Dict__Categories__By_Id
#   - Categories use ID-based parent/child references
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id     import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Ids          import List__Category_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                 import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                 import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref                import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category    import Schema__Taxonomy__Category
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text            import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version         import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe


class test_Schema__Taxonomy(TestCase):                                                  # Test taxonomy schema

    def test__init__(self):                                                             # Test initialization
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        root_id     = Category_Id(Obj_Id.from_seed('test:cat:root'))
        with Schema__Taxonomy(taxonomy_id  = taxonomy_id               ,
                              taxonomy_ref = Taxonomy_Ref('test')      ,
                              root_id      = root_id                   ) as _:
            assert type(_)           is Schema__Taxonomy
            assert isinstance(_, Type_Safe)
            assert _.taxonomy_id     == taxonomy_id
            assert str(_.taxonomy_ref) == 'test'
            assert _.root_id         == root_id                                         # Brief 3.8

    def test__init__types(self):                                                        # Test attribute types
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        root_id     = Category_Id(Obj_Id.from_seed('test:cat:root'))
        with Schema__Taxonomy(taxonomy_id  = taxonomy_id               ,
                              taxonomy_ref = Taxonomy_Ref('test')      ,
                              root_id      = root_id                   ) as _:
            assert type(_.taxonomy_id)  is Taxonomy_Id
            assert type(_.taxonomy_ref) is Taxonomy_Ref
            assert type(_.version)      is Safe_Str__Version
            assert type(_.root_id)      is Category_Id                                  # Brief 3.8
            assert type(_.categories)   is Dict__Categories__By_Id                      # Brief 3.8

    def test__init__default_values(self):                                               # Test default values
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        root_id     = Category_Id(Obj_Id.from_seed('test:cat:root'))
        with Schema__Taxonomy(taxonomy_id  = taxonomy_id               ,
                              taxonomy_ref = Taxonomy_Ref('test')      ,
                              root_id      = root_id                   ) as _:
            assert str(_.version)    == '1.0.0'
            assert len(_.categories) == 0

    def test__init__with_categories(self):                                              # Test with categories
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        root_id     = Category_Id(Obj_Id.from_seed('test:cat:root'))

        root_cat = Schema__Taxonomy__Category(category_id  = root_id                    ,
                                              category_ref = Category_Ref('root')       ,
                                              parent_id    = None                       ,
                                              child_ids    = List__Category_Ids()       )

        categories = Dict__Categories__By_Id()
        categories[root_id] = root_cat

        with Schema__Taxonomy(taxonomy_id  = taxonomy_id               ,
                              taxonomy_ref = Taxonomy_Ref('test')      ,
                              root_id      = root_id                   ,
                              categories   = categories                ) as _:
            assert len(_.categories)    == 1
            assert root_id              in _.categories
            assert _.categories[root_id] is root_cat

    def test__init__with_hierarchy(self):                                               # Test with category hierarchy
        taxonomy_id  = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        root_id      = Category_Id(Obj_Id.from_seed('test:cat:root'))
        child1_id    = Category_Id(Obj_Id.from_seed('test:cat:child1'))
        child2_id    = Category_Id(Obj_Id.from_seed('test:cat:child2'))

        root_cat = Schema__Taxonomy__Category(category_id  = root_id                          ,
                                              category_ref = Category_Ref('root')             ,
                                              parent_id    = None                             ,
                                              child_ids    = List__Category_Ids([child1_id, child2_id]))

        child1_cat = Schema__Taxonomy__Category(category_id  = child1_id                      ,
                                                category_ref = Category_Ref('child1')         ,
                                                parent_id    = root_id                        ,
                                                child_ids    = List__Category_Ids()           )

        child2_cat = Schema__Taxonomy__Category(category_id  = child2_id                      ,
                                                category_ref = Category_Ref('child2')         ,
                                                parent_id    = root_id                        ,
                                                child_ids    = List__Category_Ids()           )

        categories = Dict__Categories__By_Id()
        categories[root_id]   = root_cat
        categories[child1_id] = child1_cat
        categories[child2_id] = child2_cat

        with Schema__Taxonomy(taxonomy_id  = taxonomy_id               ,
                              taxonomy_ref = Taxonomy_Ref('test')      ,
                              root_id      = root_id                   ,
                              categories   = categories                ) as _:
            assert len(_.categories) == 3
            assert _.categories[root_id].parent_id is None
            assert _.categories[child1_id].parent_id == root_id
            assert _.categories[child2_id].parent_id == root_id
            assert len(_.categories[root_id].child_ids) == 2

    def test__pure_data_no_methods(self):                                               # Verify no taxonomy operation methods
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy'))
        root_id     = Category_Id(Obj_Id.from_seed('test:cat:root'))
        with Schema__Taxonomy(taxonomy_id  = taxonomy_id               ,
                              taxonomy_ref = Taxonomy_Ref('test')      ,
                              root_id      = root_id                   ) as _:
            # These methods should NOT exist on the schema (moved to Utils)
            assert not hasattr(_, 'get_category')    or not callable(getattr(_, 'get_category', None))
            assert not hasattr(_, 'get_root')        or not callable(getattr(_, 'get_root', None))
            assert not hasattr(_, 'get_children')    or not callable(getattr(_, 'get_children', None))
            assert not hasattr(_, 'get_parent')      or not callable(getattr(_, 'get_parent', None))
            assert not hasattr(_, 'get_ancestors')   or not callable(getattr(_, 'get_ancestors', None))
            assert not hasattr(_, 'get_descendants') or not callable(getattr(_, 'get_descendants', None))

    def test__json_serialization(self):                                                 # Test JSON round-trip
        taxonomy_id = Taxonomy_Id(Obj_Id.from_seed('test:taxonomy:serial'))
        root_id     = Category_Id(Obj_Id.from_seed('test:cat:root'))
        original    = Schema__Taxonomy(taxonomy_id  = taxonomy_id                      ,
                                       taxonomy_ref = Taxonomy_Ref('test_taxonomy')    ,
                                       version      = Safe_Str__Version('2.0.0')       ,
                                       root_id      = root_id                          )

        json_data = original.json()
        restored  = Schema__Taxonomy.from_json(json_data)

        assert str(restored.taxonomy_id)  == str(original.taxonomy_id)
        assert str(restored.taxonomy_ref) == str(original.taxonomy_ref)
        assert str(restored.version)      == str(original.version)
        assert str(restored.root_id)      == str(original.root_id)                      # Brief 3.8