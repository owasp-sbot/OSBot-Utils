import pytest
from typing                                                                    import List, Dict, Callable
from unittest                                                                  import TestCase
from osbot_utils.type_safe.Type_Safe                                           import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                 import type_safe


class test__decorator__type_safe__bugs(TestCase):


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





