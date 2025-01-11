import pytest
from typing                                import Dict
from osbot_utils.type_safe.Type_Safe       import Type_Safe
from osbot_utils.type_safe.Type_Safe__Dict import Type_Safe__Dict


class test_Type_Safe__regression(Type_Safe):
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