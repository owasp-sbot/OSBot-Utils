import time
from unittest                                                                      import TestCase
from osbot_utils.testing.Pytest                                                    import skip__if_not__in_github_actions
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector                     import Timestamp_Collector
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector__Analysis           import Timestamp_Collector__Analysis
from osbot_utils.helpers.timestamp_capture.schemas.Schema__Method_Timing           import Schema__Method_Timing
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
from osbot_utils.utils.Objects                                                     import base_classes


class test_Timestamp_Collector__Analysis(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        skip__if_not__in_github_actions()

    def test__init__(self):                                                        # Test auto-initialization
        collector = Timestamp_Collector()
        with Timestamp_Collector__Analysis(collector=collector) as _:
            assert type(_)          is Timestamp_Collector__Analysis
            assert base_classes(_)  == [Type_Safe, object]
            assert _.collector      is collector

    def test_get_method_timings__empty(self):                                      # Test with no entries
        with Timestamp_Collector() as collector:
            pass

        analysis = Timestamp_Collector__Analysis(collector=collector)
        timings  = analysis.get_method_timings()

        assert timings == {}

    def test_get_method_timings__single_method(self):                              # Test with single method
        with Timestamp_Collector() as collector:
            collector.enter('method_a')
            time.sleep(0.01)                                                       # 10ms
            collector.exit('method_a')

        analysis = Timestamp_Collector__Analysis(collector=collector)
        timings  = analysis.get_method_timings()

        assert 'method_a'                     in timings
        assert type(timings['method_a'])      is Schema__Method_Timing
        assert timings['method_a'].name       == 'method_a'
        assert timings['method_a'].call_count == 1
        assert timings['method_a'].total_ns   >= 10_000_000                        # At least 10ms

    def test_get_method_timings__multiple_calls(self):                             # Test aggregation of multiple calls
        with Timestamp_Collector() as collector:
            for _ in range(3):
                collector.enter('repeated_method')
                time.sleep(0.005)                                                  # 5ms each
                collector.exit('repeated_method')

        analysis = Timestamp_Collector__Analysis(collector=collector)
        timings  = analysis.get_method_timings()

        assert timings['repeated_method'].call_count == 3
        assert timings['repeated_method'].total_ns   >= 15_000_000                 # At least 15ms total

    def test_get_method_timings__nested_self_time(self):                           # Test self-time calculation for nested calls
        with Timestamp_Collector() as collector:
            collector.enter('outer')
            time.sleep(0.01)                                                       # 10ms in outer (before inner)

            collector.enter('inner')
            time.sleep(0.02)                                                       # 20ms in inner
            collector.exit('inner')

            time.sleep(0.01)                                                       # 10ms in outer (after inner)
            collector.exit('outer')

        analysis = Timestamp_Collector__Analysis(collector=collector)
        timings  = analysis.get_method_timings()

        outer_timing = timings['outer']
        inner_timing = timings['inner']

        assert outer_timing.total_ns >= 40_000_000                                 # ~40ms total (10+20+10)
        assert inner_timing.total_ns >= 20_000_000                                 # ~20ms total
        assert inner_timing.self_ns  >= 20_000_000                                 # Inner has no children, self == total

        # Outer's self_time should be ~20ms (total minus inner's time)
        assert outer_timing.self_ns  < outer_timing.total_ns                       # Self < Total for parent

    def test_get_method_timings__min_max(self):                                    # Test min/max tracking
        with Timestamp_Collector() as collector:
            collector.enter('variable_method')
            time.sleep(0.005)                                                      # 5ms - first call
            collector.exit('variable_method')

            collector.enter('variable_method')
            time.sleep(0.015)                                                      # 15ms - second call (longer)
            collector.exit('variable_method')

            collector.enter('variable_method')
            time.sleep(0.010)                                                      # 10ms - third call
            collector.exit('variable_method')

        analysis = Timestamp_Collector__Analysis(collector=collector)
        timings  = analysis.get_method_timings()

        timing = timings['variable_method']
        assert timing.call_count == 3
        assert timing.min_ns     <= timing.max_ns
        assert timing.min_ns     >= 5_000_000                                      # Min at least 5ms
        assert timing.max_ns     >= 15_000_000                                     # Max at least 15ms

    def test_get_hotspots(self):                                                   # Test hotspot analysis
        with Timestamp_Collector() as collector:
            collector.enter('slow_method')
            time.sleep(0.02)                                                       # 20ms
            collector.exit('slow_method')

            collector.enter('fast_method')
            time.sleep(0.005)                                                      # 5ms
            collector.exit('fast_method')

            collector.enter('medium_method')
            time.sleep(0.01)                                                       # 10ms
            collector.exit('medium_method')

        analysis = Timestamp_Collector__Analysis(collector=collector)
        hotspots = analysis.get_hotspots(top_n=3)

        assert len(hotspots) == 3
        assert hotspots[0].name == 'slow_method'                                   # Slowest first
        assert hotspots[1].name == 'medium_method'
        assert hotspots[2].name == 'fast_method'

    def test_get_hotspots__top_n(self):                                            # Test limiting hotspots
        with Timestamp_Collector() as collector:
            for i in range(5):
                collector.enter(f'method_{i}')
                time.sleep(0.001)
                collector.exit(f'method_{i}')

        analysis = Timestamp_Collector__Analysis(collector=collector)
        hotspots = analysis.get_hotspots(top_n=2)

        assert len(hotspots) == 2

    def test_get_timings_by_total(self):                                           # Test sorting by total time
        with Timestamp_Collector() as collector:
            collector.enter('short')
            time.sleep(0.005)
            collector.exit('short')

            collector.enter('long')
            time.sleep(0.015)
            collector.exit('long')

        analysis       = Timestamp_Collector__Analysis(collector=collector)
        sorted_timings = analysis.get_timings_by_total()

        assert len(sorted_timings)    == 2
        assert sorted_timings[0].name == 'long'                                    # Longest first
        assert sorted_timings[1].name == 'short'

    def test_get_timings_by_call_count(self):                                      # Test sorting by call count
        with Timestamp_Collector() as collector:
            for _ in range(5):
                collector.enter('frequent')
                collector.exit('frequent')

            for _ in range(2):
                collector.enter('infrequent')
                collector.exit('infrequent')

        analysis       = Timestamp_Collector__Analysis(collector=collector)
        sorted_timings = analysis.get_timings_by_call_count()

        assert len(sorted_timings)          == 2
        assert sorted_timings[0].name       == 'frequent'
        assert sorted_timings[0].call_count == 5
        assert sorted_timings[1].name       == 'infrequent'
        assert sorted_timings[1].call_count == 2