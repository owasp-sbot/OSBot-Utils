import time
from unittest                                                                         import TestCase

from osbot_fast_api_serverless.utils.testing.skip_tests import skip__if_not__in_github_actions

from osbot_utils.helpers.timestamp_capture.Timestamp_Collector                        import Timestamp_Collector
from osbot_utils.helpers.timestamp_capture.context_managers.timestamp_block           import timestamp_block


class test_timestamp_block(TestCase):

    def test_timestamp_block__no_collector(self):                                     # Test block works without collector
        executed = False

        with timestamp_block('test_block'):
            executed = True

        assert executed is True                                                       # Block executes normally

    def test_timestamp_block__with_collector(self):                                   # Test block records with collector
        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            with timestamp_block('my_block'):
                pass

        assert _timestamp_collector_.entry_count()     == 2                           # enter + exit
        assert _timestamp_collector_.entries[0].name   == 'my_block'
        assert _timestamp_collector_.entries[0].event  == 'enter'
        assert _timestamp_collector_.entries[1].name   == 'my_block'
        assert _timestamp_collector_.entries[1].event  == 'exit'

    def test_timestamp_block__nested_blocks(self):                                    # Test nested blocks
        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            with timestamp_block('outer_block'):
                with timestamp_block('inner_block'):
                    pass

        assert _timestamp_collector_.entry_count() == 4

        assert _timestamp_collector_.entries[0].name  == 'outer_block'
        assert _timestamp_collector_.entries[0].event == 'enter'
        assert _timestamp_collector_.entries[0].depth == 0

        assert _timestamp_collector_.entries[1].name  == 'inner_block'
        assert _timestamp_collector_.entries[1].event == 'enter'
        assert _timestamp_collector_.entries[1].depth == 1

        assert _timestamp_collector_.entries[2].name  == 'inner_block'
        assert _timestamp_collector_.entries[2].event == 'exit'

        assert _timestamp_collector_.entries[3].name  == 'outer_block'
        assert _timestamp_collector_.entries[3].event == 'exit'

    def test_timestamp_block__with_exception(self):                                   # Test block handles exceptions (exit still recorded)
        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            try:
                with timestamp_block('error_block'):
                    raise ValueError('test error')
            except ValueError:
                pass

        assert _timestamp_collector_.entry_count()     == 2                           # Still records both
        assert _timestamp_collector_.entries[0].event  == 'enter'
        assert _timestamp_collector_.entries[1].event  == 'exit'

    def test_timestamp_block__timing_accuracy(self):                                  # Test timing is reasonably accurate
        skip__if_not__in_github_actions()
        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            with timestamp_block('timed_block'):
                time.sleep(0.01)                                                      # 10ms

        enter_entry = _timestamp_collector_.entries[0]
        exit_entry  = _timestamp_collector_.entries[1]
        duration_ns = exit_entry.timestamp_ns - enter_entry.timestamp_ns

        assert duration_ns >= 10_000_000                                              # At least 10ms

    def test_timestamp_block__sequential_blocks(self):                                # Test multiple sequential blocks
        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            with timestamp_block('block_1'):
                pass
            with timestamp_block('block_2'):
                pass
            with timestamp_block('block_3'):
                pass

        assert _timestamp_collector_.entry_count()  == 6                              # 3 * (enter + exit)
        assert _timestamp_collector_.method_count() == 3                              # 3 unique block names

    def test_timestamp_block__with_return_value(self):                                # Test block can be used with value production
        _timestamp_collector_ = Timestamp_Collector()
        result = None

        with _timestamp_collector_:
            with timestamp_block('compute_block'):
                result = 42 * 2

        assert result == 84
        assert _timestamp_collector_.entry_count() == 2

    def test_timestamp_block__depth_tracking(self):                                   # Test depth is correctly tracked
        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            with timestamp_block('level_0'):                                          # depth 0
                assert _timestamp_collector_._depth == 1

                with timestamp_block('level_1'):                                      # depth 1
                    assert _timestamp_collector_._depth == 2

                    with timestamp_block('level_2'):                                  # depth 2
                        assert _timestamp_collector_._depth == 3

                    assert _timestamp_collector_._depth == 2
                assert _timestamp_collector_._depth == 1
            assert _timestamp_collector_._depth == 0