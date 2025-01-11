import pytest
from typing                                 import List
from unittest                               import TestCase
from osbot_utils.type_safe.Type_Safe        import Type_Safe
from osbot_utils.type_safe.Type_Safe__List  import Type_Safe__List


class test_Type_Safe__List__bugs(TestCase):
    def test__bug__type_safe_list_with_callable(self):
        from typing import Callable

        class An_Class(Type_Safe):
            an_list__callable: List[Callable[[int], str]]

        an_class = An_Class()

        def invalid_func(x: str) -> int:                    # Invalid callable (wrong signature)
            return len(x)

        an_class.an_list__callable.append(invalid_func)     # BUG doesn't raise  (i.e. at the moment we are not detecting the callable signature and return type)

    def test__bug__json_with_nested_dicts(self):
        class TestType(Type_Safe):
            value: str

            def __init__(self, value):
                self.value = value

        dict_list = Type_Safe__List(dict)
        dict_list.append({"simple": "value"})
        dict_list.append({
            "normal": 42,
            "safe": TestType("test"),
            "nested": {"deep": TestType("deep")}
        })

        expected = [
            {"simple": "value"},
            {
                "normal": 42,
                "safe": {"value": "test"},
                "nested": {"deep": {"value": "deep"}}
            }
        ]
        assert dict_list.json() != expected

    def test__bug__obj__not_supported(self):
        class An_Class(Type_Safe):
            an_list__obj: List[object]

        an_class = An_Class()
        an_class.an_list__obj.append('a')
        assert an_class.an_list__obj.json() == ['a']
        with pytest.raises(AttributeError, match= "Type_Safe__List' object has no attribute 'obj'"):
            an_class.an_list__obj.obj()           # BUG

