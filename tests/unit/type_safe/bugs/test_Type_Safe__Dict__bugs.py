import pytest
from typing                                 import Any, Dict
from unittest                               import TestCase
from osbot_utils.type_safe.Type_Safe        import Type_Safe
from osbot_utils.type_safe.Type_Safe__Dict  import Type_Safe__Dict


class test_Type_Safe__Dict__bugs(TestCase):

    def test__bug__doesnt_support__nested__json__with_mixed_content(self):
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


        expected = {
            "number": 42,
            "string": "text",
            "type_safe": {"value": "safe"},
            "list": [1, {"value": "in_list"}, {"nested": {"value": "in_dict"}}],
            "dict": {
                "normal": "value",
                "safe_obj": {"value": "in_nested_dict"}
            }
        }
        assert safe_dict.json() != expected                                         # BUG should be equal
        assert safe_dict.json()['list'][2]['nested'] != {"value": "in_dict"}
        assert safe_dict.json()['list'][2]['nested'].value == 'in_dict'
        assert type(safe_dict.json()['list'][2]['nested']) is TestTypeSafe


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