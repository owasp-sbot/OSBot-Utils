import pytest
from typing                                     import Dict
from unittest                                   import TestCase
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive
from osbot_utils.type_safe.Type_Safe            import Type_Safe
from osbot_utils.type_safe.Type_Safe__Dict      import Type_Safe__Dict


class test_Type_Safe__Dict__bugs(TestCase):

    def test__bug__comparison_not_type_safe(self):
        class An_Str_1(Type_Safe__Primitive, str):
            pass

        class An_Str_2(Type_Safe__Primitive, str):
            pass

        an_str_1 = An_Str_1('a')
        an_str_2 = An_Str_2('a')

        assert an_str_1      == An_Str_1('a')            # direct type comparison
        assert an_str_1      == 'a'                      # direct value comparison (equal)
        assert an_str_1      != 'b'                      # direct value comparison (not equal)
        assert an_str_1      != 123                      # direct value comparison (not equal)
        assert an_str_1      != an_str_2                 # value is the same, but types are different
        assert str(an_str_1) == str(an_str_2)            #    which we can confirm if we cast both values to str

        class An_Class(Type_Safe):
            an_dict: Dict[An_Str_1, An_Str_2]

        an_class = An_Class(an_dict=dict(a='a'))

        assert an_class.an_dict['a'] == 'a'
        assert an_class.an_dict['a'] != 'ab'
        assert an_class.an_dict['a'] != 123

        an_class = An_Class(an_dict=dict(a='a'))
        value_1 = an_class.an_dict[An_Str_1('a')]
        assert type(value_1) is An_Str_2        # with types

        assert type(an_class.an_dict['a'])     is An_Str_2          # confirms
        assert an_class.an_dict['a']           == 'a'               # we can check by direct str values
        assert an_class.an_dict['a']           == An_Str_2('a')     # ok since 'a' is supposed to be an An_Str_2
        assert an_class.an_dict['a']           != An_Str_1('a')     # strongly type fails (An_Str_1 is not An_Str_2)
        assert an_class.an_dict[An_Str_1('a')] == An_Str_2('a')     # these should be equal
        assert an_class.an_dict[An_Str_1('a')] != An_Str_1('a')     # these should NOT be equal (since the key 'a' is assigned to An_Str_2('a')




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