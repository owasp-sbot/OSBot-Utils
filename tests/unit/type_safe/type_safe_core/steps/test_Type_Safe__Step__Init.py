import re
import pytest
from typing                                                                         import Dict, List, Set, Tuple
from unittest                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path   import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                   import Safe_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List               import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set                import Type_Safe__Set
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Tuple              import Type_Safe__Tuple
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Class_Kwargs       import Type_Safe__Step__Class_Kwargs
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Init               import Type_Safe__Step__Init


class test_Type_Safe__Step__Init(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.step_class_kwargs = Type_Safe__Step__Class_Kwargs()
        cls.step_init         = Type_Safe__Step__Init        ()

    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=60)
    def test_init__class__empty(self):
        class Class__Empty: pass
        empty_class = Class__Empty()
        class_kwargs = {}
        kwargs       = {}
        self.step_init.init(empty_class, class_kwargs, **kwargs)
        assert empty_class.__dict__ == {}

    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=80)
    def test_init__class_one_int__no_kwargs(self):
        class Class__One_int:
            an_int: int

        one_int = Class__One_int()
        class_kwargs = {'an_int': 0}
        kwargs       = {}
        self.step_init.init(one_int, class_kwargs, **kwargs)
        assert one_int.__dict__ == {'an_int': 0}
        assert one_int.an_int   == 0

    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=80)
    def test_init__class_one_int__with_value__no_kwargs(self):
        class Class__One_int:
            an_int: int

        one_int = Class__One_int()
        one_int.an_int = 42
        class_kwargs = {'an_int': 0}
        kwargs       = {}
        self.step_init.init(one_int, class_kwargs, **kwargs)
        assert one_int.__dict__ == {'an_int': 42}
        assert one_int.an_int   == 42

    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=80)
    def test_init__class_one_int__no_value__no_kwargs(self):
        class Class__One_int:
            pass

        one_int = Class__One_int()

        class_kwargs = {'an_int': 0}
        kwargs       = {}
        self.step_init.init(one_int, class_kwargs, **kwargs)
        assert one_int.__dict__ == {'an_int': 0}
        assert one_int.an_int   == 0

    #@trace_calls(include=['*'], show_internals=True, show_duration=True, duration_padding=80)
    def test_init__class_one_int__with_kwargs(self):
        class Class__One_int:
            an_int: int
        one_int      = Class__One_int()
        class_kwargs = {'an_int': 0 }
        kwargs       = {'an_int': 42}
        self.step_init.init(one_int, class_kwargs, **kwargs)
        assert one_int.__dict__ == {'an_int': 42}
        assert one_int.an_int   == 42


    def test_init__type_safe__class_one_int__no_kwargs(self):
        class Class__One_int(Type_Safe):
            an_int: int

        one_int = Class__One_int()
        assert one_int.an_int == 0

    def test__dict_with_list_values__on_ctor(self):                           # Test the fix for Dict[K, List[V]] in constructor
        class An_Class_1(Type_Safe):
            all_paths: Dict[Safe_Id, List[Safe_Str__File__Path]]

        data = { 'by_hash': [ 'refs/by-hash/e1/5b/e15b31f87df1896e.json'        ,
                              'refs/by-hash/e1/5b/e15b31f87df1896e.json.config' ,
                              'refs/by-hash/e1/5b/e15b31f87df1896e.json.metadata'],
                 'by_id'  : [ 'refs/by-id/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json'        ,
                              'refs/by-id/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.config' ,
                              'refs/by-id/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.metadata'],
                 'data'   : [ 'data/direct/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json'        ,
                              'data/direct/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.config' ,
                              'data/direct/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.metadata']}

        an_class = An_Class_1(all_paths=data)

        # Verify the structure
        assert type(an_class.all_paths)             is Type_Safe__Dict
        assert type(an_class.all_paths['by_hash'])  is Type_Safe__List
        assert len(an_class.all_paths['by_hash'])   == 3

        # Verify Safe type conversion happened
        for path in an_class.all_paths['by_hash']:
            assert type(path) is Safe_Str__File__Path

        # Verify round-trip
        assert an_class.json() == {"all_paths": data}

    def test__dict_with_nested_list__various_types(self):                              # Test Dict with various nested List types
        class Schema__Complex(Type_Safe):
            str_lists   : Dict[str, List[str]]
            int_lists   : Dict[str, List[int]]
            safe_lists  : Dict[Safe_Id, List[Safe_Id]]

        data = {'str_lists' : {'group1': ['a', 'b'], 'group2': ['c']},
                'int_lists' : {'nums': [1, 2, 3], 'more': [4, 5]},
                'safe_lists': {'ids': ['id1', 'id2'], 'refs': ['ref1']}}

        schema = Schema__Complex(**data)

        # Check all conversions
        assert type(schema.str_lists)          is Type_Safe__Dict
        assert type(schema.str_lists['group1']) is Type_Safe__List
        assert schema.str_lists['group1']      == ['a', 'b']

        assert type(schema.int_lists['nums'])  is Type_Safe__List
        assert schema.int_lists['nums']        == [1, 2, 3]

        assert type(schema.safe_lists['ids'])  is Type_Safe__List
        assert type(schema.safe_lists['ids'][0]) is Safe_Id
        assert schema.safe_lists['ids'][0]     == 'id1'

    def test__dict_with_nested_set(self):                                              # Test Dict[K, Set[V]] handling
        class Schema__With_Sets(Type_Safe):
            unique_items: Dict[str, Set[int]]

        data = {'unique_items': {'set1': {1, 2, 2, 3}, 'set2': {4, 5}}}

        schema = Schema__With_Sets(**data)

        assert type(schema.unique_items)         is Type_Safe__Dict
        assert type(schema.unique_items['set1']) is Type_Safe__Set
        assert schema.unique_items['set1']       == {1, 2, 3}  # Duplicates removed

    def test__dict_with_nested_dict(self):                                             # Test Dict[K, Dict[K2, V]] handling
        class Schema__Nested_Dicts(Type_Safe):
            nested: Dict[str, Dict[str, int]]

        data = {'nested': {'outer1': {'inner1': 1, 'inner2': 2},
                          'outer2': {'inner3': 3}}}

        schema = Schema__Nested_Dicts(**data)

        assert type(schema.nested)             is Type_Safe__Dict
        assert type(schema.nested['outer1'])   is Type_Safe__Dict
        assert schema.nested['outer1']['inner1'] == 1

    # Test empty collection handling

    def test__empty_collections__become_type_safe_variants(self):                      # Test empty collections get proper Type_Safe variants
        class Schema__Collections(Type_Safe):
            items : List[str]
            data  : Dict[str, int]
            unique: Set[int]
            coords: Tuple[int, int]

        # Pass empty collections
        schema = Schema__Collections(items=[], data={}, unique=set(), coords=())

        # Verify they become Type_Safe variants
        assert type(schema.items)  is Type_Safe__List
        assert type(schema.data)   is Type_Safe__Dict
        assert type(schema.unique) is Type_Safe__Set
        assert type(schema.coords) is Type_Safe__Tuple

        # And are still empty
        assert schema.items  == []
        assert schema.data   == {}
        assert schema.unique == set()
        assert schema.coords == ()

    # Test non-empty collection handling

    def test__non_empty_list__conversion(self):                                        # Test non-empty list conversion
        class Schema__With_List(Type_Safe):
            items: List[Safe_Id]

        schema = Schema__With_List(items=['id1', 'id2', 'id3'])

        assert type(schema.items)    is Type_Safe__List
        assert len(schema.items)     == 3
        assert type(schema.items[0]) is Safe_Id
        assert schema.items[0]       == 'id1'

    def test__non_empty_set__conversion(self):                                         # Test non-empty set conversion
        class Schema__With_Set(Type_Safe):
            tags: Set[str]

        schema = Schema__With_Set(tags={'tag1', 'tag2', 'tag1'})  # Duplicate

        assert type(schema.tags) is Type_Safe__Set
        assert schema.tags       == {'tag1', 'tag2'}  # Duplicate removed

    def test__non_empty_tuple__conversion(self):                                       # Test non-empty tuple conversion
        class Schema__With_Tuple(Type_Safe):
            point: Tuple[int, int, str]

        schema = Schema__With_Tuple(point=(10, 20, 'label'))

        assert type(schema.point) is Type_Safe__Tuple
        assert schema.point       == (10, 20, 'label')

    def test__non_empty_dict__conversion(self):                                        # Test non-empty dict conversion
        class Schema__With_Dict(Type_Safe):
            mapping: Dict[Safe_Id, int]

        schema = Schema__With_Dict(mapping={'id1': 100, 'id2': 200})

        assert type(schema.mapping)       is Type_Safe__Dict
        assert type(list(schema.mapping.keys())[0]) is Safe_Id
        assert schema.mapping['id1']      == 100

    # Test enum conversion

    def test__enum_conversion_in_init(self):                                           # Test enum auto-conversion in __init__
        from enum import Enum

        class Status_Enum(str, Enum):
            PENDING = 'pending'
            ACTIVE  = 'active'

        class Schema__With_Enum(Type_Safe):
            status: Status_Enum = Status_Enum.PENDING

        # String should convert to enum
        schema = Schema__With_Enum(status='active')

        assert schema.status        == Status_Enum.ACTIVE
        assert type(schema.status)  is Status_Enum

        # Invalid value should raise
        error_message = "Invalid value 'invalid' for enum Status_Enum"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Schema__With_Enum(status='invalid')

    # Test forward reference handling

    def test__forward_ref_in_list(self):                                               # Test forward references in lists
        class Tree_Node(Type_Safe):
            value   : str
            children: List['Tree_Node']

        # Create nested structure
        schema = Tree_Node(value='root',
                           children=[{'value': 'child1', 'children': []},
                                     {'value': 'child2', 'children': []}])

        assert schema.value              == 'root'
        assert len(schema.children)      == 2
        assert type(schema.children)     is Type_Safe__List
        assert type(schema.children[0])  is Tree_Node
        assert schema.children[0].value  == 'child1'

    # Test error scenarios

    def test__invalid_attribute_error(self):                                           # Test error when setting non-existent attribute
        class Schema__Strict(Type_Safe):
            valid_field: str

        error_message = "Schema__Strict has no attribute 'invalid_field' and cannot be assigned the value 'test'. Use Schema__Strict.__default_kwargs__() see what attributes are available"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Schema__Strict(invalid_field='test')

    def test__none_values_dont_overwrite(self):                                        # Test None values don't overwrite existing values
        class Schema__With_Defaults(Type_Safe):
            field1: str = 'default1'
            field2: str = 'default2'

        # None should not overwrite
        schema = Schema__With_Defaults(field1='custom', field2=None)

        assert schema.field1 == 'custom'   # Set to custom value
        assert schema.field2 == 'default2' # None didn't overwrite default

    # Test complex nested scenarios

    def test__deeply_nested_collections(self):                                         # Test complex nested collection structures
        class Schema__Deep(Type_Safe):
            complex: Dict[str, List[Dict[str, Set[int]]]]

        data = {
            'complex': {
                'level1': [
                    {'set1': {1, 2, 3}, 'set2': {4, 5}},
                    {'set3': {6, 7}}
                ]
            }
        }

        schema = Schema__Deep(**data)

        assert type(schema.complex)                    is Type_Safe__Dict
        assert type(schema.complex['level1'])          is Type_Safe__List
        assert type(schema.complex['level1'][0])       is dict                          # Note: inner dict not converted
        assert schema.complex['level1'][0]['set1']     == {1, 2, 3}

    # Test convert_dict_with_nested_collections method directly

    def test__convert_dict_with_nested_collections__method(self):                      # Test the new method directly
        class Schema__Test(Type_Safe):
            data: Dict[str, List[str]]

        schema = Schema__Test()
        annotation = Dict[str, List[str]]
        value = {'key1': ['a', 'b'], 'key2': ['c']}

        result = self.step_init.convert_dict_with_nested_collections(schema, annotation, value)

        assert result is not None
        assert type(result)        is Type_Safe__Dict
        assert type(result['key1']) is Type_Safe__List
        assert result['key1']      == ['a', 'b']

    def test__convert_dict_with_nested_collections__returns_none_for_non_collections(self):
        class Schema__Test(Type_Safe):
            data: Dict[str, str]  # Not a nested collection

        schema = Schema__Test()
        annotation = Dict[str, str]
        value = {'key': 'value'}

        result = self.step_init.convert_dict_with_nested_collections(schema, annotation, value)

        assert result is None  # Should return None for non-collection values

    # Test Safe primitive conversions in nested structures

    def test__safe_primitives_in_dict_lists(self):                                     # Test Safe primitives get converted
        from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url import Safe_Str__Url

        class Schema__URLs(Type_Safe):
            urls_by_category: Dict[str, List[Safe_Str__Url]]

        data = {
            'urls_by_category': {
                'docs': ['https://docs.example.com', 'https://api.example.com'],
                'apis': ['https://api.example.com/v1']
            }
        }

        schema = Schema__URLs(**data)

        assert type(schema.urls_by_category['docs'][0]) is Safe_Str__Url
        assert schema.urls_by_category['docs'][0]       == 'https://docs.example.com'

    # Test that regular dict handling still works

    def test__regular_dict_without_nested_collections(self):                           # Test regular dict handling isn't broken
        class Schema__Simple_Dict(Type_Safe):
            mapping: Dict[str, int]

        schema = Schema__Simple_Dict(mapping={'a': 1, 'b': 2})

        assert type(schema.mapping) is Type_Safe__Dict
        assert schema.mapping       == {'a': 1, 'b': 2}

    # Performance test (marked to run manually)

    def test__performance_with_large_nested_structure(self):                           # Test performance with large data
        import time

        class Schema__Large(Type_Safe):
            data: Dict[str, List[str]]

        # Create large dataset
        large_data = {
            'data': {f'key_{i}': [f'item_{j}' for j in range(100)]
                    for i in range(10)}
        }

        start = time.time()
        schema = Schema__Large(**large_data)
        elapsed = time.time() - start

        assert len(schema.data)        == 10
        assert len(schema.data['key_0']) == 100
        assert elapsed < 0.02  # Should be fast

    # Test edge cases

    def test__empty_dict_with_list_annotation(self):                                   # Test empty dict with List annotation
        class Schema__Empty(Type_Safe):
            data: Dict[str, List[str]]

        schema = Schema__Empty(data={})

        assert type(schema.data) is Type_Safe__Dict
        assert schema.data       == {}

    def test__dict_with_empty_lists(self):                                             # Test dict containing empty lists
        class Schema__With_Empty_Lists(Type_Safe):
            data: Dict[str, List[str]]

        schema = Schema__With_Empty_Lists(data={'key1': [], 'key2': []})

        assert type(schema.data['key1']) is Type_Safe__List
        assert schema.data['key1']       == []

    # Test that the fix doesn't break existing behavior

    def test__backwards_compatibility(self):                                           # Ensure fix doesn't break existing code
        class Schema__Legacy(Type_Safe):
            simple_list : List[str]
            simple_dict : Dict[str, str]
            simple_value: str

        schema = Schema__Legacy(simple_list=['a', 'b'],
                               simple_dict={'k': 'v'},
                               simple_value='test')

        assert type(schema.simple_list) is Type_Safe__List
        assert type(schema.simple_dict) is Type_Safe__Dict
        assert schema.simple_value      == 'test'

