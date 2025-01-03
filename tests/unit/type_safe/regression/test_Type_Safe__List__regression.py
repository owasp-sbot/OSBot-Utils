import pytest
from typing                                 import List
from unittest                               import TestCase
from osbot_utils.type_safe.Type_Safe        import Type_Safe
from osbot_utils.type_safe.Type_Safe__List  import Type_Safe__List


class test_Type_Safe__List__regression(TestCase):
    def test__regression__nested_types__not_supported__in_list(self):
        class An_Class(Type_Safe):
            an_str  : str
            an_list : List['An_Class']

        an_class   = An_Class()
        assert type(an_class.an_list) is Type_Safe__List
        assert an_class.an_list       == []

        an_class_a = An_Class()
        an_class.an_list.append(an_class_a)
        with pytest.raises(TypeError, match="In Type_Safe__List: Invalid type for item: Expected 'An_Class', but got 'str'"):
            an_class.an_list.append('b'       )     # BUG: as above

    def test__regression__type_safe_list_with_forward_references(self):
        class An_Class(Type_Safe):
            an_list__self_reference: List['An_Class']

        an_class = An_Class()
        an_class.an_list__self_reference.append(An_Class())

        #an_class.an_list__self_reference.append(1)  # BUG , type safety not checked on forward references
        with pytest.raises(TypeError, match="Expected 'An_Class', but got 'int'"):
            an_class.an_list__self_reference.append(1)

    def test__regression__json_is_not_supported(self):
        class An_Class(Type_Safe):
            an_str  : str
            an_list : List['An_Class']

        an_class = An_Class()
        an_class.an_list.append(An_Class())
        assert an_class.json() == {'an_list': [{'an_list': [], 'an_str': ''}], 'an_str': ''}

        # with pytest.raises(AttributeError, match = "Type_Safe__List' object has no attribute 'json'"):
        #     assert an_class.an_list.json()

        assert an_class.an_list.json() == [{'an_list': [], 'an_str': ''}]