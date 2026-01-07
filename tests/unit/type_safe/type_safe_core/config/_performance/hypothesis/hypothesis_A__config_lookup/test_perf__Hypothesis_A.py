# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Hypothesis A - Config Lookup Integration
# Uses Perf_Benchmark__Hypothesis to compare baseline vs hypothesis in one test
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import List, Dict
from unittest                                                                                 import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                         import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Hypothesis                     import Perf_Benchmark__Hypothesis
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Measure_Mode               import Enum__Measure_Mode
from osbot_utils.helpers.performance.benchmark.schemas.hypothesis.Schema__Perf__Benchmark__Hypothesis__Config import Schema__Perf__Benchmark__Hypothesis__Config

from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
from osbot_utils.utils.Env                                                                    import not_in_github_action
from osbot_utils.utils.Files                                                                  import path_combine

from Type_Safe__Hypothesis_A                                                                  import Type_Safe__Hypothesis_A


# ═══════════════════════════════════════════════════════════════════════════════
# BASELINE Test Classes - Current Type_Safe (for run_before)
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Empty__Baseline(Type_Safe):                                                         # Baseline: empty
    pass

class TS__With_Primitives__Baseline(Type_Safe):                                               # Baseline: with primitives
    name   : str  = ''
    count  : int  = 0
    active : bool = False

class TS__Inner__Baseline(Type_Safe):                                                         # Baseline: inner class
    value : str = ''

class TS__With_Nested__Baseline(Type_Safe):                                                   # Baseline: with nested
    inner  : TS__Inner__Baseline
    name   : str = ''

class TS__With_Collections__Baseline(Type_Safe):                                              # Baseline: with collections
    items : List[str]
    data  : Dict[str, str]


# ═══════════════════════════════════════════════════════════════════════════════
# HYPOTHESIS Test Classes - Type_Safe__Hypothesis_A (for run_after)
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Empty__Hyp_A(Type_Safe__Hypothesis_A):                                              # Hypothesis A: empty
    pass

class TS__With_Primitives__Hyp_A(Type_Safe__Hypothesis_A):                                    # Hypothesis A: with primitives
    name   : str  = ''
    count  : int  = 0
    active : bool = False

class TS__Inner__Hyp_A(Type_Safe__Hypothesis_A):                                              # Hypothesis A: inner class
    value : str = ''

class TS__With_Nested__Hyp_A(Type_Safe__Hypothesis_A):                                        # Hypothesis A: with nested
    inner  : TS__Inner__Hyp_A
    name   : str = ''

class TS__With_Collections__Hyp_A(Type_Safe__Hypothesis_A):                                   # Hypothesis A: with collections
    items : List[str]
    data  : Dict[str, str]


# ═══════════════════════════════════════════════════════════════════════════════
# Benchmark Functions (same IDs, different implementations)
# ═══════════════════════════════════════════════════════════════════════════════

def run_baseline_benchmarks(timing: Perf_Benchmark__Timing):                                  # Baseline benchmarks
    timing.benchmark('A_01__empty'              , TS__Empty__Baseline                                        )
    timing.benchmark('A_02__with_primitives'    , TS__With_Primitives__Baseline                              )
    timing.benchmark('A_03__with_nested'        , TS__With_Nested__Baseline                                  )
    timing.benchmark('A_04__with_collections'   , TS__With_Collections__Baseline                             )
    timing.benchmark('B_01__empty_x10'          , lambda: [TS__Empty__Baseline() for _ in range(10)]         )
    timing.benchmark('B_02__empty_x100'         , lambda: [TS__Empty__Baseline() for _ in range(100)]        )
    timing.benchmark('B_03__with_primitives_x10', lambda: [TS__With_Primitives__Baseline() for _ in range(10)])
    timing.benchmark('B_04__with_nested_x10'    , lambda: [TS__With_Nested__Baseline() for _ in range(10)]   )


def run_hypothesis_benchmarks(timing: Perf_Benchmark__Timing):                                # Hypothesis benchmarks
    timing.benchmark('A_01__empty'              , TS__Empty__Hyp_A                                           )
    timing.benchmark('A_02__with_primitives'    , TS__With_Primitives__Hyp_A                                 )
    timing.benchmark('A_03__with_nested'        , TS__With_Nested__Hyp_A                                     )
    timing.benchmark('A_04__with_collections'   , TS__With_Collections__Hyp_A                                )
    timing.benchmark('B_01__empty_x10'          , lambda: [TS__Empty__Hyp_A() for _ in range(10)]            )
    timing.benchmark('B_02__empty_x100'         , lambda: [TS__Empty__Hyp_A() for _ in range(100)]           )
    timing.benchmark('B_03__with_primitives_x10', lambda: [TS__With_Primitives__Hyp_A() for _ in range(10)]  )
    timing.benchmark('B_04__with_nested_x10'    , lambda: [TS__With_Nested__Hyp_A() for _ in range(10)]      )


class test_perf__Hypothesis_A(TestCase):

    def test__hypothesis_a__config_lookup_overhead(self):
        """
        HYPOTHESIS A: Adding find_type_safe_config() to Type_Safe.__init__

        Expected: Small overhead (< 1µs per object) when no config present
        Target: 0% improvement (we're measuring overhead, not optimization)

        A negative result (regression) is expected and acceptable if < 50%
        """
        output_path = path_combine(__file__, '../')

        # Configure hypothesis settings
        config = Schema__Perf__Benchmark__Hypothesis__Config(use_raw_scores = True,                        # Use raw scores for accurate overhead measurement
                                                            measure_mode   = Enum__Measure_Mode.QUICK)    # Quick mode for faster iteration

        hypothesis = Perf_Benchmark__Hypothesis(config             = config,
                                                description        = 'Hypothesis A: Config lookup overhead in Type_Safe.__init__',
                                                target_improvement = -0.5,                    # Accept up to 50% regression (overhead)
                                                comments           = 'Testing cost of adding find_type_safe_config() call')

        # ═══════════════════════════════════════════════════════════════════════
        # Run BEFORE: Current Type_Safe (baseline)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_baseline_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Run AFTER: Type_Safe__Hypothesis_A (with config lookup)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_after(run_hypothesis_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Evaluate and Report
        # ═══════════════════════════════════════════════════════════════════════

        result = hypothesis.evaluate()

        if not_in_github_action():
            hypothesis.print_report()
            hypothesis.save_report(path_combine(output_path, 'hypothesis_a_report.txt'))
            hypothesis.save(path_combine(output_path, 'hypothesis_a_result.json'))