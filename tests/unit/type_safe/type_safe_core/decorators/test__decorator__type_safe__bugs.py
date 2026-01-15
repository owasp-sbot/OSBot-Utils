import re

import pytest
from typing                                                                     import List, Dict, Callable
from unittest                                                                   import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List           import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                  import type_safe


class test__decorator__type_safe__bugs(TestCase):

    def test__regression__type_safe_decorator__doesnt_auto_convert_lists_return_value(self):

        #BUG 1
        @type_safe
        def an_function_1(value:str) -> List[Safe_Str__Id]:
            values = ['42', value]
            return values

        # error_message_1 = "Function 'test__decorator__type_safe__bugs.test__bug__type_safe_decorator__doesnt_auto_convert_lists_return_value.<locals>.an_function_1' return type validation failed: In list at index 0: Expected 'Safe_Str__Id', but got 'str'"
        # with pytest.raises(TypeError, match=re.escape(error_message_1)):
        #     an_function_1('is the answer')                                        # BUG
        assert an_function_1('is the answer')       == ['42', 'is_the_answer']      # FIXED
        assert an_function_1('is the answer').obj() == ['42', 'is_the_answer']      # FIXED

        # BUG 2
        class An_List(Type_Safe__List):
            expected_type = Safe_Str__Id

        @type_safe
        def an_function_2(value:str) -> An_List:
            values= ['42', value]
            return values

        # error_message_2 = "In Type_Safe__List: Invalid type for item: Expected 'An_List', but got 'str'"
        # with pytest.raises(TypeError, match=re.escape(error_message_2)):
        #     an_function_2('is the answer')                                  # BUG

        assert an_function_2('is the answer')       == ['42', 'is_the_answer']      # FIXED
        assert an_function_2('is the answer').obj () == ['42', 'is_the_answer']      # FIXED
        assert an_function_2('is the answer').json() == ['42', 'is_the_answer']      # FIXED

        # Control test 1

        @type_safe
        def an_function_3(value:str) -> List[Safe_Str__Id]:
            an_list = Type_Safe__List(expected_type=Safe_Str__Id)
            values  = ['42', value]
            an_list.extend(values)
            return an_list

        an_function_3('is the answer')

        # # Control test 2
        an_list_1 = Type_Safe__List(expected_type=Safe_Str__Id)
        values_1  = ['42', 'value']
        an_list_1.extend(values_1)
        assert type(an_list_1) is Type_Safe__List
        assert type(an_list_1[0]) is Safe_Str__Id
        assert an_list_1 == ['42', 'value']

    def test__bug__type_safe__list_callable_with_signatures(self):

        @type_safe
        def process_with_str_to_int(transformations: List[Callable[[str], int]]):
            pass

        # This should work if signature checking is implemented
        def str_to_int(s: str) -> int:
            return len(s)

        # This should fail if signature checking is implemented
        def int_to_str(i: int) -> str:
            return str(i)

        # Test what happens
        process_with_str_to_int(transformations=[str_to_int])  # Should pass

        # If full signature checking is implemented, this should fail
        # because int_to_str has wrong signature (int -> str instead of str -> int)
        process_with_str_to_int(transformations=[int_to_str])       # BUG: this should had raised exception

    def test__regression__type_safe__list_dict_param__not_supported(self):
        from osbot_utils.type_safe.type_safe_core.decorators.type_safe import type_safe
        @type_safe
        def create_openapi_spec(servers: List[Dict[str, str]]):
            pass
        #error_message = "Validation for list items with subscripted type 'typing.Dict[str, str]' is not yet supported in parameter 'servers'."
        # with pytest.raises(NotImplementedError, match=re.escape(error_message)):
        #     create_openapi_spec(servers     = [{'url': 'https://api.example.com'}])     # FIXED:  BUG raises exception

        create_openapi_spec(servers=[{'url': 'https://api.example.com'}])                 # FIXED: no exception raised :)
        # now that we are checking the types, we can confirm the type checking is working
        with pytest.raises(ValueError, match="Dict value for key 'url' at index 0 expected type <class 'str'>, but got <class 'int'>"):
            create_openapi_spec(servers=[{'url': 123}])
        with pytest.raises(ValueError, match="Dict key '1111' at index 0 expected type <class 'str'>, but got <class 'int'>"):
            create_openapi_spec(servers=[{1111: '123'}])
        with pytest.raises(ValueError, match="Parameter 'servers' expected a list but got <class 'str'>"):
            create_openapi_spec(servers='abc')
        with pytest.raises(ValueError, match="Parameter 'servers' expected a list but got <class 'dict'>"):
            create_openapi_spec(servers={})
        with pytest.raises(ValueError, match="Parameter 'servers' expected a list but got <class 'set'>"):
            create_openapi_spec(servers=set())
        with pytest.raises(ValueError, match="Parameter 'servers' is not optional but got None"):
            create_openapi_spec(servers=None)
        with pytest.raises(ValueError, match="Dict value for key 'aaa' at index 0 expected type <class 'str'>, but got <class 'NoneType'>"):
            create_openapi_spec(servers=[{'aaa': None}])
        with pytest.raises(ValueError, match="Dict key 'None' at index 0 expected type <class 'str'>, but got <class 'NoneType'>"):
            create_openapi_spec(servers=[{None: 'abc'}])
        with pytest.raises(ValueError, match="Dict key 'None' at index 0 expected type <class 'str'>, but got <class 'NoneType'>"):
            create_openapi_spec(servers=[{None: None}])









