# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Hypothesis B - NOP Type_Safe__Config in Context
# Compares: Config lookup with None vs Config lookup with actual config
# ═══════════════════════════════════════════════════════════════════════════════
#
# BASELINE (Before): Type_Safe__Hypothesis_A - NO config context
#                    find_type_safe_config() returns None
#
# HYPOTHESIS (After): Type_Safe__Hypothesis_B - WITH config context
#                     find_type_safe_config() returns Type_Safe__Config
#                     But we DON'T act on the flags yet (NOP)
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                                    import List, Dict
from unittest                                                                                                  import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                                          import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Hypothesis                                      import Perf_Benchmark__Hypothesis
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Measure_Mode                                import Enum__Measure_Mode
from osbot_utils.helpers.performance.benchmark.schemas.hypothesis.Schema__Perf__Benchmark__Hypothesis__Config  import Schema__Perf__Benchmark__Hypothesis__Config
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                                             import Type_Safe__Config
from osbot_utils.utils.Env                                                                                     import not_in_github_action
from osbot_utils.utils.Files                                                                                   import path_combine
from Type_Safe__Hypothesis_B                                                                                   import Type_Safe__Hypothesis_B


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Empty__Baseline(Type_Safe__Hypothesis_B):                                           # Baseline: empty
    pass

class TS__With_Primitives__Baseline(Type_Safe__Hypothesis_B):                                 # Baseline: with primitives
    name   : str  = ''
    count  : int  = 0
    active : bool = False

class TS__Inner__Baseline(Type_Safe__Hypothesis_B):                                           # Baseline: inner class
    value : str = ''

class TS__With_Nested__Baseline(Type_Safe__Hypothesis_B):                                     # Baseline: with nested
    inner  : TS__Inner__Baseline
    name   : str = ''

class TS__With_Collections__Baseline(Type_Safe__Hypothesis_B):                                # Baseline: with collections
    items : List[str]
    data  : Dict[str, str]


# ═══════════════════════════════════════════════════════════════════════════════
# Benchmark Functions
# ═══════════════════════════════════════════════════════════════════════════════

def run_baseline_benchmarks(timing: Perf_Benchmark__Timing):                                    # NO context - config returns None
        timing.benchmark('A_01__empty'              , TS__Empty__Baseline                                        )
        timing.benchmark('A_02__with_primitives'    , TS__With_Primitives__Baseline                              )
        timing.benchmark('A_03__with_nested'        , TS__With_Nested__Baseline                                  )
        timing.benchmark('A_04__with_collections'   , TS__With_Collections__Baseline                             )
        timing.benchmark('B_01__empty_x10'          , lambda: [TS__Empty__Baseline() for _ in range(10)]         )
        timing.benchmark('B_02__empty_x100'         , lambda: [TS__Empty__Baseline() for _ in range(100)]        )
        timing.benchmark('B_03__with_primitives_x10', lambda: [TS__With_Primitives__Baseline() for _ in range(10)])
        timing.benchmark('B_04__with_nested_x10'    , lambda: [TS__With_Nested__Baseline() for _ in range(10)]   )

def run_hypothesis_benchmarks(timing: Perf_Benchmark__Timing):                                   # WITH context - config returns object
    with Type_Safe__Config(skip_validation=True):                                                # Config IS present (but NOP)
        timing.benchmark('A_01__empty'              , TS__Empty__Baseline                                        )
        timing.benchmark('A_02__with_primitives'    , TS__With_Primitives__Baseline                              )
        timing.benchmark('A_03__with_nested'        , TS__With_Nested__Baseline                                  )
        timing.benchmark('A_04__with_collections'   , TS__With_Collections__Baseline                             )
        timing.benchmark('B_01__empty_x10'          , lambda: [TS__Empty__Baseline() for _ in range(10)]         )
        timing.benchmark('B_02__empty_x100'         , lambda: [TS__Empty__Baseline() for _ in range(100)]        )
        timing.benchmark('B_03__with_primitives_x10', lambda: [TS__With_Primitives__Baseline() for _ in range(10)])
        timing.benchmark('B_04__with_nested_x10'    , lambda: [TS__With_Nested__Baseline() for _ in range(10)]   )


class test_perf__Hypothesis_B(TestCase):

    def test__hypothesis_b__nop_config_in_context(self):
        """
        HYPOTHESIS B: NOP Type_Safe__Config in Context

        Baseline: find_type_safe_config() returns None (no context)
        Hypothesis: find_type_safe_config() returns Type_Safe__Config (with context)

        Expected: ~0 ns difference (thread-local getattr same speed either way)
        Target: < 100 ns additional overhead
        """
        output_path        = path_combine(__file__, '../')
        hypothesis__config = Schema__Perf__Benchmark__Hypothesis__Config(measure_mode   = Enum__Measure_Mode.FAST)
        hypothesis         = Perf_Benchmark__Hypothesis(description        = 'Hypothesis B: NOP config in context vs no context'       ,
                                                        target_improvement = -0.1                                                      ,   # Accept up to 10% regression
                                                        comments           = 'Testing if having config present (vs None) adds overhead',
                                                        config             = hypothesis__config)

        # ═══════════════════════════════════════════════════════════════════════
        # Run BEFORE: No config context (find_type_safe_config returns None)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_baseline_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Run AFTER: With config context (find_type_safe_config returns config)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_after(run_hypothesis_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Evaluate and Report
        # ═══════════════════════════════════════════════════════════════════════

        if False: # disabling so that we don't overwrite the results
            result = hypothesis.evaluate()

            if not_in_github_action():
                hypothesis.print_report()
                hypothesis.save_report(path_combine(output_path, 'hypothesis_b_report.txt'))
                hypothesis.save(path_combine(output_path, 'hypothesis_b_result.json'))

        # ═══════════════════════════════════════════════════════════════════════
        # Verify config is actually found in hypothesis run
        # ═══════════════════════════════════════════════════════════════════════

        self.verify_config_discovery()

    def verify_config_discovery(self):                                                        # Verify config is found correctly
        # print("\n")
        # print("═" * 70)
        # print(" Config Discovery Verification")
        # print("═" * 70)

        # Without context
        obj_no_context = TS__Empty__Baseline()
        config_none = getattr(obj_no_context, '__hypothesis_config__', 'NOT_SET')
        #print(f"  Without context: __hypothesis_config__ = {config_none}")
        assert config_none is None, "Should be None without context"

        # With context
        with Type_Safe__Config(skip_validation=True) as ctx:
            obj_with_context = TS__Empty__Baseline()
            config_found = getattr(obj_with_context, '__hypothesis_config__', 'NOT_SET')
            assert config_found is not None
            #print(f"  With context:    __hypothesis_config__ = {config_found}")
            assert config_found is ctx, "Should find the context config"
            assert config_found.skip_validation == True, "skip_validation should be True"

        # print("  ✓ Config discovery working correctly")
        # print("═" * 70)
        # print()