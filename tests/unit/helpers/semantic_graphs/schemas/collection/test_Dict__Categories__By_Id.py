# ═══════════════════════════════════════════════════════════════════════════════
# Test Dict__Categories__By_Id - Tests for category dictionary typed collection
#
# Updated for Brief 3.7:
#   - Category_Id is now Obj_Id-based
#   - Schema__Taxonomy__Category uses category_ref for human-readable name
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                            import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id      import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Refs          import List__Category_Refs
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                  import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                 import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category     import Schema__Taxonomy__Category
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id          import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text             import Safe_Str__Text
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                    import Type_Safe__Dict


class test_Dict__Categories__By_Id(TestCase):                                            # Test category dictionary collection

    def test__init__(self):                                                              # Test initialization
        with Dict__Categories__By_Id() as _:
            assert type(_)               is Dict__Categories__By_Id
            assert isinstance(_, Type_Safe__Dict)
            assert _.expected_key_type   is Category_Id
            assert _.expected_value_type is Schema__Taxonomy__Category
            assert len(_)                == 0

    def test__add_and_retrieve(self):                                                    # Test adding and retrieving categories
        with Dict__Categories__By_Id() as _:
            cat_id   = Category_Id(Obj_Id.from_seed('test:cat:test'))
            category = Schema__Taxonomy__Category(category_ref = Category_Ref('test_category'),
                                                  name         = Safe_Str__Id('test_category'),
                                                  description  = Safe_Str__Text('')           ,
                                                  parent_ref   = Category_Ref('')             ,
                                                  child_refs   = List__Category_Refs()        )
            _[cat_id] = category

            assert len(_)        == 1
            assert _[cat_id]     is category
            assert _.get(cat_id) is category

    def test__multiple_categories(self):                                                 # Test multiple category operations
        with Dict__Categories__By_Id() as _:
            cat1_id = Category_Id(Obj_Id.from_seed('test:cat:cat1'))
            cat2_id = Category_Id(Obj_Id.from_seed('test:cat:cat2'))
            cat1    = Schema__Taxonomy__Category(category_ref = Category_Ref('cat_1')        ,
                                                 name         = Safe_Str__Id('cat_1')        ,
                                                 description  = Safe_Str__Text('')           ,
                                                 parent_ref   = Category_Ref('')             ,
                                                 child_refs   = List__Category_Refs()        )
            cat2    = Schema__Taxonomy__Category(category_ref = Category_Ref('cat_2')        ,
                                                 name         = Safe_Str__Id('cat_2')        ,
                                                 description  = Safe_Str__Text('')           ,
                                                 parent_ref   = Category_Ref('cat_1')        ,
                                                 child_refs   = List__Category_Refs()        )

            _[cat1_id] = cat1
            _[cat2_id] = cat2

            assert len(_)     == 2
            assert _[cat1_id] is cat1
            assert _[cat2_id] is cat2

    def test__iteration(self):                                                           # Test iteration over categories
        with Dict__Categories__By_Id() as _:
            cat1_id = Category_Id(Obj_Id.from_seed('test:cat:iter1'))
            cat2_id = Category_Id(Obj_Id.from_seed('test:cat:iter2'))
            cat1    = Schema__Taxonomy__Category(category_ref = Category_Ref('iter_1')       ,
                                                 name         = Safe_Str__Id('iter_1')       ,
                                                 description  = Safe_Str__Text('')           ,
                                                 parent_ref   = Category_Ref('')             ,
                                                 child_refs   = List__Category_Refs()        )
            cat2    = Schema__Taxonomy__Category(category_ref = Category_Ref('iter_2')       ,
                                                 name         = Safe_Str__Id('iter_2')       ,
                                                 description  = Safe_Str__Text('')           ,
                                                 parent_ref   = Category_Ref('')             ,
                                                 child_refs   = List__Category_Refs()        )

            _[cat1_id] = cat1
            _[cat2_id] = cat2

            keys   = list(_.keys())
            values = list(_.values())
            items  = list(_.items())

            assert len(keys)   == 2
            assert len(values) == 2
            assert len(items)  == 2