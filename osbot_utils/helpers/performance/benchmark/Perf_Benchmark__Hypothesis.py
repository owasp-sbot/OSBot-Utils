# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Benchmark__Hypothesis - Hypothesis testing for performance improvements
# Structured experiments with baseline vs optimized code comparison
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                                   import Callable
from osbot_utils.helpers.Print_Table                                                                          import Print_Table
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Measure_Mode                               import Enum__Measure_Mode
from osbot_utils.helpers.performance.benchmark.schemas.hypothesis.Schema__Perf__Benchmark__Hypothesis__Config import Schema__Perf__Benchmark__Hypothesis__Config
from osbot_utils.helpers.performance.benchmark.schemas.hypothesis.Schema__Perf__Hypothesis__Result            import Schema__Perf__Hypothesis__Result
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description              import Safe_Str__Benchmark__Description
from osbot_utils.type_safe.Type_Safe                                                                          import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                         import Safe_Float
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path                             import Safe_Str__File__Path
from osbot_utils.utils.Files                                                                                  import file_create, file_exists
from osbot_utils.utils.Json                                                                                   import json_dumps, json_load_file
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                                         import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config          import Schema__Perf_Benchmark__Timing__Config
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results                    import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Hypothesis__Status                         import Enum__Hypothesis__Status
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Result              import Schema__Perf__Benchmark__Result


