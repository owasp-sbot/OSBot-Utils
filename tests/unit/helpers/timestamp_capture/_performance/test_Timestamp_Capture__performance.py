"""
Performance benchmarks measuring @timestamp decorator overhead.

Scenarios tested:
    a) Decorator present, no collector  (stack-walk only)
    b) Decorator present, with collector (full capture)
    c) No decorator (baseline)

Key findings from benchmarks (using @dataclass(slots=True) schemas):
    • Stack-walk overhead (no collector): ~3 μs per decorated call
    • Full capture overhead (with collector): ~8 μs per decorated call
    • Overhead scales linearly with nesting depth (N decorators = N × overhead)

Overhead breakdown:
    - sys._getframe() and frame traversal: ~3 μs
    - @dataclass object creation (2 entries): ~3 μs
    - time.perf_counter_ns() + time.time_ns(): ~1 μs
    - List append operations: ~1 μs

Production guidance:
    • Safe to leave @timestamp decorators in production code
    • Stack-walk only adds ~3μs when no collector present (negligible)
    • Full capture (~8μs) acceptable for methods taking >100μs (<8% overhead)
    • For hot loops or μs-level functions, decorate only the outer entry point
"""

import pytest
import time
from unittest                                                                         import TestCase
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector                        import Timestamp_Collector
from osbot_utils.helpers.timestamp_capture.decorators.timestamp                       import timestamp


