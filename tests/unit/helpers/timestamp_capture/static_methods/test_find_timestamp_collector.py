from unittest                                                                      import TestCase
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector                     import Timestamp_Collector
from osbot_utils.helpers.timestamp_capture.static_methods.find_timestamp_collector import find_timestamp_collector
from osbot_utils.helpers.timestamp_capture.timestamp_collector__config             import COLLECTOR_VAR_NAME


class test_find_timestamp_collector(TestCase):

    def test_find_timestamp_collector__not_found(self):                            # Test returns None when no collector
        result = find_timestamp_collector()
        assert result is None

    def test_find_timestamp_collector__found_in_local(self):                       # Test finds collector in local scope
        _timestamp_collector_ = Timestamp_Collector(name='local_test')

        result = find_timestamp_collector()

        assert result                 is _timestamp_collector_
        assert result.name            == 'local_test'

    def test_find_timestamp_collector__found_in_parent_frame(self):                # Test finds collector in parent frame
        _timestamp_collector_ = Timestamp_Collector(name='parent_test')

        def nested_function():
            return find_timestamp_collector()

        result = nested_function()

        assert result      is _timestamp_collector_
        assert result.name == 'parent_test'

    def test_find_timestamp_collector__found_deeply_nested(self):                  # Test finds collector through multiple frames
        _timestamp_collector_ = Timestamp_Collector(name='deep_test')

        def level_1():
            return level_2()

        def level_2():
            return level_3()

        def level_3():
            return find_timestamp_collector()

        result = level_1()

        assert result      is _timestamp_collector_
        assert result.name == 'deep_test'

    def test_find_timestamp_collector__max_depth(self):                            # Test respects max_depth parameter
        _timestamp_collector_ = Timestamp_Collector(name='depth_test')

        def level_1():
            return find_timestamp_collector(max_depth=2)                           # Only search 2 frames up

        def level_2():
            return find_timestamp_collector(max_depth=1)                           # Only search 1 frame up

        result_found     = level_1()                                               # 2 frames up: level_1 -> test method
        result_not_found = level_2()                                               # 1 frame up: level_2 (collector is 2 frames up)

        assert result_found     is _timestamp_collector_                           # Found within 2 frames
        assert result_not_found is None                                            # Not found - max_depth too small

    def test_find_timestamp_collector__wrong_variable_name(self):                  # Test doesn't find wrong variable name
        wrong_collector = Timestamp_Collector(name='wrong_name')                   # Not using magic name

        result = find_timestamp_collector()
        assert result is None

    def test_find_timestamp_collector__wrong_type(self):                           # Test doesn't return wrong type
        _timestamp_collector_ = "not a collector"                                  # Right name, wrong type

        result = find_timestamp_collector()
        assert result is None

    def test_find_timestamp_collector__multiple_collectors(self):                  # Test finds nearest collector
        _timestamp_collector_ = Timestamp_Collector(name='outer')

        def inner_scope():
            _timestamp_collector_ = Timestamp_Collector(name='inner')              # Shadows outer
            return find_timestamp_collector()

        result = inner_scope()
        assert result.name == 'inner'                                              # Finds inner, not outer

    def test_collector_var_name_constant(self):                                    # Test the constant matches expected value
        assert COLLECTOR_VAR_NAME == '_timestamp_collector_'