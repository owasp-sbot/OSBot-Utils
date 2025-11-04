import re
import pytest
from typing                                                                    import List, Dict, Callable
from unittest                                                                  import TestCase
from osbot_utils.type_safe.Type_Safe                                           import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                 import type_safe


class test__decorator__type_safe__bugs(TestCase):

    def test__bug__type_safe__return_value__not_works__with_forward_refs(self):
        class An_Class(Type_Safe):
            @type_safe
            def return_self(self) ->'An_Class':
                return self
        error_message = "Function 'test__decorator__type_safe__bugs.test__bug__type_safe__return_value__not_works__with_forward_refs.<locals>.An_Class.return_self' return type validation failed: isinstance() arg 2 must be a type, a tuple of types, or a union"
        with pytest.raises(TypeError, match=re.escape(error_message)):
            An_Class().return_self()

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





    def test__bug__kwargs_not_properly_returned_in_type_safe(self):

        class Test_Class(Type_Safe):
            @type_safe
            def method_with_kwargs(self, name: str, **kwargs):          # The bug is caused by the non handling correctly of the **kwargs parameter
                return {"name": name, "kwargs": kwargs}                 # We expect kwargs to contain all extra parameters

        test_obj = Test_Class()
        with self.assertRaises(ValueError) as context:                  # This works as expected - type safety catches the error
            test_obj.method_with_kwargs(name=b'123')                    # Wrong type for 'name'

        assert str(context.exception) == "Parameter 'name' expected type <class 'str'>, but got <class 'bytes'>"

        result   = test_obj.method_with_kwargs(name="test", extra=True, another="value")
        expected = {"kwargs": {"extra": True, "another": "value"},
                    "name"  : "test",}
        current =  {'kwargs': { "kwargs": {"extra": True, "another": "value"}},             # # BUG: there is an extra kwargs added to the return value
                     "name" : "test",}

        assert result != expected  # BUG: This is what we expect
        assert result == current   # BUG: This is what we get



