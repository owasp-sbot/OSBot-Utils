import pytest
from typing                                                           import Dict
from unittest                                                         import TestCase
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict import Type_Safe__Dict


class test_Type_Safe__Dict__bugs(TestCase):


    def test__bug__json__with_nested_dicts(self):
        class TestTypeSafe(Type_Safe):
            value: str

            def __init__(self, value):
                self.value = value

        safe_dict = Type_Safe__Dict(str, dict)
        safe_dict["simple"] = {"a": 1, "b": 2}
        safe_dict["complex"] = {
            "normal": "value",
            "safe": TestTypeSafe("test"),
            "nested": {"deep": TestTypeSafe("deep")}
        }

        expected = {
            "simple": {"a": 1, "b": 2},
            "complex": {
                "normal": "value",
                "safe": {"value": "test"},
                "nested": {"deep": {"value": "deep"}}
            }
        }
        assert safe_dict.json() != expected         # BUG should be equal

    def test__bug__json__with_tuple_values(self):
        class TestTypeSafe(Type_Safe):
            value: str

            def __init__(self, value):
                self.value = value

        safe_dict = Type_Safe__Dict(str, tuple)
        safe_dict["simple"] = (1, 2, 3)
        safe_dict["mixed"] = (TestTypeSafe("test"), 2, TestTypeSafe("other"))

        expected = {
            "simple": (1, 2, 3),
            "mixed": ({"value": "test"}, 2, {"value": "other"})
        }
        assert safe_dict.json() != expected                                     # BUG should be equal

    def test__bug__obj__not_supported(self):
        class An_Class(Type_Safe):
            an_dict: Dict[str, str]

        an_class = An_Class()
        an_class.an_dict['a'] = 'b'
        assert an_class.an_dict.json() == {'a':'b'}
        with pytest.raises(AttributeError, match= "Type_Safe__Dict' object has no attribute 'obj'"):
            an_class.an_dict.obj()           # BUG