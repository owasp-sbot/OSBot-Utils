# ═══════════════════════════════════════════════════════════════════════════════
# Test List__Category_Ids - Tests for category ID list typed collection
#
# Updated for Brief 3.7:
#   - Category_Id is now Obj_Id-based (not string)
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Ids      import List__Category_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id             import Category_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List               import Type_Safe__List


class test_List__Category_Ids(TestCase):                                             # Test category ID list collection

    def test__init__(self):                                                          # Test initialization
        with List__Category_Ids() as _:
            assert type(_)         is List__Category_Ids
            assert isinstance(_, Type_Safe__List)
            assert _.expected_type is Category_Id
            assert len(_)          == 0

    def test__append_and_retrieve(self):                                             # Test appending and retrieving IDs
        with List__Category_Ids() as _:
            cat_id = Category_Id(Obj_Id.from_seed('test:cat:test'))
            _.append(cat_id)

            assert len(_) == 1
            assert _[0]   == cat_id

    def test__multiple_ids(self):                                                    # Test multiple ID operations
        with List__Category_Ids() as _:
            cat1 = Category_Id(Obj_Id.from_seed('test:cat:cat1'))
            cat2 = Category_Id(Obj_Id.from_seed('test:cat:cat2'))
            cat3 = Category_Id(Obj_Id.from_seed('test:cat:cat3'))

            _.append(cat1)
            _.append(cat2)
            _.append(cat3)

            assert len(_) == 3
            assert _[0]   == cat1
            assert _[1]   == cat2
            assert _[2]   == cat3

    def test__extend(self):                                                          # Test extend operation
        with List__Category_Ids() as _:
            ids = [Category_Id(Obj_Id.from_seed('test:cat:ext1')),
                   Category_Id(Obj_Id.from_seed('test:cat:ext2'))]
            _.extend(ids)

            assert len(_) == 2

    def test__contains(self):                                                        # Test membership check
        with List__Category_Ids() as _:
            cat1 = Category_Id(Obj_Id.from_seed('test:cat:in1'))
            cat2 = Category_Id(Obj_Id.from_seed('test:cat:in2'))
            _.append(cat1)

            assert cat1 in _
            assert cat2 not in _

    def test__iteration(self):                                                       # Test iteration
        with List__Category_Ids() as _:
            ids = [Category_Id(Obj_Id.from_seed('test:cat:iter1')),
                   Category_Id(Obj_Id.from_seed('test:cat:iter2')),
                   Category_Id(Obj_Id.from_seed('test:cat:iter3'))]
            _.extend(ids)

            result = list(_)
            assert len(result) == 3