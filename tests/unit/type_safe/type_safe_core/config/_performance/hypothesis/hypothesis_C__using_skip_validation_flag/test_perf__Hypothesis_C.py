# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Hypothesis C - skip_validation Flag Implementation
# Compares: Normal validation vs skip_validation=True
# ═══════════════════════════════════════════════════════════════════════════════
#
# BASELINE (Before): Type_Safe__Hypothesis_C with skip_validation=False
#                    Full Type_Safe validation machinery runs
#
# HYPOTHESIS (After): Type_Safe__Hypothesis_C with skip_validation=True
#                     Bypasses validation, uses object.__setattr__ directly
#
# Expected: ~600 ns savings per attribute (break-even at 1 attribute)
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import List, Dict
from unittest                                                                                 import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                         import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Hypothesis                     import Perf_Benchmark__Hypothesis
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import Type_Safe__Config, get_active_config
from osbot_utils.utils.Env                                                                    import not_in_github_action
from osbot_utils.utils.Files                                                                  import path_combine

from Type_Safe__Hypothesis_C                                                                  import Type_Safe__Hypothesis_C


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes - All inherit from Type_Safe__Hypothesis_C
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Empty(Type_Safe__Hypothesis_C):                                                     # Empty class
    pass

class TS__With_Primitives(Type_Safe__Hypothesis_C):                                           # 3 primitive attributes
    name   : str  = ''
    count  : int  = 0
    active : bool = False

class TS__Inner(Type_Safe__Hypothesis_C):                                                     # Inner class for nesting
    value : str = ''

class TS__With_Nested(Type_Safe__Hypothesis_C):                                               # With nested Type_Safe
    inner  : TS__Inner
    name   : str = ''

class TS__With_Collections(Type_Safe__Hypothesis_C):                                          # With typed collections
    items : List[str]
    data  : Dict[str, str]

class TS__Many_Attributes(Type_Safe__Hypothesis_C):                                           # 10 attributes (high savings expected)
    attr_01 : str  = ''
    attr_02 : str  = ''
    attr_03 : str  = ''
    attr_04 : str  = ''
    attr_05 : str  = ''
    attr_06 : int  = 0
    attr_07 : int  = 0
    attr_08 : int  = 0
    attr_09 : bool = False
    attr_10 : bool = False


# ═══════════════════════════════════════════════════════════════════════════════
# Benchmark Functions
# ═══════════════════════════════════════════════════════════════════════════════

def run_baseline_benchmarks(timing: Perf_Benchmark__Timing):                                  # skip_validation=FALSE
    with Type_Safe__Config(skip_validation=False):                                            # Full validation (baseline)
        timing.benchmark('A_01__empty'              , TS__Empty                                        )
        timing.benchmark('A_02__with_primitives'    , TS__With_Primitives                              )
        timing.benchmark('A_03__with_nested'        , TS__With_Nested                                  )
        timing.benchmark('A_04__with_collections'   , TS__With_Collections                             )
        timing.benchmark('A_05__many_attributes'    , TS__Many_Attributes                              )
        timing.benchmark('B_01__empty_x10'          , lambda: [TS__Empty() for _ in range(10)]         )
        timing.benchmark('B_02__empty_x100'         , lambda: [TS__Empty() for _ in range(100)]        )
        timing.benchmark('B_03__with_primitives_x10', lambda: [TS__With_Primitives() for _ in range(10)])
        timing.benchmark('B_04__with_nested_x10'    , lambda: [TS__With_Nested() for _ in range(10)]   )
        timing.benchmark('B_05__many_attributes_x10', lambda: [TS__Many_Attributes() for _ in range(10)])


