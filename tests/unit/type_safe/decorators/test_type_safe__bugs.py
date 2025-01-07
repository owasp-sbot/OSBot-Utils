import pytest
from typing                                     import Any
from unittest                                   import TestCase
from osbot_utils.type_safe.Type_Safe            import Type_Safe
from osbot_utils.type_safe.decorators.type_safe import type_safe

class test_type_safe__bugs(TestCase):

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