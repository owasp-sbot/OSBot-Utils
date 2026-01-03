# ═══════════════════════════════════════════════════════════════════════════════
# Test Dict__Taxonomies__By_Id - Tests for taxonomy dictionary typed collection
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Taxonomies__By_Id  import Dict__Taxonomies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id              import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id              import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy           import Schema__Taxonomy
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class test_Dict__Taxonomies__By_Id(TestCase):                                        # Test taxonomy dictionary collection

    def test__init__(self):                                                          # Test initialization
        with Dict__Taxonomies__By_Id() as _:
            assert type(_)              is Dict__Taxonomies__By_Id
            assert isinstance(_, Type_Safe__Dict)
            assert _.expected_key_type   is Taxonomy_Id
            assert _.expected_value_type is Schema__Taxonomy
            assert len(_)               == 0

    def test__add_and_retrieve(self):                                                # Test adding and retrieving taxonomies
        with Dict__Taxonomies__By_Id() as _:
            tax_id   = Taxonomy_Id('test_taxonomy')
            taxonomy = Schema__Taxonomy(taxonomy_id   = tax_id                ,
                                        root_category = Category_Id('root')   ,
                                        categories    = {}                    )
            _[tax_id] = taxonomy

            assert len(_)         == 1
            assert _[tax_id]      is taxonomy
            assert _.get(tax_id)  is taxonomy

    def test__multiple_taxonomies(self):                                             # Test multiple taxonomy operations
        with Dict__Taxonomies__By_Id() as _:
            tax1_id = Taxonomy_Id('tax_1')
            tax2_id = Taxonomy_Id('tax_2')
            tax1    = Schema__Taxonomy(taxonomy_id=tax1_id, root_category=Category_Id('root1'), categories={})
            tax2    = Schema__Taxonomy(taxonomy_id=tax2_id, root_category=Category_Id('root2'), categories={})

            _[tax1_id] = tax1
            _[tax2_id] = tax2

            assert len(_)     == 2
            assert _[tax1_id] is tax1
            assert _[tax2_id] is tax2