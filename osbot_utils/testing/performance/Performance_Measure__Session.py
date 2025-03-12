import time
from typing                                                                         import Callable, List
from statistics                                                                     import mean, median, stdev
from osbot_utils.utils.Env                                                          import in_github_action
from osbot_utils.testing.performance.models.Model__Performance_Measure__Measurement import Model__Performance_Measure__Measurement
from osbot_utils.testing.performance.models.Model__Performance_Measure__Result      import Model__Performance_Measure__Result
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe

MEASURE__INVOCATION__LOOPS = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]            # Fibonacci sequence for measurement loops

class Performance_Measure__Session(Type_Safe):
    result        : Model__Performance_Measure__Result = None                                          # Current measurement result
    assert_enabled: bool = True
    padding       : int  = 30

    def calculate_raw_score(self, times: List[int]) -> int:                                     # Calculate raw performance score
        if len(times) < 3:                                                                      # Need at least 3 values for stability
            return mean(times)

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
            return int(round(raw_score / 1000) * 1000)                                          # Under 10µs: nearest 500ns
        elif raw_score < 100_000:
            return int(round(raw_score / 10000) * 10000)                                        # Under 100µs: nearest 1000ns
        else:
            return int(round(raw_score / 100000) * 100000)                                        # Above 100µs: nearest 5000ns

    def calculate_metrics(self, times: List[int]) -> Model__Performance_Measure__Measurement:   # Calculate statistical metrics
        if not times:
            raise ValueError("Cannot calculate metrics from empty time list")
        raw_score = self.calculate_raw_score   (times)
        score     = self.calculate_stable_score(raw_score)
        return Model__Performance_Measure__Measurement(
            avg_time    = int(mean(times))                                                  ,
            min_time    = min(times)                                        ,
            max_time    = max(times)                                        ,
            median_time = int(median(times))                                ,
            stddev_time = stdev(times) if len(times) > 1 else 0             ,
            raw_times   = times                                             ,
            sample_size = len(times)                                        ,
            raw_score   = raw_score                                         ,
            score       = score                                             )

    def measure(self, target: Callable) -> 'Performance_Measure__Session':               # Perform measurements
        name         = target.__name__
        measurements = {}
        all_times    = []                                                                    # Collect all times for final score

        for loop_size in MEASURE__INVOCATION__LOOPS:                                        # Measure each loop size
            loop_times = []
            for i in range(loop_size):
                start = time.perf_counter_ns()
                target()
                end   = time.perf_counter_ns()
                time_taken = end - start
                loop_times.append(time_taken)
                all_times.append(time_taken)                                                 # Add to overall collection

            measurements[loop_size] = self.calculate_metrics(loop_times)                     # Store metrics for this loop size

        raw_score    = self.calculate_raw_score  (all_times)
        final_score = self.calculate_stable_score(raw_score)                                # Calculate final stable score

        self.result = Model__Performance_Measure__Result(
            measurements = measurements                                                      ,
            name        = name                                                              ,
            raw_score   = raw_score                                                         ,
            final_score = final_score                                                       )

        return self

    def print_measurement(self, measurement: Model__Performance_Measure__Measurement):       # Format measurement details
        print(f"Samples : {measurement.sample_size}")
        print(f"Score   : {measurement.score:,.0f}ns")
        print(f"Avg     : {measurement.avg_time:,}ns")
        print(f"Min     : {measurement.min_time:,}ns")
        print(f"Max     : {measurement.max_time:,}ns")
        print(f"Median  : {measurement.median_time:,}ns")
        print(f"StdDev  : {measurement.stddev_time:,.2f}ns")

    def print(self):                                                # Print measurement results
        if not self.result:
            print("No measurements taken yet")
            return
        print(f"{self.result.name:{self.padding}} | score: {self.result.final_score:7,d} ns  | raw: {self.result.raw_score:7,d} ns")          # Print name and normalized score

        return self

    def assert_time(self, *expected_time: int):                                              # Assert that the final score matches the expected normalized time"""
        if self.assert_enabled is False:
            return
        if in_github_action():
            last_expected_time = expected_time[-1] + 100                                    # +100 in case it is 0
            new_expected_time   = last_expected_time * 5                                    # using last_expected_time * 5 as the upper limit (since these tests are significantly slowed in GitHUb Actions)
            assert last_expected_time <=  self.result.final_score <= new_expected_time, f"Performance changed for {self.result.name}: expected {last_expected_time} < {self.result.final_score:,d}ns, expected {new_expected_time}"
        else:
            assert self.result.final_score in expected_time,  f"Performance changed for {self.result.name}: got {self.result.final_score:,d}ns, expected {expected_time}"

    def assert_time(self, *expected_time: int):                                              # Assert that the final score matches the expected normalized time"""
        if self.assert_enabled is False:
            return
        if in_github_action():
            last_expected_time = expected_time[-1] + 100                                    # +100 in case it is 0
            new_expected_time   = last_expected_time * 5                                    # using last_expected_time * 5 as the upper limit (since these tests are significantly slowed in GitHUb Actions)
            assert last_expected_time <=  self.result.final_score <= new_expected_time, f"Performance changed for {self.result.name}: expected {last_expected_time} < {self.result.final_score:,d}ns, expected {new_expected_time}"
        else:
            assert self.result.final_score in expected_time,  f"Performance changed for {self.result.name}: got {self.result.final_score:,d}ns, expected {expected_time}"

    def assert_time__less_than(self, max_time: int):                                              # Assert that the final score matches the expected normalized time"""
        if self.assert_enabled is False:
            return
        if in_github_action():
            max_time   = max_time * 6               # adjust for GitHub's slowness

        assert self.result.final_score <= max_time,  f"Performance changed for {self.result.name}: got {self.result.final_score:,d}ns, expected less than {max_time}ns"