class Perf_Benchmark__Hypothesis(Type_Safe):                                     # Hypothesis tester
    config             : Schema__Perf__Benchmark__Hypothesis__Config              # Configuration settings
    description        : Safe_Str__Benchmark__Description                        # What we're testing
    target_improvement : Safe_Float                                              # e.g., 0.5 for 50%
    before_results     : Dict__Benchmark_Results                                 # Baseline measurements
    after_results      : Dict__Benchmark_Results                                 # Optimized measurements
    comments           : Safe_Str__Benchmark__Description                        # Optional notes


    # ═══════════════════════════════════════════════════════════════════════════════
    # Capture Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def run_before(self                                                     ,    # Capture baseline
                   benchmarks: Callable[[Perf_Benchmark__Timing], None]          # Benchmark function
              ) -> 'Perf_Benchmark__Hypothesis':

        timing_config = self.create_timing_config('Hypothesis Baseline')
        timing        = Perf_Benchmark__Timing(config=timing_config)
        timing.start()

        benchmarks(timing)

        timing.stop()
        self.before_results = timing.results
        return self

    def run_after(self                                                      ,    # Capture optimized
                  benchmarks: Callable[[Perf_Benchmark__Timing], None]           # Benchmark function
             ) -> 'Perf_Benchmark__Hypothesis':

        timing_config = self.create_timing_config('Hypothesis After')
        timing        = Perf_Benchmark__Timing(config=timing_config)
        timing.start()

        benchmarks(timing)

        timing.stop()
        self.after_results = timing.results
        return self

    def create_timing_config(self, title: str) -> Schema__Perf_Benchmark__Timing__Config:  # Create timing config from hypothesis config
        # Start from user's timing_config or create default
        if self.config.timing_config:
            timing_config = self.config.timing_config
        else:
            timing_config = Schema__Perf_Benchmark__Timing__Config()

        # Override specific values for hypothesis context
        timing_config.title            = title
        timing_config.print_to_console = False

        # Set measure mode based on config
        if self.config.measure_mode == Enum__Measure_Mode.QUICK:
            timing_config.measure_quick = True
            timing_config.measure_fast  = False
        elif self.config.measure_mode == Enum__Measure_Mode.FAST:
            timing_config.measure_quick = False
            timing_config.measure_fast = True                                   # TODO: implement FAST mode separately
        else:  # DEFAULT
            timing_config.measure_quick = False
            timing_config.measure_fast  = False

        return timing_config


    # ═══════════════════════════════════════════════════════════════════════════════
    # Evaluation
    # ═══════════════════════════════════════════════════════════════════════════════

    def evaluate(self) -> Schema__Perf__Hypothesis__Result:                      # Evaluate hypothesis
        if not self.before_results or len(self.before_results) == 0:
            raise ValueError('Must run before benchmarks first')
        if not self.after_results or len(self.after_results) == 0:
            raise ValueError('Must run after benchmarks first')

        improvements = []

        for benchmark_id in self.before_results.keys():
            if benchmark_id not in self.after_results:
                continue

            before_score, after_score = self.get_scores(benchmark_id)

            if before_score > 0:
                improvement = (before_score - after_score) / before_score
                improvements.append(improvement)

        if len(improvements) == 0:
            actual_improvement = 0.0
            status = Enum__Hypothesis__Status.INCONCLUSIVE
        else:
            actual_improvement = sum(improvements) / len(improvements)

            target = float(self.target_improvement) if self.target_improvement else 0.0

            if actual_improvement >= target:
                status = Enum__Hypothesis__Status.SUCCESS
            elif actual_improvement < 0:
                status = Enum__Hypothesis__Status.REGRESSION
            elif actual_improvement > 0:
                status = Enum__Hypothesis__Status.FAILURE
            else:
                status = Enum__Hypothesis__Status.INCONCLUSIVE

        return Schema__Perf__Hypothesis__Result(description        = self.description                       ,
                                                target_improvement = self.target_improvement                ,
                                                actual_improvement = Safe_Float(actual_improvement)         ,
                                                before_results     = self.before_results                    ,
                                                after_results      = self.after_results                     ,
                                                status             = status                                 ,
                                                comments           = self.comments                          )

    def get_scores(self, benchmark_id: str) -> tuple:                            # Get before/after scores based on config
        before = self.before_results[benchmark_id]
        after  = self.after_results[benchmark_id]

        if self.config.use_raw_scores:
            return int(before.raw_score), int(after.raw_score)
        else:
            return int(before.final_score), int(after.final_score)


    # ═══════════════════════════════════════════════════════════════════════════════
    # Persistence
    # ═══════════════════════════════════════════════════════════════════════════════

    def save(self, filepath: Safe_Str__File__Path) -> None:                                  # Save to file
        result = self.evaluate()
        data   = result.json()
        file_create(str(filepath), json_dumps(data, indent=2))

    @classmethod
    def load(cls, filepath: Safe_Str__File__Path) -> 'Perf_Benchmark__Hypothesis':           # Load from file
        if file_exists(str(filepath)) is False:
            return None

        data = json_load_file(str(filepath))
        if data is None:
            return None

        hypothesis = cls(description        = data.get('description', '')                    ,
                         target_improvement = Safe_Float(data.get('target_improvement', 0.0)),
                         comments           = data.get('comments', '')                       )

        hypothesis.before_results = Dict__Benchmark_Results()
        for bid, rdata in data.get('before_results', {}).items():
            hypothesis.before_results[bid] = Schema__Perf__Benchmark__Result.from_json(rdata)

        hypothesis.after_results = Dict__Benchmark_Results()
        for bid, rdata in data.get('after_results', {}).items():
            hypothesis.after_results[bid] = Schema__Perf__Benchmark__Result.from_json(rdata)

        return hypothesis


    # ═══════════════════════════════════════════════════════════════════════════════
    # Reporting
    # ═══════════════════════════════════════════════════════════════════════════════

    def build_report(self) -> str:                                               # Build full report as string
        result = self.evaluate()
        table  = Print_Table()

        table.set_title(f'HYPOTHESIS: {self.description}')
        table.add_headers('Benchmark', 'Before', 'After', 'Overhead', 'Change', 'Per-Call')

        for benchmark_id in sorted(self.before_results.keys()):
            if benchmark_id not in self.after_results:
                continue

            before_score, after_score = self.get_scores(benchmark_id)
            overhead                  = after_score - before_score

            # Calculate change percentage
            if before_score > 0:
                change_pct = ((before_score - after_score) / before_score) * 100
                if change_pct > 0:
                    change_str = f"-{change_pct:.1f}% ▼"
                elif change_pct < 0:
                    change_str = f"+{abs(change_pct):.1f}% ▲"
                else:
                    change_str = "0%"
            else:
                change_str = "N/A"

            # Calculate per-call overhead for bulk operations
            if 'x100' in benchmark_id:
                per_call     = overhead / 100
                per_call_str = f"{per_call:+,.0f} ns"
            elif 'x10' in benchmark_id:
                per_call     = overhead / 10
                per_call_str = f"{per_call:+,.0f} ns"
            else:
                per_call_str = f"{overhead:+,} ns"

            table.add_row([benchmark_id            ,
                           f'{before_score:,} ns'  ,
                           f'{after_score:,} ns'   ,
                           f'{overhead:+,} ns'     ,
                           change_str              ,
                           per_call_str            ])

        # Build footer with status and verdict
        target_pct = float(self.target_improvement) * 100 if self.target_improvement else 0
        actual_pct = float(result.actual_improvement) * 100
        status_str = result.status.value.upper()

        if result.status == Enum__Hypothesis__Status.SUCCESS:
            status_line = f"✓ {status_str} ({actual_pct:.1f}% >= {target_pct:.1f}% target)"
        elif result.status == Enum__Hypothesis__Status.REGRESSION:
            status_line = f"✗ {status_str} ({actual_pct:.1f}% - performance got worse)"
        else:
            status_line = f"✗ {status_str} ({actual_pct:.1f}% < {target_pct:.1f}% target)"

        verdict = "Per-call: <500ns ✅ | 500-1000ns ⚠️ | >1000ns ❌"
        table.set_footer(f"{status_line} | {verdict}")

        return table.text()

    def save_report(self, filepath: Safe_Str__File__Path) -> None:               # Save report to file
        file_create(str(filepath), self.build_report())

    def print_report(self) -> None:                                              # Print report to console
        print(self.build_report())