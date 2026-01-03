# ═══════════════════════════════════════════════════════════════════════════════
# Test Dict__Categories__By_Id - Tests for category dictionary typed collection
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                            import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id      import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                  import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category     import Schema__Taxonomy__Category
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                    import Type_Safe__Dict


class test_Dict__Categories__By_Id(TestCase):                                            # Test category dictionary collection

    def test__init__(self):                                                              # Test initialization
        with Dict__Categories__By_Id() as _:
            assert type(_)              is Dict__Categories__By_Id
            assert isinstance(_, Type_Safe__Dict)
            assert _.expected_key_type   is Category_Id
            assert _.expected_value_type is Schema__Taxonomy__Category
            assert len(_)               == 0

    def test__add_and_retrieve(self):                                                    # Test adding and retrieving categories
        with Dict__Categories__By_Id() as _:
            cat_id   = Category_Id('test_category')
            category = Schema__Taxonomy__Category(category_id = cat_id          ,
                                                  name        = 'test_category' ,
                                                  parent_ref  = Category_Id(''),
                                                  child_refs  = []              )
            _[cat_id] = category

            assert len(_)         == 1
            assert _[cat_id]      is category
            assert _.get(cat_id)  is category

    def test__multiple_categories(self):                                                 # Test multiple category operations
        with Dict__Categories__By_Id() as _:
            cat1_id = Category_Id('cat_1')
            cat2_id = Category_Id('cat_2')
            cat1    = Schema__Taxonomy__Category(category_id=cat1_id, name='cat_1',
                                                 parent_ref=Category_Id(''), child_refs=[])
            cat2    = Schema__Taxonomy__Category(category_id=cat2_id, name='cat_2',
                                                 parent_ref=Category_Id('cat_1'), child_refs=[])

            _[cat1_id] = cat1
            _[cat2_id] = cat2

            assert len(_)     == 2
            assert _[cat1_id] is cat1
            assert _[cat2_id] is cat2