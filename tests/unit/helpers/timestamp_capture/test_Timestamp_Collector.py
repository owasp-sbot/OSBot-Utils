import threading
from unittest                                                                      import TestCase

from osbot_fast_api_serverless.utils.testing.skip_tests import skip__if_not__in_github_actions

from osbot_utils.helpers.timestamp_capture.Timestamp_Collector                     import Timestamp_Collector
from osbot_utils.helpers.timestamp_capture.schemas.Schema__Timestamp_Entry         import Schema__Timestamp_Entry
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
from osbot_utils.utils.Objects                                                     import base_classes


class test_Timestamp_Collector(TestCase):

    def test__init__(self):                                                        # Test auto-initialization
        with Timestamp_Collector() as _:
            assert type(_)            is Timestamp_Collector
            assert base_classes(_)    == [Type_Safe, object]
            assert _.name             == 'default'
            assert _.entries          == []
            assert _.start_time_ns    > 0                                          # Set by __enter__
            assert _.end_time_ns      == 0                                         # Not set until __exit__
            assert _.thread_id        == threading.get_ident()
            assert _._depth           == 0
            assert _._active          is True                                      # Active inside context
            assert _._call_stack      == []

    def test__init____with_name(self):                                             # Test custom name
        with Timestamp_Collector(name='my_workflow') as _:
            assert _.name == 'my_workflow'

    def test__context_manager(self):                                               # Test context manager protocol
        collector = Timestamp_Collector()
        assert collector.is_active()      is False
        assert collector.start_time_ns    == 0
        assert collector.end_time_ns      == 0

        with collector:
            assert collector.is_active()  is True
            assert collector.start_time_ns > 0
            assert collector.end_time_ns   == 0

        assert collector.is_active()      is False
        assert collector.end_time_ns      > 0
        assert collector.end_time_ns      >= collector.start_time_ns

    def test_record(self):                                                         # Test low-level record API
        with Timestamp_Collector() as _:
            entry = _.record('method_a', 'enter')

            assert type(entry)         is Schema__Timestamp_Entry
            assert entry.name          == 'method_a'
            assert entry.event         == 'enter'
            assert entry.timestamp_ns  > 0
            assert entry.clock_ns      > 0
            assert entry.thread_id     == threading.get_ident()
            assert entry.depth         == 0
            assert entry.extra         is None
            assert len(_.entries)      == 1

    def test_record__with_extra(self):                                             # Test record with extra data
        with Timestamp_Collector() as _:
            entry = _.record('method_b', 'exit', extra={'count': 42})

            assert entry.extra == {'count': 42}

    def test_record__when_inactive(self):                                          # Test record returns None when inactive
        collector = Timestamp_Collector()
        entry = collector.record('method_c', 'enter')

        assert entry              is None
        assert len(collector.entries) == 0

    def test_enter(self):                                                          # Test enter method
        with Timestamp_Collector() as _:
            _.enter('method_1')

            assert len(_.entries)      == 1
            assert _.entries[0].name   == 'method_1'
            assert _.entries[0].event  == 'enter'
            assert _.entries[0].depth  == 0
            assert _._depth            == 1
            assert len(_._call_stack)  == 1

    def test_exit(self):                                                           # Test exit method
        with Timestamp_Collector() as _:
            _.enter('method_1')
            _.exit('method_1')

            assert len(_.entries)      == 2
            assert _.entries[0].event  == 'enter'
            assert _.entries[1].event  == 'exit'
            assert _.entries[1].name   == 'method_1'
            assert _._depth            == 0
            assert len(_._call_stack)  == 0

    def test_enter_exit__nested(self):                                             # Test nested enter/exit with depth tracking
        with Timestamp_Collector() as _:
            _.enter('outer')                                                       # depth 0 -> 1
            assert _._depth == 1
            assert _.entries[-1].depth == 0

            _.enter('middle')                                                      # depth 1 -> 2
            assert _._depth == 2
            assert _.entries[-1].depth == 1

            _.enter('inner')                                                       # depth 2 -> 3
            assert _._depth == 3
            assert _.entries[-1].depth == 2

            _.exit('inner')                                                        # depth 3 -> 2
            assert _._depth == 2

            _.exit('middle')                                                       # depth 2 -> 1
            assert _._depth == 1

            _.exit('outer')                                                        # depth 1 -> 0
            assert _._depth == 0

            assert len(_.entries) == 6                                             # 3 enters + 3 exits

    def test_total_duration_ns(self):                                              # Test total duration calculation
        skip__if_not__in_github_actions()
        import time
        with Timestamp_Collector() as _:
            time.sleep(0.01)                                                       # 10ms

        duration_ns = _.total_duration_ns()
        duration_ms = _.total_duration_ms()

        assert duration_ns        > 0
        assert duration_ns        >= 10_000_000                                    # At least 10ms
        assert duration_ms        >= 10.0
        assert duration_ms        == duration_ns / 1_000_000

    def test_entry_count(self):                                                    # Test entry count
        with Timestamp_Collector() as _:
            _.enter('a')
            _.exit('a')
            _.enter('b')
            _.exit('b')

            assert _.entry_count() == 4

    def test_method_count(self):                                                   # Test unique method count
        with Timestamp_Collector() as _:
            _.enter('method_a')
            _.exit('method_a')
            _.enter('method_a')                                                    # Same method again
            _.exit('method_a')
            _.enter('method_b')
            _.exit('method_b')

            assert _.method_count() == 2                                           # Only 2 unique methods