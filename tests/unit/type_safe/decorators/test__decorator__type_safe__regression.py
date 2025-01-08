import re
import pytest
from typing                                     import Any, Dict
from unittest                                   import TestCase
from osbot_utils.type_safe.Type_Safe            import Type_Safe
from osbot_utils.type_safe.decorators.type_safe import type_safe

class test_decorator__type_safe__regression(TestCase):

    def test__regression__dict_attribute_fail(self):
        class An_Attribute(Type_Safe):
            an_str: str

        class An_Class(Type_Safe):
            @type_safe
            def an_method__instance(self, attributes: Dict[str, An_Attribute]):
                return attributes

        @type_safe
        def an_method__static(attributes: Dict[str, An_Attribute]):
            return attributes

        an_attribute = An_Attribute()
        attributes   = {'aaa': an_attribute}
        # with pytest.raises(TypeError, match="Subscripted generics cannot be used with class and instance checks"):
        #     an_method__static(attributes)                                                 # Fixed: BUG   : should have not raised TypeError error
        assert an_method__static(attributes           ) == attributes                        # Fixed: now it works :)
        assert an_method__static({'aaa': an_attribute}) == attributes

        # with pytest.raises(TypeError, match="Subscripted generics cannot be used with class and instance checks"):
        #     an_method__static({'aaa': 'abc'       })                                      # Fixed: BUG: should have failed with type safe check

        with pytest.raises(ValueError, match=re.escape("Dict value for key 'aaa' expected type <class 'test__decorator__type_safe__regression.test_decorator__type_safe__regression.test__regression__dict_attribute_fail.<locals>.An_Attribute'>, but got <class 'str'>")):
            an_method__static({'aaa': 'abc'       })                                        # Fixed: BUG: should have failed with type safe check
        #
        # with pytest.raises(TypeError, match="Subscripted generics cannot be used with class and instance checks"):
        #     An_Class().an_method__instance({'aaa': an_attribute})                         # Fixed: BUG   : should have not raised TypeError error

        assert An_Class().an_method__instance(attributes           ) == attributes          # Fixed: expected behaviour
        assert An_Class().an_method__instance({'aaa': an_attribute}) == attributes


    def test__regression__kwargs_any_is_converted_into_bool(self):

        class An_Class(Type_Safe):

            @type_safe
            def method_1(self, value: any, node_type: type = None):
                return dict(value=value, node_type=node_type)

            @type_safe
            def method_2(self, value: Any, node_type: type = None):
                return dict(value=value, node_type=node_type)

        expected_error = "Parameter 'value' uses lowercase 'any' instead of 'Any' from typing module. Please use 'from typing import Any' and annotate as 'value: Any'"
        with pytest.raises(ValueError, match=expected_error):
            assert An_Class().method_1('a', int) # Fixed was:  == {'value': True, 'node_type': int}  # BUG, value should be 'a'

        assert An_Class().method_2('a', int) == {'node_type': int, 'value': 'a'}            # Fixed