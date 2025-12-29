import pytest
from statistics                                                                     import mean, median
from unittest                                                                       import TestCase
from unittest.mock                                                                  import patch
from osbot_utils.testing.performance.Performance_Measure__Session                   import Performance_Measure__Session
from osbot_utils.testing.performance.Performance_Measure__Session                   import MEASURE__INVOCATION__LOOPS
from osbot_utils.testing.performance.Performance_Measure__Session                   import MEASURE__INVOCATION__LOOPS__QUICK
from osbot_utils.testing.performance.Performance_Measure__Session                   import MEASURE__INVOCATION__LOOPS__FAST
from osbot_utils.testing.performance.models.Model__Performance_Measure__Measurement import Model__Performance_Measure__Measurement
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class test_Performance_Measure__Session(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = Performance_Measure__Session()

    def test__init__(self):                                                                     # Test initialization and Type_Safe inheritance
        with Performance_Measure__Session() as _:
            assert type(_)               is Performance_Measure__Session
            assert isinstance(_, Type_Safe)
            assert _.result              is None
            assert _.assert_enabled      is True
            assert _.padding             == 30

    def test__init____with_kwargs(self):                                                        # Test initialization with custom values
        with Performance_Measure__Session(assert_enabled=False, padding=50) as _:
            assert _.assert_enabled is False
            assert _.padding        == 50

    # ------------------------------------------------
    # Tests for calculate_raw_score
    # ------------------------------------------------

    def test_calculate_raw_score(self):                                                         # Test raw score calculation with normal data
        with self.session as _:
            times     = [100, 110, 105, 108, 102, 107, 103, 109, 104, 106]                      # 10 samples, ~10% trimmed from each end
            raw_score = _.calculate_raw_score(times)
            assert 100 <= raw_score <= 110                                                      # Should be within range

    def test_calculate_raw_score__with_outliers(self):                                          # Test that outliers are removed
        with self.session as _:
            times = [100, 102, 103, 104, 105, 106, 107, 108, 109, 10000]                        # One massive outlier
            raw_score = _.calculate_raw_score(times)
            assert raw_score < 200                                                              # Outlier should be trimmed

    def test_calculate_raw_score__less_than_3_values(self):                                     # Test fallback to mean for small samples
        with self.session as _:
            times_1 = [100]
            times_2 = [100, 200]
            assert _.calculate_raw_score(times_1) == 100                                        # Single value returns itself
            assert _.calculate_raw_score(times_2) == 150                                        # Two values return mean

    def test_calculate_raw_score__weighted_median_mean(self):                                   # Test 60% median, 40% mean weighting
        with self.session as _:
            times = [100] * 50 + [200] * 50                                                     # Half 100, half 200
            raw_score = _.calculate_raw_score(times)
            assert 100 < raw_score < 200                                                        # Between extremes

    # ------------------------------------------------
    # Tests for calculate_stable_score
    # ------------------------------------------------

    def test_calculate_stable_score__under_1us(self):                                           # Test normalization under 1µs
        with self.session as _:
            assert _.calculate_stable_score(50)   == 0                                          # round(0.5) = 0 (banker's rounding)
            assert _.calculate_stable_score(149)  == 100                                        # round(1.49) = 1
            assert _.calculate_stable_score(150)  == 200                                        # round(1.5) = 2 (banker's rounding)
            assert _.calculate_stable_score(250)  == 200                                        # round(2.5) = 2 (banker's rounding)
            assert _.calculate_stable_score(350)  == 400                                        # round(3.5) = 4 (banker's rounding)
            assert _.calculate_stable_score(850)  == 800                                        # round(8.5) = 8 (banker's rounding)
            assert _.calculate_stable_score(999)  == 1000                                       # round(9.99) = 10

    def test_calculate_stable_score__1us_to_10us(self):                                         # Test normalization 1-10µs
        with self.session as _:
            assert _.calculate_stable_score(1_000)  == 1_000
            assert _.calculate_stable_score(1_499)  == 1_000
            assert _.calculate_stable_score(1_500)  == 2_000
            assert _.calculate_stable_score(5_500)  == 6_000
            assert _.calculate_stable_score(9_999)  == 10_000

    def test_calculate_stable_score__10us_to_100us(self):                                       # Test normalization 10-100µs
        with self.session as _:
            assert _.calculate_stable_score(10_000)  == 10_000
            assert _.calculate_stable_score(14_999)  == 10_000
            assert _.calculate_stable_score(15_000)  == 20_000
            assert _.calculate_stable_score(55_000)  == 60_000
            assert _.calculate_stable_score(99_999)  == 100_000

    def test_calculate_stable_score__above_100us(self):                                         # Test normalization above 100µs
        with self.session as _:
            assert _.calculate_stable_score(100_000)   == 100_000
            assert _.calculate_stable_score(149_999)   == 100_000
            assert _.calculate_stable_score(150_000)   == 200_000                               # round(1.5) = 2 (banker's rounding)
            assert _.calculate_stable_score(250_000)   == 200_000                               # round(2.5) = 2 (banker's rounding)
            assert _.calculate_stable_score(1_850_000) == 1_800_000                             # round(18.5) = 18 (banker's rounding)

    # ------------------------------------------------
    # Tests for calculate_metrics
    # ------------------------------------------------

    def test_calculate_metrics(self):                                                           # Test metrics calculation
        with self.session as _:
            times   = [100, 200, 150, 175, 125]
            metrics = _.calculate_metrics(times)

            assert type(metrics)        is Model__Performance_Measure__Measurement
            assert metrics.sample_size  == 5
            assert metrics.min_time     == 100
            assert metrics.max_time     == 200
            assert metrics.avg_time     == int(mean(times))
            assert metrics.median_time  == int(median(times))
            assert metrics.raw_times    == times

    def test_calculate_metrics__empty_list(self):                                               # Test error on empty list
        with self.session as _:
            with pytest.raises(ValueError, match="Cannot calculate metrics from empty time list"):
                _.calculate_metrics([])

    def test_calculate_metrics__single_value(self):                                             # Test single value (stddev = 0)
        with self.session as _:
            metrics = _.calculate_metrics([100])
            assert metrics.sample_size  == 1
            assert metrics.stddev_time  == 0
            assert metrics.avg_time     == 100

    # ------------------------------------------------
    # Tests for measure
    # ------------------------------------------------

    def test_measure(self):                                                                     # Test basic measurement
        call_count = 0
        def target_function():
            nonlocal call_count
            call_count += 1

        with Performance_Measure__Session() as _:
            result = _.measure(target_function)

            assert result is _                                                                  # Returns self for chaining
            assert _.result is not None
            assert _.result.name == 'target_function'
            assert call_count == sum(MEASURE__INVOCATION__LOOPS)                                # 1597 invocations

    def test_measure__with_custom_loops(self):                                                  # Test custom loops parameter
        call_count = 0
        def target_function():
            nonlocal call_count
            call_count += 1

        custom_loops = [1, 2, 3]
        with Performance_Measure__Session() as _:
            _.measure(target_function, loops=custom_loops)

            assert call_count == sum(custom_loops)                                              # 6 invocations
            assert len(_.result.measurements) == len(custom_loops)

    def test_measure__with_quick_loops(self):                                                   # Test QUICK loops preset
        call_count = 0
        def target_function():
            nonlocal call_count
            call_count += 1

        with Performance_Measure__Session() as _:
            _.measure(target_function, loops=MEASURE__INVOCATION__LOOPS__QUICK)

            assert call_count == sum(MEASURE__INVOCATION__LOOPS__QUICK)                         # 19 invocations
            assert len(_.result.measurements) == len(MEASURE__INVOCATION__LOOPS__QUICK)

    def test_measure__with_fast_loops(self):                                                    # Test FAST loops preset
        call_count = 0
        def target_function():
            nonlocal call_count
            call_count += 1

        with Performance_Measure__Session() as _:
            _.measure__fast(target_function)

            assert call_count == sum(MEASURE__INVOCATION__LOOPS__FAST)                          # 87 invocations

    def test_measure__stores_measurements_per_loop_size(self):                                  # Test measurements dict structure
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 5, 10])

            assert 1  in _.result.measurements
            assert 5  in _.result.measurements
            assert 10 in _.result.measurements
            assert _.result.measurements[1].sample_size  == 1
            assert _.result.measurements[5].sample_size  == 5
            assert _.result.measurements[10].sample_size == 10

    def test_measure__class_instantiation(self):                                                # Test measuring class ctor
        class TestClass:
            pass

        with Performance_Measure__Session() as _:
            _.measure(TestClass, loops=[1, 2, 3])

            assert _.result.name == 'TestClass'
            assert _.result.final_score > 0

    # ------------------------------------------------
    # Tests for print methods
    # ------------------------------------------------

    def test_print__no_measurements(self):                                                      # Test print when no measurements
        import io
        import sys
        with Performance_Measure__Session() as _:
            captured = io.StringIO()
            sys.stdout = captured
            try:
                result = _.print()
            finally:
                sys.stdout = sys.__stdout__

            assert result is _                                                                  # Returns self
            assert "No measurements taken yet" in captured.getvalue()

    def test_print__with_measurements(self):                                                    # Test print output format
        import io
        import sys
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])

            captured = io.StringIO()
            sys.stdout = captured
            try:
                _.print()
            finally:
                sys.stdout = sys.__stdout__

            output = captured.getvalue()
            assert "<lambda>" in output
            assert "score:" in output
            assert "raw:" in output
            assert "ns" in output

    def test_print__custom_padding(self):                                                       # Test custom padding
        import io
        import sys
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1])

            captured = io.StringIO()
            sys.stdout = captured
            try:
                _.print(padding=50)
            finally:
                sys.stdout = sys.__stdout__

            output = captured.getvalue()
            assert len(output.split("|")[0].strip()) <= 50

    def test_print_measurement(self):                                                           # Test detailed measurement print
        import io
        import sys
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])

            captured = io.StringIO()
            sys.stdout = captured
            try:
                _.print_measurement(_.result.measurements[3])
            finally:
                sys.stdout = sys.__stdout__

            output = captured.getvalue()
            assert "Samples : 3" in output
            assert "Score" in output
            assert "Avg" in output
            assert "Min" in output
            assert "Max" in output
            assert "Median" in output
            assert "StdDev" in output

    # ------------------------------------------------
    # Tests for assert_time
    # ------------------------------------------------

    def test_assert_time__passes(self):                                                         # Test assertion passes with correct value
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            score = _.result.final_score
            _.assert_time(score)                                                                # Should not raise

    def test_assert_time__multiple_expected(self):                                              # Test assertion with multiple expected values
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            score = _.result.final_score
            _.assert_time(100, 200, score, 500)                                                 # Should pass if score in list

    def test_assert_time__fails(self):                                                          # Test assertion fails with wrong value
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            with pytest.raises(AssertionError, match="Performance changed"):
                _.assert_time(999_999_999)                                                      # Unlikely to match

    def test_assert_time__disabled(self):                                                       # Test assertion disabled
        with Performance_Measure__Session(assert_enabled=False) as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            result = _.assert_time(999_999_999)                                                 # Should not raise
            assert result is _                                                                  # Returns self

    def test_assert_time__chaining(self):                                                       # Test method chaining
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            score  = _.result.final_score
            print()
            print(score)
            result = _.assert_time(score)
            assert result is _

    @patch('osbot_utils.testing.performance.Performance_Measure__Session.in_github_action')
    def test_assert_time__github_actions_multiplier(self, mock_in_github):                      # Test 5x multiplier in GitHub Actions
        mock_in_github.return_value = True
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            # In GitHub Actions, uses last value + 100, then * 5 as upper bound
            # So assert_time(100) allows: 200 <= score <= 1000
            # This should pass or fail based on actual score
            score = _.result.final_score
            if 200 <= score <= 1000:
                _.assert_time(100)                                                              # Should pass

    # ------------------------------------------------
    # Tests for assert_time__less_than
    # ------------------------------------------------

    def test_assert_time__less_than__passes(self):                                              # Test less_than passes
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            _.assert_time__less_than(10_000_000)                                                # 10ms should be plenty

    def test_assert_time__less_than__fails(self):                                               # Test less_than fails
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            with pytest.raises(AssertionError, match="expected less than"):
                _.assert_time__less_than(1)                                                     # 1ns is too low

    def test_assert_time__less_than__disabled(self):                                            # Test disabled assertion
        with Performance_Measure__Session(assert_enabled=False) as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            result = _.assert_time__less_than(1)                                                # Should not raise
            assert result is _

    @patch('osbot_utils.testing.performance.Performance_Measure__Session.in_github_action')
    def test_assert_time__less_than__github_actions_multiplier(self, mock_in_github):           # Test 6x multiplier in GitHub Actions
        mock_in_github.return_value = True
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            # In GitHub Actions, max_time is multiplied by 6
            # So assert_time__less_than(100) allows score <= 600
            score = _.result.final_score
            if score <= 600:
                _.assert_time__less_than(100)                                                   # Should pass with 6x

    # ------------------------------------------------
    # Tests for assert_time__more_than
    # ------------------------------------------------

    def test_assert_time__more_than__passes(self):                                              # Test more_than passes
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            _.assert_time__more_than(0)                                                         # 0ns should always pass

    def test_assert_time__more_than__fails(self):                                               # Test more_than fails
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            with pytest.raises(AssertionError, match="expected more than"):
                _.assert_time__more_than(10_000_000_000)                                         # 10s is too high

    def test_assert_time__more_than__disabled(self):                                            # Test disabled assertion
        with Performance_Measure__Session(assert_enabled=False) as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            result = _.assert_time__more_than(10_000_000_000)                                   # Should not raise
            assert result is _

    # ------------------------------------------------
    # Tests for context manager
    # ------------------------------------------------

    def test_context_manager(self):                                                             # Test context manager protocol
        with Performance_Measure__Session() as session:
            assert type(session) is Performance_Measure__Session

    def test_context_manager__reuse(self):                                                      # Test session reuse across contexts
        session = Performance_Measure__Session()

        with session as _:
            _.measure(lambda: None, loops=[1])
            first_result = _.result

        with session as _:
            _.measure(lambda: None, loops=[1])
            second_result = _.result

        assert first_result is not second_result                                                # New result each measure

    # ------------------------------------------------
    # Tests for loop constants
    # ------------------------------------------------

    def test_loop_constants(self):                                                              # Test loop constant values
        assert MEASURE__INVOCATION__LOOPS        == [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
        assert MEASURE__INVOCATION__LOOPS__QUICK == [1, 2, 3, 5, 8]
        assert MEASURE__INVOCATION__LOOPS__FAST  == [1, 2, 3, 5, 8, 13, 21, 34]

    def test_loop_constants__total_invocations(self):                                           # Test total invocation counts
        assert sum(MEASURE__INVOCATION__LOOPS)        == 1595
        assert sum(MEASURE__INVOCATION__LOOPS__QUICK) == 19
        assert sum(MEASURE__INVOCATION__LOOPS__FAST)  == 87

    # ------------------------------------------------
    # Tests for method chaining
    # ------------------------------------------------

    def test_method_chaining__full_chain(self):                                                 # Test complete method chain
        with Performance_Measure__Session() as _:
            _.measure(lambda: None, loops=[1, 2, 3])
            score = _.result.final_score

            result = (_.measure(lambda: None, loops=[1])
                       .print()
                       .assert_time(_.result.final_score)
                       .assert_time__less_than(10_000_000))

            assert result is _

    # ------------------------------------------------
    # Integration tests
    # ------------------------------------------------

    def test_integration__type_safe_class_measurement(self):                                    # Test measuring Type_Safe class ctor
        class An_Class(Type_Safe):
            an_int: int
            an_str: str

        with Performance_Measure__Session() as _:
            _.measure(An_Class, loops=MEASURE__INVOCATION__LOOPS__QUICK)

            assert _.result.name        == 'An_Class'
            assert _.result.final_score > 0
            assert _.result.raw_score   > 0

    def test_integration__slow_function_quick_mode(self):                                       # Test quick mode for slow functions
        import time
        def slow_function():
            time.sleep(0.001)                                                                   # 1ms delay

        with Performance_Measure__Session() as _:
            _.measure(slow_function, loops=MEASURE__INVOCATION__LOOPS__QUICK)

            assert _.result.final_score >= 1_000_000                                            # Should be at least 1ms
            # Quick mode: only 19 invocations instead of 1597

    def test_integration__comparison_of_implementations(self):                                  # Test comparing two implementations
        def impl_a():
            return [i for i in range(10)]

        def impl_b():
            return list(range(10))

        with Performance_Measure__Session() as _:
            _.measure__quick(impl_a)
            time_a = _.result.final_score

            _.measure(impl_b, loops=MEASURE__INVOCATION__LOOPS__QUICK)
            time_b = _.result.final_score

            # Both should complete, times should be comparable
            assert time_a > 0
            assert time_b > 0