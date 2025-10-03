import pytest
from unittest                                                                       import TestCase
from typing                                                                         import Dict, Type, Set, Any, List
from osbot_utils.type_safe.primitives.core.Safe_Int                                 import Safe_Int
from osbot_utils.testing.__                                                         import __
from osbot_utils.type_safe.Type_Safe__Primitive                                     import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path   import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id     import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List               import Type_Safe__List
from osbot_utils.utils.Objects                                                      import base_classes, obj
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                   import Safe_Id
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class test_Type_Safe__Dict__regression(TestCase):

    def test__regression__dict__in__doesnt_find_element(self):
        class An_Class(Type_Safe):
            an_dict : Dict[Safe_Str__Id, Safe_Int]

        an_class_1 = An_Class(an_dict={Safe_Str__Id('an_tag'): 42})
        assert an_class_1.obj ()      == __(an_dict=__(an_tag=42))
        assert an_class_1.json()      != {'an_dict': {Safe_Str__Id('an_tag'): 42}}
        assert an_class_1.json()      == {'an_dict': {'an_tag': 42}}
        assert Safe_Str__Id('an_tag') in an_class_1.an_dict


        #error_message_2 = "assert 'an_tag' in {Safe_Str__Id('an_tag'): Safe_Int(42)}\n +  where {Safe_Str__Id('an_tag'): Safe_Int(42)}"
        # with pytest.raises(AssertionError, match=re.escape(error_message_2)):
        #     assert 'an_tag' in an_class_1.an_dict                                                        # FIXED BUG 1 - an_tag should have been converted to Safe_Str__Fast_API__Route__Tag and the 'in' check should had worked
        assert 'an_tag' in an_class_1.an_dict                                                              # FIXED

        assert Safe_Str__Id('an_tag') in an_class_1.an_dict

        an_class_2 = An_Class(an_dict={'an_tag': 42})
        assert an_class_2.obj ()      == __(an_dict=__(an_tag=42))
        assert an_class_2.json()      == {'an_dict': {'an_tag': 42}}
        #assert 'an_tag'          not in an_class_2.an_dict                              # FIXED: BUG 2 - not working
        assert 'an_tag'               in an_class_2.an_dict                              # FIXED
        assert Safe_Str__Id('an_tag') in an_class_2.an_dict

    def test__regression__obj__not_supported(self):
        class An_Class(Type_Safe):
            an_dict: Dict[str, str]

        an_class = An_Class()
        an_class.an_dict['a'] = 'b'
        assert an_class.an_dict.json() == {'a':'b'}
        #with pytest.raises(AttributeError, match= "Type_Safe__Dict' object has no attribute 'obj'"):
        #    an_class.an_dict.obj()           # FIXED BUG
        assert an_class.obj() == __(an_dict=__(a='b'))

    def test__regression__json__with_nested_dicts(self):
        class TestTypeSafe(Type_Safe):
            value: str

        safe_dict = Type_Safe__Dict(str, dict)
        safe_dict["simple" ] = {"a": 1, "b": 2}
        safe_dict["complex"] = { "normal": "value",
                                 "safe"  : TestTypeSafe(value="test"),
                                 "nested": {"deep": TestTypeSafe(value="deep")} }

        expected = { "simple": {"a": 1, "b": 2},
                     "complex": { "normal": "value",
                                  "safe"  : {"value": "test"},
                                  "nested": {"deep": {"value": "deep"}}}}
        assert safe_dict.json() == expected         # FIXED: BUG should be equal
        assert safe_dict.obj() == __(simple  = __(a=1, b=2),
                                     complex = __(normal = 'value',
                                                  safe   = __(value = 'test'            ),
                                                  nested = __(deep  = __(value='deep'))))

    def test__regression__dict_with_safe_id_keys__string_lookup_fails(self):   #  Test that demonstrates the bug where Type_Safe__Dict with Safe_Id keys doesn't support plain string lookups (get with string key returns None).

        class Schema_With_Safe_Id_Keys(Type_Safe):
            metadata: Dict[Safe_Id, str]

        # Create instance and add data with Safe_Id keys
        schema = Schema_With_Safe_Id_Keys()
        schema.metadata[Safe_Id('cache_hash')] = '36e2b79ffcdbc847'
        schema.metadata[Safe_Id('stored_at')] = '1756754569954'
        schema.metadata[Safe_Id('namespace')] = 'test-api'

        # Verify the data is stored correctly with Safe_Id keys
        assert len(schema.metadata) == 3
        assert Safe_Id('cache_hash') in schema.metadata.keys()
        assert Safe_Id('stored_at') in schema.metadata.keys()
        assert Safe_Id('namespace') in schema.metadata.keys()

        # Direct lookup with Safe_Id works
        assert schema.metadata[Safe_Id('cache_hash')] == '36e2b79ffcdbc847'
        assert schema.metadata[Safe_Id('stored_at')] == '1756754569954'
        assert schema.metadata[Safe_Id('namespace')] == 'test-api'

        # FIXED: BUG: Plain string lookup fails (returns KeyError or None with .get())
        assert schema.metadata.get('cache_hash') is not None   # FIXED : BUG: should return '36e2b79ffcdbc847'
        assert schema.metadata.get('stored_at' ) is not None   # FIXED : BUG: should return '1756754569954'
        assert schema.metadata.get('namespace' ) is not None   # FIXED : BUG: should return 'test-api'

        assert schema.metadata.get('cache_hash') == '36e2b79ffcdbc847'
        assert schema.metadata.get('stored_at' ) == '1756754569954'
        assert schema.metadata.get('namespace' ) == 'test-api'

        # Direct string access raises KeyError (Works)
        assert schema.metadata['cache_hash'] == '36e2b79ffcdbc847'
        assert schema.metadata['stored_at' ] == '1756754569954'

        # Demonstrate the issue in a simulated cache retrieval scenario
        response_retrieve = { 'data'    : 'test cache string',
                              'metadata': schema.metadata }             # This has Safe_Id keys


        # This is what fails in the original test
        stored_at_plain = response_retrieve.get('metadata').get('stored_at')
        assert stored_at_plain is not None  # FIXED BUG: Returns None because string doesn't match Safe_Id
        assert stored_at_plain == '1756754569954'

        # Current workaround required
        stored_at_safe = response_retrieve.get('metadata').get(Safe_Id('stored_at'))
        assert stored_at_safe == '1756754569954'            # This works but is not intuitive

        # Additional test: iteration shows the keys are actually Safe_Id instances
        for key in schema.metadata.keys():
            assert type(key) is Safe_Id
            assert type(str(key)) is str
            if str(key) == 'cache_hash':
                assert key == 'cache_hash'              # this also works

    def test__regression__get__not_working_with_strings(self):
        class An_Class(Type_Safe):
            some_ids : dict[Safe_Id,int]

        an_class = An_Class(some_ids={'abc':42})
        an_class_json = an_class.json()
        assert an_class_json       != {'some_ids': { Safe_Id('abc'): 42}}           # FIXED: BUG: .json() should be pure primitives
        assert an_class_json       == {'some_ids': {'abc': 42}}                     # FIXED: BUG: this should be equal
        assert type(an_class_json.get('some_ids')) is dict
        assert type(an_class_json.get('some_ids')) is not Type_Safe__Dict
        assert an_class_json.get('some_ids').get('abc'         ) is not None        # FIXED: BUG this should have worked
        assert an_class_json.get('some_ids').get(Safe_Id('abc')) != 42              # FIXED: BUG this should not be the only way to make this work

    def test__regression__str_to_safe_id__conversion_not_supports(self):
        class An_Class(Type_Safe):
            an_dict: Dict[Safe_Id, Safe_Id]
        an_class = An_Class()
        an_class.an_dict[Safe_Id("aaa")] = Safe_Id("bbbb")  # strongly typed
        assert isinstance(Safe_Id, str) is False            # confirm Safe_Id is not a direct string
        assert issubclass(Safe_Id, str) is True             # but has str as a base class
        assert base_classes(Safe_Id) == [Type_Safe__Primitive, str, object, object]       # also confirmed by the base class list
        #with pytest.raises(TypeError, match="Expected 'Safe_Id', but got 'str'") :
        #    an_class.an_dict[Safe_Id("aaa")] = "bbbb"                                                       # FIXED: BUG: this should be supported since we can convert the str into Safe_Id
        #with pytest.raises(TypeError, match="Expected 'Safe_Id', but got 'str'") :
        #    an_class.an_dict["ccc"] = Safe_Id("dddd")                                                       # FIXED: BUG: this should be supported since we can convert the str into Safe_Id

        # confirm direct assigment now works
        an_class.an_dict[Safe_Id("aaa")] = "bbbb"
        an_class.an_dict["ccc"         ] = Safe_Id("dddd")
        assert type(an_class.an_dict["aaa"]) is Safe_Id
        assert type(an_class.an_dict["ccc"]) is Safe_Id
        for key, value in an_class.an_dict.items():
            assert type(key) is Safe_Id
            assert type(value) is Safe_Id

        # confirm kwargs assigment now works
        kwargs = dict(an_dict={        "an_key_1" :"an_value_1"         ,
                               Safe_Id("an_key_2"): "an_value_2"          ,
                                       "an_key_3" : Safe_Id("an_value_3" )})
        an_class_2 = An_Class(**kwargs)

        with an_class_2.an_dict as _:
            for key, value in _.items():
                assert type(key) is Safe_Id
                assert type(value) is Safe_Id

        with an_class_2.an_dict.keys() as _:
            assert type(_)          is Type_Safe__List
            assert _.expected_type  is Safe_Id
            assert _                == ['an_key_1', 'an_key_2', 'an_key_3']
            assert _                == [Safe_Id('an_key_1'), 'an_key_2', 'an_key_3']
            assert _                == [Safe_Id('an_key_1'), Safe_Id('an_key_2'), Safe_Id('an_key_3')]

        with an_class_2.an_dict.values() as _:
            assert type(_) is Type_Safe__List
            assert _.expected_type is Safe_Id
            assert _                == [        'an_value_1',          'an_value_2',          'an_value_3']
            assert _                == [Safe_Id('an_value_1'),         'an_value_2',          'an_value_3']
            assert _                == [Safe_Id('an_value_1'), Safe_Id('an_value_2'), Safe_Id('an_value_3')]

    def test__regression__doesnt_support__nested__json__with_mixed_content(self):
        class TestTypeSafe(Type_Safe):
            value: str

        safe_dict = Type_Safe__Dict(str, Any)
        safe_dict["number"] = 42
        safe_dict["string"] = "text"
        safe_dict["type_safe"] = TestTypeSafe(value="safe")
        safe_dict["list"] = [1, TestTypeSafe(value="in_list"), {"nested": TestTypeSafe(value="in_dict")}]
        safe_dict["dict"] = {
            "normal": "value",
            "safe_obj": TestTypeSafe(value="in_nested_dict")
        }


        expected = { "number": 42,
                     "string": "text",
                     "type_safe": {"value": "safe"},
                     "list": [1, {"value": "in_list"}, {"nested": {"value": "in_dict"}}],
                     "dict": {
                         "normal": "value",
                         "safe_obj": {"value": "in_nested_dict"} } }
        assert safe_dict.json() == expected                                         # FIXED: BUG should be equal
        assert safe_dict.json()['list'][2]['nested'] == {"value": "in_dict"}        # FIXED:
        assert safe_dict.json()['list'][2]['nested']['value'] == 'in_dict'          # FIXED:
        assert type(safe_dict.json()['list'][2]['nested']) is dict                  # FIXED:


    def test__regression__type_keys_in_json(self):

        class Bug_Type_Keys:                                                       # Simple class for testing
            pass

        class Another_Type:                                                        # Another class for testing
            pass


        # Create a Type_Safe_Dict with Type objects as keys
        type_dict                = Type_Safe__Dict(Type, Set[str])
        type_dict[Bug_Type_Keys] = {'value1', 'value2'}
        type_dict[Another_Type]  = {'value3', 'value4'}

        # Get JSON representation
        json_data = type_dict.json()
        assert json_data == { 'test_Type_Safe__Dict__regression.Another_Type' : {'value4', 'value3'},
                              'test_Type_Safe__Dict__regression.Bug_Type_Keys': {'value2', 'value1'}}     # FIXED

        # # The bug is that the keys in json_data are still Type objects
        # # This assertion passes when the bug is present
        # self.assertTrue(any(isinstance(key, type) for key in json_data.keys()),"Bug confirmed: Type objects are not being converted to strings in JSON output" )
        #
        # # Additional verification that shows the problematic output
        # type_keys = [key for key in json_data.keys() if isinstance(key, type)]
        # self.assertGreater(len(type_keys),0,"Should find Type objects as keys in JSON output, confirming the bug")

    def test__regression__in_schema_context(self):

        class Bug_Type_Keys:                                                       # Simple class for testing
            pass


        class Schema_With_Type_Dict(Type_Safe):                                    # Schema that uses Dict[Type, Set[str]]
            values: Dict[Type, Set[str]]

        schema                       = Schema_With_Type_Dict()                      # Demonstrate the bug in the context of a schema
        schema.values[Bug_Type_Keys] = set()
        schema.values[Bug_Type_Keys].add('test1')
        schema.values[Bug_Type_Keys].add('test2')

        assert type(schema.values) is Type_Safe__Dict
        json_data = schema.json()                                                   # Get JSON representation

        #assert json_data == { 'values': { test_Type_Safe__Dict__bugs.Bug_Type_Keys: ['test1', 'test2']}}       # BUG should not be using type
        bug_type_keys = json_data.get('values').get('test_Type_Safe__Dict__regression.Bug_Type_Keys')
        assert type(bug_type_keys) is set
        assert 'test1' in bug_type_keys
        assert 'test2' in bug_type_keys
        #assert type(json_data.values['test_Type_Safe__Dict__bugs.Bug_Type_Keys']) is set
        # Verify the bug exists in schema context
        self.assertFalse(any(isinstance(key, type) for key in json_data['values'].keys()), "Bug confirmed: Type objects remain as Type objects in schema JSON output")

    def test__regression__json_not_supported(self):
        class An_Class(Type_Safe):
            an_dict: Dict[str, int]

        an_class = An_Class()
        an_class.an_dict['key'] = 42

        assert an_class.json() == {'an_dict': {'key': 42}}
        # with pytest.raises(AttributeError, match = "Type_Safe__Dict' object has no attribute 'json'"):
        #     assert an_class.an_dict.json() ==  {'key': 42}          # BUG - this should work
        assert an_class.an_dict.json() ==  {'key': 42}

    def test__regression__nested_types__not_supported__in_dict(self):       # Similar to the list test that uses forward references in nested structures
        class An_Class(Type_Safe):
            an_str: str
            an_dict: Dict[str, 'An_Class']

        an_class = An_Class()
        an_class.an_str = "top-level"
        assert type(an_class.an_dict) is Type_Safe__Dict
        assert an_class.an_dict == {}

        # Valid usage
        an_child = An_Class()
        an_child.an_str = "child"
        an_class.an_dict['child'] = an_child

        # Invalid usage
        with pytest.raises(TypeError, match="Expected 'An_Class', but got 'str'"):
            an_class.an_dict['bad_child'] = "some string"                               # Fixed: BUG didn't raise an exception

    def test__regression__type_safe_assigment__not_handling_dict_with_List__on_ctor(self):
        class An_Class_1(Type_Safe):
            all_paths      : Dict[Safe_Str__Id, List[Safe_Str__File__Path]]

        data = { 'by_hash': [ 'refs/by-hash/e1/5b/e15b31f87df1896e.json',
                               'refs/by-hash/e1/5b/e15b31f87df1896e.json.config',
                               'refs/by-hash/e1/5b/e15b31f87df1896e.json.metadata'],
                  'by_id': [ 'refs/by-id/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json',
                             'refs/by-id/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.config',
                             'refs/by-id/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.metadata'],
                  'data': [ 'data/direct/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json',
                            'data/direct/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.config',
                            'data/direct/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.metadata']}

        # error_message_1 = "In list at index 0: Expected 'Safe_Str__File__Path', but got 'str'"
        # with pytest.raises(TypeError, match=re.escape(error_message_1)):
        #     An_Class_1(all_paths=data)                                                                    # BUG
        An_Class_1(all_paths=data)

        an_class_1 = An_Class_1(all_paths=data)
        assert an_class_1.json()    == {"all_paths": data }                                             # confirm roundtrip with .json()
        assert an_class_1.obj()     == __(all_paths = obj(data))                                        # confirm roundtrip with obj().

    def test__regression__type_safe_assigment__not_handling_dict_with_List(self):
        class An_Class_1(Type_Safe):
            all_paths      : Dict[Safe_Str__Id, List[Safe_Str__File__Path]]

        data = { 'by_hash': [ 'refs/by-hash/e1/5b/e15b31f87df1896e.json',
                               'refs/by-hash/e1/5b/e15b31f87df1896e.json.config',
                               'refs/by-hash/e1/5b/e15b31f87df1896e.json.metadata'],
                  'by_id': [ 'refs/by-id/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json',
                             'refs/by-id/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.config',
                             'refs/by-id/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.metadata'],
                  'data': [ 'data/direct/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json',
                            'data/direct/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.config',
                            'data/direct/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.metadata']}

        # error_message_1 = "Type List cannot be instantiated; use list() instead"                      # BUG 1 with List
        # with pytest.raises(TypeError, match=re.escape(error_message_1)):
        #     An_Class_1().all_paths = data
        An_Class_1().all_paths = data                                                                   # FIXED
        an_class_1 = An_Class_1()
        an_class_1.all_paths = data                                                                     # FIXED:
        assert an_class_1.json()    == {"all_paths": data }                                             # confirm roundtrip with .json()
        assert an_class_1.obj()     == __(all_paths = obj(data))                                        # confirm roundtrip with obj().


        class An_Class_2(Type_Safe):
            all_paths      : Dict[Safe_Str__Id, list[Safe_Str__File__Path]]

        # error_message_2 = "In list at index 0: Expected 'Safe_Str__File__Path', but got 'str'"        # BUG 2 with list
        # with pytest.raises(TypeError, match=re.escape(error_message_2)):
        #     An_Class_2().all_paths = data
        An_Class_2().all_paths = data                                                                   # FIXED
        an_class_2 = An_Class_2()
        an_class_2.all_paths = data                                                                     # FIXED:
        assert an_class_2.json()    == {"all_paths": data }                                             # confirm roundtrip with .json()
        assert an_class_2.obj()     == __(all_paths = obj(data))                                        # confirm roundtrip with obj().