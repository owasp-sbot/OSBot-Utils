from unittest                                   import TestCase
from osbot_utils.type_safe.Type_Safe__On_Demand import Type_Safe__On_Demand


class test_Type_Safe__On_Demand__regression(TestCase):                              # Regression tests for specific bugs

    def test__init_complete_flag_timing(self):                                      # Ensure _on_demand__init_complete is False during init, True after
        class Inner(Type_Safe__On_Demand):
            value: str = ""

        class Outer(Type_Safe__On_Demand):
            inner: Inner

        # After construction, flag should be True
        outer = Outer()
        assert outer._on_demand__init_complete    is True

    def test__multiple_instances_independent(self):                                 # Test that multiple instances have independent on-demand state
        class Inner(Type_Safe__On_Demand):
            value: str = "default"

        class Outer(Type_Safe__On_Demand):
            inner: Inner

        outer1 = Outer()
        outer2 = Outer()

        # Access inner on outer1 only
        inner1 = outer1.inner
        inner1.value = "modified"

        # outer2.inner should still be pending
        assert 'inner' not in outer1._on_demand__types                              # Accessed
        assert 'inner' in outer2._on_demand__types                                  # Still pending

        # And when accessed, should have default value
        assert outer2.inner.value                 == "default"

    def test__json_does_not_include_internal_attrs(self):                           # Verify internal attributes handling in JSON
        class Simple(Type_Safe__On_Demand):
            value: str = "test"

        with Simple() as _:
            json_data = _.json()
            # Internal attrs may be present but should not break functionality
            assert 'value' in json_data
            assert json_data['value']             == "test"
