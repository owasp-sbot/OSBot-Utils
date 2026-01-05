# ═══════════════════════════════════════════════════════════════════════════════
# Test Dict__Taxonomies__By_Id - Tests for taxonomy dictionary typed collection
#
# Updated for Brief 3.8:
#   - Taxonomy_Id is Obj_Id-based
#   - root_category → root_id (Category_Id)
#   - Dict__Categories__By_Ref → Dict__Categories__By_Id
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Categories__By_Id  import Dict__Categories__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Taxonomies__By_Id  import Dict__Taxonomies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id              import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id              import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref             import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy           import Schema__Taxonomy
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class test_Dict__Taxonomies__By_Id(TestCase):                                        # Test taxonomy dictionary collection

    def test__init__(self):                                                          # Test initialization
        with Dict__Taxonomies__By_Id() as _:
            assert type(_)               is Dict__Taxonomies__By_Id
            assert isinstance(_, Type_Safe__Dict)
            assert _.expected_key_type   is Taxonomy_Id
            assert _.expected_value_type is Schema__Taxonomy
            assert len(_)                == 0

    def test__add_and_retrieve(self):                                                # Test adding and retrieving taxonomies
        with Dict__Taxonomies__By_Id() as _:
            tax_id   = Taxonomy_Id(Obj_Id.from_seed('test:tax:test'))
            root_id  = Category_Id(Obj_Id.from_seed('test:cat:root'))
            taxonomy = Schema__Taxonomy(taxonomy_id  = tax_id                        ,
                                        taxonomy_ref = Taxonomy_Ref('test_taxonomy') ,
                                        root_id      = root_id                       ,
                                        categories   = Dict__Categories__By_Id()     )
            _[tax_id] = taxonomy

            assert len(_)        == 1
            assert _[tax_id]     is taxonomy
            assert _.get(tax_id) is taxonomy

    def test__multiple_taxonomies(self):                                             # Test multiple taxonomy operations
        with Dict__Taxonomies__By_Id() as _:
            tax1_id  = Taxonomy_Id(Obj_Id.from_seed('test:tax:tax1'))
            tax2_id  = Taxonomy_Id(Obj_Id.from_seed('test:tax:tax2'))
            root1_id = Category_Id(Obj_Id.from_seed('test:cat:root1'))
            root2_id = Category_Id(Obj_Id.from_seed('test:cat:root2'))
            tax1     = Schema__Taxonomy(taxonomy_id  = tax1_id                       ,
                                        taxonomy_ref = Taxonomy_Ref('tax_1')         ,
                                        root_id      = root1_id                      ,
                                        categories   = Dict__Categories__By_Id()     )
            tax2     = Schema__Taxonomy(taxonomy_id  = tax2_id                       ,
                                        taxonomy_ref = Taxonomy_Ref('tax_2')         ,
                                        root_id      = root2_id                      ,
                                        categories   = Dict__Categories__By_Id()     )

            _[tax1_id] = tax1
            _[tax2_id] = tax2

            assert len(_)     == 2
            assert _[tax1_id] is tax1
            assert _[tax2_id] is tax2

    def test__iteration(self):                                                       # Test iteration over taxonomies
        with Dict__Taxonomies__By_Id() as _:
            tax1_id  = Taxonomy_Id(Obj_Id.from_seed('test:tax:iter1'))
            tax2_id  = Taxonomy_Id(Obj_Id.from_seed('test:tax:iter2'))
            root1_id = Category_Id(Obj_Id.from_seed('test:cat:iter_root1'))
            root2_id = Category_Id(Obj_Id.from_seed('test:cat:iter_root2'))
            tax1     = Schema__Taxonomy(taxonomy_id  = tax1_id                       ,
                                        taxonomy_ref = Taxonomy_Ref('tax_1')         ,
                                        root_id      = root1_id                      ,
                                        categories   = Dict__Categories__By_Id()     )
            tax2     = Schema__Taxonomy(taxonomy_id  = tax2_id                       ,
                                        taxonomy_ref = Taxonomy_Ref('tax_2')         ,
                                        root_id      = root2_id                      ,
                                        categories   = Dict__Categories__By_Id()     )

            _[tax1_id] = tax1
            _[tax2_id] = tax2

            keys   = list(_.keys())
            values = list(_.values())
            items  = list(_.items())

            assert len(keys)   == 2
            assert len(values) == 2
            assert len(items)  == 2