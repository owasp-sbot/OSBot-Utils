import time
from typing                                                                           import Callable, List, Optional
from statistics                                                                       import mean, median, stdev
from osbot_utils.utils.Env                                                            import in_github_action
from osbot_utils.helpers.performance.schemas.Schema__Performance_Measure__Measurement import Schema__Performance_Measure__Measurement
from osbot_utils.helpers.performance.schemas.Schema__Performance_Measure__Result      import Schema__Performance_Measure__Result
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe

MEASURE__INVOCATION__LOOPS          = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]     # Fibonacci sequence for measurement loops (1,597 total invocations)
MEASURE__INVOCATION__LOOPS__QUICK   = [1, 2, 3, 5, 8]                                             # Quick mode for slow functions (19 total invocations)
MEASURE__INVOCATION__LOOPS__FAST    = [1, 2, 3, 5, 8, 13, 21, 34]                                   # Fast mode - balanced (87 total invocations)
MEASURE__INVOCATION__LOOPS__ONLY__3 = [1, 2]                                                        # only run 3 times: 1 + 2

class Performance_Measure__Session(Type_Safe):
    result        : Schema__Performance_Measure__Result = None                                   # Current measurement result
    assert_enabled: bool                               = True
    padding       : int                                = 30

    def calculate_raw_score(self, times: List[int]) -> int:                                     # Calculate raw performance score
        if len(times) < 3:                                                                      # Need at least 3 values for stability
            return int(mean(times))

        sorted_times = sorted(times)                                                            # Sort times for analysis
        trim_size    = max(1, len(times) // 10)                                                 # Remove ~10% from each end

        trimmed      = sorted_times[trim_size:-trim_size]                                       # Remove outliers
        med          = median(trimmed)                                                          # Get median of trimmed data
        trimmed_mean = mean  (trimmed)                                                          # Get mean of trimmed data

        raw_score = int(med * 0.6 + trimmed_mean * 0.4)                                         # Weighted combination favoring median
        return raw_score

    def calculate_stable_score(self, raw_score: float) -> int:                                  # Calculate stable performance score
        if raw_score < 1_000:                                                                   # Dynamic normalization based on score magnitude
            return int(round(raw_score / 100) * 100)                                            # Under 1µs: nearest 100ns
        elif raw_score < 10_000:
            return int(round(raw_score / 1000) * 1000)                                          # Under 10µs: nearest 1000ns
        elif raw_score < 100_000:
            return int(round(raw_score / 10000) * 10000)                                        # Under 100µs: nearest 10000ns
        else:
            return int(round(raw_score / 100000) * 100000)                                      # Above 100µs: nearest 100000ns

    def calculate_metrics(self, times: List[int]) -> Schema__Performance_Measure__Measurement:   # Calculate statistical metrics
        if not times:
            raise ValueError("Cannot calculate metrics from empty time list")
        raw_score = self.calculate_raw_score   (times)
        score     = self.calculate_stable_score(raw_score)
        return Schema__Performance_Measure__Measurement(
            avg_time    = int(mean(times))                                                  ,
            min_time    = min(times)                                                        ,
            max_time    = max(times)                                                        ,
            median_time = int(median(times))                                                ,
            stddev_time = stdev(times) if len(times) > 1 else 0                             ,
            raw_times   = times                                                             ,
            sample_size = len(times)                                                        ,
            raw_score   = raw_score                                                         ,
            score       = score                                                             )

    def measure(self, target : Callable                    ,                                    # Perform measurements
                      loops  : Optional[List[int]] = None  ) -> 'Performance_Measure__Session':
        name           = target.__name__
        measurements   = {}
        all_times      = []                                                                     # Collect all times for final score
        measure_loops  = loops if loops is not None else MEASURE__INVOCATION__LOOPS             # Use custom loops or default

        for loop_size in measure_loops:                                                         # Measure each loop size
            loop_times = []
            for i in range(loop_size):
                start      = time.perf_counter_ns()
                target()
                end        = time.perf_counter_ns()
                time_taken = end - start
                loop_times.append(time_taken)
                all_times.append(time_taken)                                                    # Add to overall collection

            measurements[loop_size] = self.calculate_metrics(loop_times)                        # Store metrics for this loop size

        raw_score   = self.calculate_raw_score  (all_times)
        final_score = self.calculate_stable_score(raw_score)                                    # Calculate final stable score

        self.result = Schema__Performance_Measure__Result(
            measurements = measurements                                                         ,
            name         = name                                                                 ,
            raw_score    = raw_score                                                            ,
            final_score  = final_score                                                          )

        return self

    def measure__quick(self,
                       target : Callable
                      ) -> 'Performance_Measure__Session':
        return self.measure(target, loops=MEASURE__INVOCATION__LOOPS__QUICK)

    def measure__fast(self,
                   target : Callable
                  ) -> 'Performance_Measure__Session':
        return self.measure(target, loops=MEASURE__INVOCATION__LOOPS__FAST)

    def measure__only_3(self,
                   target : Callable
                  ) -> 'Performance_Measure__Session':
        return self.measure(target, loops=MEASURE__INVOCATION__LOOPS__ONLY__3)

    def print_measurement(self, measurement: Schema__Performance_Measure__Measurement):          # Format measurement details
        print(f"Samples : {measurement.sample_size}")
        print(f"Score   : {measurement.score:,.0f}ns")
        print(f"Avg     : {measurement.avg_time:,}ns")
        print(f"Min     : {measurement.min_time:,}ns")
        print(f"Max     : {measurement.max_time:,}ns")
        print(f"Median  : {measurement.median_time:,}ns")
        print(f"StdDev  : {measurement.stddev_time:,.2f}ns")

    def assert_time(self, *expected_time: int) -> 'Performance_Measure__Session':               # Assert that the final score matches the expected normalized time
        if self.assert_enabled is False:
            return self
        if in_github_action():
            last_expected_time = expected_time[-1]
            if last_expected_time == 0:
                last_expected_time += 100                                                       # +100 in case it is 0
            new_expected_time  = last_expected_time * 5                                         # using last_expected_time * 5 as the upper limit (since these tests are significantly slowed in GitHub Actions)
            assert last_expected_time <= self.result.final_score <= new_expected_time, f"Performance changed for {self.result.name}: expected {last_expected_time} < {self.result.final_score:,d}ns < {new_expected_time}"
        else:
            assert self.result.final_score in expected_time, f"Performance changed for {self.result.name}: got {self.result.final_score:,d}ns, expected {expected_time}"
        return self

    def assert_time__less_than(self, max_time: int) -> 'Performance_Measure__Session':          # Assert that the final score is below threshold
        if self.assert_enabled is False:
            return self
        effective_max = max_time * 6 if in_github_action() else max_time                        # adjust for GitHub's slowness
        assert self.result.final_score <= effective_max, f"Performance changed for {self.result.name}: got {self.result.final_score:,d}ns, expected less than {effective_max}ns"
        return self

    def assert_time__more_than(self, min_time: int) -> 'Performance_Measure__Session':          # Assert that the final score is above threshold
        if self.assert_enabled is False:
            return self
        assert self.result.final_score >= min_time, f"Performance changed for {self.result.name}: got {self.result.final_score:,d}ns, expected more than {min_time}ns"
        return self

    def print(self, padding: Optional[int] = None) -> 'Performance_Measure__Session':           # Print measurement results
        if not self.result:
            print("No measurements taken yet")
            return self
        pad = padding if padding is not None else self.padding
        print(f"{self.result.name:{pad}} | score: {self.result.final_score:7,d} ns  | raw: {self.result.raw_score:7,d} ns")

        return self

    def format_time(self, ns: int) -> str:                                                      # Format nanoseconds to human readable
        if ns >= 1_000_000_000:
            return f"{ns / 1_000_000_000:.3f} s"
        elif ns >= 1_000_000:
            return f"{ns / 1_000_000:.3f} ms"
        elif ns >= 1_000:
            return f"{ns / 1_000:.3f} µs"
        else:
            return f"{ns} ns"
    def print_report(self, bins: int = 10, width: int = 40) -> 'Performance_Measure__Session':  # Print detailed report with histogram
        if not self.result:
            print("No measurements taken yet")
            return self

        r = self.result
        m = r.measurements

        # Collect all raw times
        all_times = []
        for measurement in m.values():
            all_times.extend(measurement.raw_times)

        total_samples = len(all_times)
        min_time      = min(all_times)
        max_time      = max(all_times)
        avg_time      = int(mean(all_times))
        med_time      = int(median(all_times))
        std_time      = stdev(all_times) if len(all_times) > 1 else 0

        # Build histogram
        bin_size   = (max_time - min_time) / bins if max_time > min_time else 1
        bin_counts = [0] * bins

        for t in all_times:
            bin_idx = min(int((t - min_time) / bin_size), bins - 1)
            bin_counts[bin_idx] += 1

        max_count = max(bin_counts) if bin_counts else 1

        # Find which bin the score falls into
        score_bin = min(int((r.raw_score - min_time) / bin_size), bins - 1) if max_time > min_time else 0

        # Print report
        print()
        print(f"{'─' * 60}")
        print(f"  Performance Report: {r.name}")
        print(f"{'─' * 60}")
        print()
        print(f"  {'Score':<12} : {self.format_time(r.final_score):>12}   (normalized)")
        print(f"  {'Raw Score':<12} : {self.format_time(r.raw_score):>12}   (actual)")
        print()
        print(f"  {'Samples':<12} : {total_samples:>12,}")
        print(f"  {'Min':<12} : {self.format_time(min_time):>12}")
        print(f"  {'Max':<12} : {self.format_time(max_time):>12}")
        print(f"  {'Average':<12} : {self.format_time(avg_time):>12}")
        print(f"  {'Median':<12} : {self.format_time(med_time):>12}")
        print(f"  {'Std Dev':<12} : {self.format_time(int(std_time)):>12}")
        print()
        print(f"  {'Variance':<12} : {max_time / min_time:.1f}x   (max/min ratio)")
        print()
        print(f"  Distribution:                              {'count':>6}  {'%':>6}")
        print()

        # Print histogram
        for i, count in enumerate(bin_counts):
            bin_start = min_time + (i * bin_size)
            bin_end   = min_time + ((i + 1) * bin_size)
            bar_len   = int((count / max_count) * width) if max_count > 0 else 0
            bar       = '█' * bar_len
            pct       = (count / total_samples) * 100

            # Mark the bin containing the score
            marker = ' ◀ score' if i == score_bin else ''

            # Format bin range
            if count > 0:
                label = f"{self.format_time(int(bin_start)):>10} - {self.format_time(int(bin_end)):<10}"
                print(f"  {label} │{bar:<{width}} {count:>5} ({pct:>5.1f}%){marker}")

        print()
        print(f"{'─' * 60}")
        print()



Perf                = Performance_Measure__Session
perf_session        = Performance_Measure__Session
performance_session = Performance_Measure__Session