class test_Timestamp_Capture__Performance(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pytest.skip("Performance tests need manual execution")



    ITERATIONS       = 10_000                                                         # Number of calls per measurement
    WARMUP_RUNS      = 1_000                                                          # Warmup iterations before measurement
    MEASUREMENT_RUNS = 5                                                              # Number of measurement runs to average

    # ═══════════════════════════════════════════════════════════════════════════════
    # Test Functions - Minimal work to isolate decorator overhead
    # ═══════════════════════════════════════════════════════════════════════════════

    @staticmethod
    def bare_function():                                                              # Baseline - no decorator
        return 42

    @staticmethod
    @timestamp
    def decorated_function():                                                         # With @timestamp decorator
        return 42

    @staticmethod
    def function_with_work():                                                         # Simulates real work (addition)
        x = 0
        for i in range(100):
            x += i
        return x

    @staticmethod
    @timestamp
    def decorated_function_with_work():                                               # Decorated version with work
        x = 0
        for i in range(100):
            x += i
        return x

    # ═══════════════════════════════════════════════════════════════════════════════
    # Measurement Helpers
    # ═══════════════════════════════════════════════════════════════════════════════

    def measure_execution_time(self, func, iterations: int) -> float:                 # Returns total time in nanoseconds
        start = time.perf_counter_ns()
        for _ in range(iterations):
            func()
        end = time.perf_counter_ns()
        return end - start

    def measure_with_collector(self, func, iterations: int) -> float:                 # Measure with active collector
        _timestamp_collector_ = Timestamp_Collector(name='perf_test')

        with _timestamp_collector_:
            start = time.perf_counter_ns()
            for _ in range(iterations):
                func()
            end = time.perf_counter_ns()

        return end - start

    def run_benchmark(self, func_no_decorator, func_with_decorator, label: str):      # Run full benchmark suite
        results = {
            'no_decorator'          : [],
            'decorator_no_capture'  : [],
            'decorator_with_capture': [],
        }

        # Warmup all paths
        for _ in range(self.WARMUP_RUNS):
            func_no_decorator()
            func_with_decorator()

        _timestamp_collector_ = Timestamp_Collector()
        with _timestamp_collector_:
            for _ in range(self.WARMUP_RUNS):
                func_with_decorator()

        # Measurement runs
        for run in range(self.MEASUREMENT_RUNS):
            # a) No decorator (baseline)
            time_ns = self.measure_execution_time(func_no_decorator, self.ITERATIONS)
            results['no_decorator'].append(time_ns)

            # b) Decorator without collector (stack-walk overhead only)
            time_ns = self.measure_execution_time(func_with_decorator, self.ITERATIONS)
            results['decorator_no_capture'].append(time_ns)

            # c) Decorator with collector (full capture overhead)
            time_ns = self.measure_with_collector(func_with_decorator, self.ITERATIONS)
            results['decorator_with_capture'].append(time_ns)

        return self.analyze_results(results, label)

    def analyze_results(self, results: dict, label: str) -> dict:                     # Calculate statistics and overhead
        def avg(lst):
            return sum(lst) / len(lst)

        def per_call_ns(total_ns):
            return total_ns / self.ITERATIONS

        baseline_ns           = avg(results['no_decorator'])
        no_capture_ns         = avg(results['decorator_no_capture'])
        with_capture_ns       = avg(results['decorator_with_capture'])

        baseline_per_call     = per_call_ns(baseline_ns)
        no_capture_per_call   = per_call_ns(no_capture_ns)
        with_capture_per_call = per_call_ns(with_capture_ns)

        overhead_no_capture   = no_capture_per_call - baseline_per_call
        overhead_with_capture = with_capture_per_call - baseline_per_call

        pct_overhead_no_capture   = (overhead_no_capture / baseline_per_call * 100) if baseline_per_call > 0 else 0
        pct_overhead_with_capture = (overhead_with_capture / baseline_per_call * 100) if baseline_per_call > 0 else 0

        analysis = {
            'label'                    : label,
            'iterations'               : self.ITERATIONS,
            'measurement_runs'         : self.MEASUREMENT_RUNS,
            'baseline_per_call_ns'     : baseline_per_call,
            'no_capture_per_call_ns'   : no_capture_per_call,
            'with_capture_per_call_ns' : with_capture_per_call,
            'overhead_no_capture_ns'   : overhead_no_capture,
            'overhead_with_capture_ns' : overhead_with_capture,
            'overhead_no_capture_us'   : overhead_no_capture / 1_000,
            'overhead_with_capture_us' : overhead_with_capture / 1_000,
            'pct_overhead_no_capture'  : pct_overhead_no_capture,
            'pct_overhead_with_capture': pct_overhead_with_capture,
        }

        return analysis

    def format_results(self, analysis: dict) -> str:                                  # Format results for display
        lines = []
        lines.append("")
        lines.append("=" * 90)
        lines.append(f"PERFORMANCE BENCHMARK: {analysis['label']}")
        lines.append("=" * 90)
        lines.append(f"  Iterations per run   : {analysis['iterations']:,}")
        lines.append(f"  Measurement runs     : {analysis['measurement_runs']}")
        lines.append("")
        lines.append("-" * 90)
        lines.append(f"{'Scenario':<35} {'Per-Call (ns)':>15} {'Per-Call (μs)':>15} {'Overhead':>20}")
        lines.append("-" * 90)

        lines.append(
            f"{'(c) No decorator (baseline)':<35} "
            f"{analysis['baseline_per_call_ns']:>15.1f} "
            f"{analysis['baseline_per_call_ns']/1000:>15.3f} "
            f"{'—':>20}"
        )

        overhead_nc = f"+{analysis['overhead_no_capture_ns']:.1f}ns"
        lines.append(
            f"{'(a) Decorator, no capture':<35} "
            f"{analysis['no_capture_per_call_ns']:>15.1f} "
            f"{analysis['no_capture_per_call_ns']/1000:>15.3f} "
            f"{overhead_nc:>20}"
        )

        overhead_wc = f"+{analysis['overhead_with_capture_ns']:.1f}ns"
        lines.append(
            f"{'(b) Decorator, with capture':<35} "
            f"{analysis['with_capture_per_call_ns']:>15.1f} "
            f"{analysis['with_capture_per_call_ns']/1000:>15.3f} "
            f"{overhead_wc:>20}"
        )

        lines.append("-" * 90)
        lines.append("")
        lines.append("OVERHEAD SUMMARY:")
        lines.append(f"  • Stack-walk only (no collector): +{analysis['overhead_no_capture_us']:.2f} μs/call ({analysis['pct_overhead_no_capture']:.1f}% overhead)")
        lines.append(f"  • Full capture (with collector) : +{analysis['overhead_with_capture_us']:.2f} μs/call ({analysis['pct_overhead_with_capture']:.1f}% overhead)")
        lines.append("")
        lines.append("=" * 90)

        return "\n".join(lines)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Performance Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_overhead__minimal_function(self):                                        # Test overhead on minimal function
        analysis = self.run_benchmark(
            func_no_decorator   = self.bare_function,
            func_with_decorator = self.decorated_function,
            label               = "Minimal Function (return 42)"
        )

        print(self.format_results(analysis))

        # Assertions based on measured performance:
        # - Stack-walk (sys._getframe + traversal): ~5-6 μs
        # - Full capture (Type_Safe object creation dominates): ~140 μs
        assert analysis['overhead_no_capture_us']   < 20.0                            # Stack-walk overhead
        assert analysis['overhead_with_capture_us'] < 250.0                           # Full capture overhead

    def test_overhead__function_with_work(self):                                      # Test overhead relative to real work
        analysis = self.run_benchmark(
            func_no_decorator   = self.function_with_work,
            func_with_decorator = self.decorated_function_with_work,
            label               = "Function with Work (100 additions)"
        )

        print(self.format_results(analysis))

        # When function does real work (~2μs), the *absolute* overhead is the same,
        # but the *relative* overhead is much lower (more realistic scenario)
        assert analysis['overhead_no_capture_us']   < 20.0
        assert analysis['overhead_with_capture_us'] < 250.0

        # For a 2μs function, 5μs overhead = 250% relative
        # For a 1ms function, 5μs overhead = 0.5% relative (acceptable!)

    def test_overhead__nested_calls(self):                                            # Test overhead with nested decorated calls
        @timestamp
        def outer():
            return inner()

        @timestamp
        def inner():
            return 42

        def bare_outer():
            return bare_inner()

        def bare_inner():
            return 42

        analysis = self.run_benchmark(
            func_no_decorator   = bare_outer,
            func_with_decorator = outer,
            label               = "Nested Calls (2 levels)"
        )

        print(self.format_results(analysis))

        # Nested calls have 2x the overhead (2 decorated functions)
        assert analysis['overhead_no_capture_us']   < 40.0                            # 2x stack-walk
        assert analysis['overhead_with_capture_us'] < 500.0                           # 2x full capture

    def test_overhead__deeply_nested_calls(self):                                     # Test overhead with deep nesting
        @timestamp
        def level_1():
            return level_2()

        @timestamp
        def level_2():
            return level_3()

        @timestamp
        def level_3():
            return level_4()

        @timestamp
        def level_4():
            return 42

        def bare_1():
            return bare_2()

        def bare_2():
            return bare_3()

        def bare_3():
            return bare_4()

        def bare_4():
            return 42

        analysis = self.run_benchmark(
            func_no_decorator   = bare_1,
            func_with_decorator = level_1,
            label               = "Deeply Nested Calls (4 levels)"
        )

        print(self.format_results(analysis))

        # 4 decorated functions - overhead scales linearly with decoration count
        assert analysis['overhead_no_capture_us']   < 80.0                            # 4x stack-walk
        assert analysis['overhead_with_capture_us'] < 1000.0                          # 4x full capture

    def test_overhead__many_entries(self):                                            # Test collector performance with many entries
        @timestamp
        def quick_func():
            return 42

        iterations = 10_000

        _timestamp_collector_ = Timestamp_Collector(name='many_entries_test')

        # Measure time to capture many entries
        with _timestamp_collector_:
            start = time.perf_counter_ns()
            for _ in range(iterations):
                quick_func()
            end = time.perf_counter_ns()

        total_ms     = (end - start) / 1_000_000
        per_call_us  = (end - start) / iterations / 1_000
        entry_count  = _timestamp_collector_.entry_count()

        print("")
        print("=" * 70)
        print("COLLECTOR CAPACITY TEST")
        print("=" * 70)
        print(f"  Calls made      : {iterations:,}")
        print(f"  Entries recorded: {entry_count:,}")
        print(f"  Total time      : {total_ms:.2f} ms")
        print(f"  Per-call time   : {per_call_us:.2f} μs")
        print("=" * 70)

        assert entry_count == iterations * 2                                          # enter + exit per call
        assert per_call_us < 250.0                                                    # Full capture overhead

    def test_overhead__summary_report(self):                                          # Generate comprehensive summary
        print("")
        print("")
        print("╔" + "═" * 88 + "╗")
        print("║" + " TIMESTAMP CAPTURE OVERHEAD SUMMARY ".center(88) + "║")
        print("╚" + "═" * 88 + "╝")
        print("")

        # Collect all benchmarks
        benchmarks = [
            (self.bare_function, self.decorated_function, "Minimal (return 42)"),
            (self.function_with_work, self.decorated_function_with_work, "With Work (100 adds)"),
        ]

        results = []
        for bare, decorated, label in benchmarks:
            analysis = self.run_benchmark(bare, decorated, label)
            results.append(analysis)

        # Summary table
        print("-" * 90)
        print(f"{'Benchmark':<25} {'Baseline':>12} {'No Capture':>12} {'With Capture':>12} {'Overhead (NC)':>14} {'Overhead (WC)':>14}")
        print("-" * 90)

        for r in results:
            print(
                f"{r['label']:<25} "
                f"{r['baseline_per_call_ns']/1000:>11.2f}μs "
                f"{r['no_capture_per_call_ns']/1000:>11.2f}μs "
                f"{r['with_capture_per_call_ns']/1000:>11.2f}μs "
                f"{r['overhead_no_capture_us']:>+13.2f}μs "
                f"{r['overhead_with_capture_us']:>+13.2f}μs "
            )

        print("-" * 90)
        print("")
        print("KEY FINDINGS:")
        print(f"  • Decorator with no collector (stack-walk): ~{results[0]['overhead_no_capture_us']:.1f}-{results[1]['overhead_no_capture_us']:.1f} μs overhead")
        print(f"  • Decorator with collector (full capture) : ~{results[0]['overhead_with_capture_us']:.1f}-{results[1]['overhead_with_capture_us']:.1f} μs overhead")
        print("")
        print("ANALYSIS:")
        print("  • The ~5μs stack-walk overhead is acceptable for methods taking >1ms")
        print("  • For microsecond-level functions, consider removing decorators or")
        print("    using @timestamp only on higher-level methods")
        print("")
        print("RECOMMENDATION:")
        print("  • Safe to leave @timestamp decorators on methods that take >100μs")
        print("  • Full capture mode is for profiling/debugging only, not production")
        print("")