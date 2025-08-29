import re

import pytest
from typing                                                           import Dict, List, Any
from unittest                                                         import TestCase
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict import Type_Safe__Dict


class test_Type_Safe__Dict__bugs(TestCase):

    def test__bug__type_safe_list_with_dict_any_type__and__error_message_is_confusing(self):   # Document bug where Dict[str, any] fails in List ,and the error message doesn't mention that Any works

        class Schema__Order__Bug(Type_Safe):
            items: List[Dict[str, any]]                                                    # BUG: lowercase 'any' is a function, not a type

        class Schema__Order__Fixed(Type_Safe):
            items: List[Dict[str, Any]]                                                    # FIXED: uppercase 'Any' from typing

        # Document the bug - lowercase 'any' causes TypeError
        with Schema__Order__Bug() as buggy_order:
            error_message = "In Type_Safe__List: Invalid type for item: In dict value for key 'product': isinstance() arg 2 must be a type, a tuple of types, or a union"
            with pytest.raises(TypeError, match=re.escape(error_message)):
                buggy_order.items = [{'product': 'laptop', 'qty': 1}]                     # BUG: fails with isinstance error

        # Document what SHOULD work (using Any from typing)
        with Schema__Order__Fixed() as fixed_order:
            fixed_order.items = [{'product': 'laptop', 'qty': 1, 'price': 999.99}]       # Works with Any
            assert fixed_order.items == [{'product': 'laptop', 'qty': 1, 'price': 999.99}]

        # Alternative that also works - using dict without type params
        class Schema__Order__Alternative(Type_Safe):
            items: List[dict]                                                             # Plain dict also works

        with Schema__Order__Alternative() as alt_order:
            alt_order.items = [{'product': 'laptop', 'qty': 1}]                          # Works
            assert alt_order.items == [{'product': 'laptop', 'qty': 1}]

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