def run_hypothesis_benchmarks(timing: Perf_Benchmark__Timing):                                # skip_validation=TRUE
    with Type_Safe__Config(skip_validation=True):                                             # SKIP validation (hypothesis)
        timing.benchmark('A_01__empty'              , TS__Empty                                        )
        timing.benchmark('A_02__with_primitives'    , TS__With_Primitives                              )
        timing.benchmark('A_03__with_nested'        , TS__With_Nested                                  )
        timing.benchmark('A_04__with_collections'   , TS__With_Collections                             )
        timing.benchmark('A_05__many_attributes'    , TS__Many_Attributes                              )
        timing.benchmark('B_01__empty_x10'          , lambda: [TS__Empty() for _ in range(10)]         )
        timing.benchmark('B_02__empty_x100'         , lambda: [TS__Empty() for _ in range(100)]        )
        timing.benchmark('B_03__with_primitives_x10', lambda: [TS__With_Primitives() for _ in range(10)])
        timing.benchmark('B_04__with_nested_x10'    , lambda: [TS__With_Nested() for _ in range(10)]   )
        timing.benchmark('B_05__many_attributes_x10', lambda: [TS__Many_Attributes() for _ in range(10)])


class test_perf__Hypothesis_C(TestCase):

    def test__hypothesis_c__skip_validation(self):
        """
        HYPOTHESIS C: skip_validation Flag Implementation

        Baseline: skip_validation=False (full Type_Safe validation)
        Hypothesis: skip_validation=True (bypass validation machinery)

        Expected: ~600 ns savings per attribute
        Break-even: 1 attribute (need to recover ~350 ns config overhead)
        """
        output_path = path_combine(__file__, '../')

        hypothesis = Perf_Benchmark__Hypothesis(
            description        = 'Hypothesis C: skip_validation=True vs False',
            target_improvement = 0.2,                                                         # Expect 20%+ improvement
            comments           = 'Testing performance gain from skipping validation'
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Run BEFORE: skip_validation=False (full validation)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_baseline_benchmarks)                                  # warm up functions
        hypothesis.run_before(run_baseline_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Run AFTER: skip_validation=True (bypass validation)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_after(run_hypothesis_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Evaluate and Report
        # ═══════════════════════════════════════════════════════════════════════

        if False:
            result = hypothesis.evaluate()

            if not_in_github_action():
                hypothesis.print_report()
                hypothesis.save_report(path_combine(output_path, 'hypothesis_c_report.txt'))
                hypothesis.save(path_combine(output_path, 'hypothesis_c_result.json'))

        # ═══════════════════════════════════════════════════════════════════════
        # Verify objects are created correctly
        # ═══════════════════════════════════════════════════════════════════════

        self.verify_object_creation()

    def verify_object_creation(self):
        # With skip_validation=True
        with Type_Safe__Config(skip_validation=True):
            obj = TS__With_Primitives()
            assert obj.name   == ''   , f"Expected name='', got '{obj.name}'"
            assert obj.count  == 0    , f"Expected count=0, got {obj.count}"
            assert obj.active == False, f"Expected active=False, got {obj.active}"

            obj_with_kwargs = TS__With_Primitives(name='test', count=42, active=True)
            assert obj_with_kwargs.name   == 'test', f"Expected name='test', got ..."
            assert obj_with_kwargs.count  == 42    , f"Expected count=42, got ..."
            assert obj_with_kwargs.active == True  , f"Expected active=True, got ..."

        # With skip_validation=False (normal)
        with Type_Safe__Config(skip_validation=False):
            obj_normal = TS__With_Primitives()
            assert obj_normal.name   == '', ...
            assert obj_normal.count  == 0 , ...
            assert obj_normal.active == False, ...

        # Verify both modes produce equivalent objects
        with Type_Safe__Config(skip_validation=True):
            obj_fast = TS__With_Primitives(name='compare', count=99, active=True)
        with Type_Safe__Config(skip_validation=False):
            obj_normal = TS__With_Primitives(name='compare', count=99, active=True)

        assert obj_fast.name   == obj_normal.name  , "Fast and normal mode should produce same name"
        assert obj_fast.count  == obj_normal.count , "Fast and normal mode should produce same count"
        assert obj_fast.active == obj_normal.active, "Fast and normal mode should produce same active"