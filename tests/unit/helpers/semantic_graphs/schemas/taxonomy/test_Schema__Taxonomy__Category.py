# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Taxonomy__Category - Tests for taxonomy category schema
#
# Updated for Brief 3.7:
#   - category_id → category_ref (ref is primary identifier)
#   - name uses Safe_Str__Id type
#   - description uses Safe_Str__Text type
#   - parent_ref uses Category_Ref type
#   - child_refs uses List__Category_Refs type
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Refs         import List__Category_Refs
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category    import Schema__Taxonomy__Category
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text            import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id         import Safe_Str__Id


class test_Schema__Taxonomy__Category(TestCase):                                        # Test category schema

    def test__init__(self):                                                             # Test initialization with defaults
        with Schema__Taxonomy__Category() as _:
            assert type(_.category_ref) is Category_Ref
            assert str(_.category_ref)  == ''
            assert str(_.name)          == ''
            assert str(_.description)   == ''
            assert str(_.parent_ref)    == ''
            assert type(_.child_refs)   is List__Category_Refs
            assert len(_.child_refs)    == 0

    def test__init__types(self):                                                        # Test attribute types
        with Schema__Taxonomy__Category(category_ref = Category_Ref('test')        ,
                                        name         = Safe_Str__Id('test')        ,
                                        description  = Safe_Str__Text('A test')    ,
                                        parent_ref   = Category_Ref('')            ,
                                        child_refs   = List__Category_Refs()       ) as _:
            assert type(_.category_ref) is Category_Ref
            assert type(_.name)         is Safe_Str__Id
            assert type(_.description)  is Safe_Str__Text
            assert type(_.parent_ref)   is Category_Ref
            assert type(_.child_refs)   is List__Category_Refs

    def test__with_values(self):                                                        # Test with explicit values
        child_refs = List__Category_Refs()
        child_refs.append(Category_Ref('class_unit'))

        with Schema__Taxonomy__Category(category_ref = Category_Ref('code_unit')              ,
                                        name         = Safe_Str__Id('code_unit')              ,
                                        description  = Safe_Str__Text('Executable code units'),
                                        parent_ref   = Category_Ref('code_element')           ,
                                        child_refs   = child_refs                             ) as _:
            assert str(_.category_ref) == 'code_unit'
            assert str(_.name)         == 'code_unit'
            assert str(_.description)  == 'Executable code units'
            assert str(_.parent_ref)   == 'code_element'
            assert len(_.child_refs)   == 1
            assert str(_.child_refs[0]) == 'class_unit'

    def test__with_multiple_children(self):                                             # Test with multiple children
        child_refs = List__Category_Refs()
        child_refs.append(Category_Ref('container'))
        child_refs.append(Category_Ref('code_unit'))
        child_refs.append(Category_Ref('callable'))

        with Schema__Taxonomy__Category(category_ref = Category_Ref('code_element')           ,
                                        name         = Safe_Str__Id('code_element')           ,
                                        description  = Safe_Str__Text('Root element')         ,
                                        parent_ref   = Category_Ref('')                       ,
                                        child_refs   = child_refs                             ) as _:
            assert len(_.child_refs) == 3
            assert Category_Ref('container') in _.child_refs
            assert Category_Ref('code_unit') in _.child_refs
            assert Category_Ref('callable')  in _.child_refs

    def test__json_serialization(self):                                                 # Test JSON round-trip
        child_refs = List__Category_Refs()
        child_refs.append(Category_Ref('child1'))
        child_refs.append(Category_Ref('child2'))

        original = Schema__Taxonomy__Category(category_ref = Category_Ref('parent')           ,
                                              name         = Safe_Str__Id('parent')           ,
                                              description  = Safe_Str__Text('Parent category'),
                                              parent_ref   = Category_Ref('root')             ,
                                              child_refs   = child_refs                       )

        json_data = original.json()
        restored  = Schema__Taxonomy__Category.from_json(json_data)

        assert str(restored.category_ref) == str(original.category_ref)
        assert str(restored.name)         == str(original.name)
        assert str(restored.description)  == str(original.description)
        assert str(restored.parent_ref)   == str(original.parent_ref)
        assert len(restored.child_refs)   == len(original.child_refs)