# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Hypothesis D - skip_conversion Flag Implementation
# Compares: skip_conversion=False vs skip_conversion=True (both with skip_validation=True)
# ═══════════════════════════════════════════════════════════════════════════════
#
# BASELINE (Before): skip_validation=True, skip_conversion=False
#                    Kwargs go through convert_value_to_type_safe_objects()
#
# HYPOTHESIS (After): skip_validation=True, skip_conversion=True
#                     Kwargs assigned directly (no conversion)
#
# NOTE: Both have skip_validation=True to isolate the conversion cost.
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import List, Dict
from unittest                                                                                 import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                         import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Hypothesis                     import Perf_Benchmark__Hypothesis
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import Type_Safe__Config, get_active_config
from osbot_utils.utils.Env                                                                    import not_in_github_action
from osbot_utils.utils.Files                                                                  import path_combine

from Type_Safe__Hypothesis_D                                                                  import Type_Safe__Hypothesis_D


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes - All inherit from Type_Safe__Hypothesis_D
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Empty(Type_Safe__Hypothesis_D):                                                     # Empty class - no kwargs impact
    pass

class TS__With_Primitives(Type_Safe__Hypothesis_D):                                           # 3 primitive attributes
    name   : str  = ''
    count  : int  = 0
    active : bool = False

class TS__Inner(Type_Safe__Hypothesis_D):                                                     # Inner class for nesting
    value : str = ''

class TS__With_Nested(Type_Safe__Hypothesis_D):                                               # With nested Type_Safe
    inner  : TS__Inner
    name   : str = ''

class TS__With_Collections(Type_Safe__Hypothesis_D):                                          # With typed collections
    items : List[str]
    data  : Dict[str, str]

class TS__Many_Primitives(Type_Safe__Hypothesis_D):                                           # 10 primitive attributes (high kwargs impact)
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

def run_baseline_benchmarks(timing: Perf_Benchmark__Timing):                                  # skip_conversion=FALSE
    with Type_Safe__Config(skip_validation=True, skip_conversion=False):                      # Conversion ON (baseline)

        # Without kwargs (should be similar)
        timing.benchmark('A_01__empty'              , TS__Empty                                        )
        timing.benchmark('A_02__with_primitives'    , TS__With_Primitives                              )
        timing.benchmark('A_03__with_nested'        , TS__With_Nested                                  )
        timing.benchmark('A_04__with_collections'   , TS__With_Collections                             )

        # WITH kwargs (should show conversion cost)
        timing.benchmark('A_05__primitives_w_kwargs', lambda: TS__With_Primitives(name='test', count=42, active=True))
        timing.benchmark('A_06__many_prims_w_kwargs', lambda: TS__Many_Primitives(
            attr_01='a', attr_02='b', attr_03='c', attr_04='d', attr_05='e',
            attr_06=1, attr_07=2, attr_08=3, attr_09=True, attr_10=False
        ))

        # Batch creation with kwargs
        timing.benchmark('B_01__primitives_w_kwargs_x10', lambda: [
            TS__With_Primitives(name='test', count=i, active=True) for i in range(10)
        ])
        timing.benchmark('B_02__many_prims_w_kwargs_x10', lambda: [
            TS__Many_Primitives(attr_01='a', attr_02='b', attr_06=i) for i in range(10)
        ])


def run_hypothesis_benchmarks(timing: Perf_Benchmark__Timing):                                # skip_conversion=TRUE
    with Type_Safe__Config(skip_validation=True, skip_conversion=True):                       # Conversion OFF (hypothesis)

        # Without kwargs (should be similar)
        timing.benchmark('A_01__empty'              , TS__Empty                                        )
        timing.benchmark('A_02__with_primitives'    , TS__With_Primitives                              )
        timing.benchmark('A_03__with_nested'        , TS__With_Nested                                  )
        timing.benchmark('A_04__with_collections'   , TS__With_Collections                             )

        # WITH kwargs (should show savings!)
        timing.benchmark('A_05__primitives_w_kwargs', lambda: TS__With_Primitives(name='test', count=42, active=True))
        timing.benchmark('A_06__many_prims_w_kwargs', lambda: TS__Many_Primitives(
            attr_01='a', attr_02='b', attr_03='c', attr_04='d', attr_05='e',
            attr_06=1, attr_07=2, attr_08=3, attr_09=True, attr_10=False
        ))

        # Batch creation with kwargs
        timing.benchmark('B_01__primitives_w_kwargs_x10', lambda: [
            TS__With_Primitives(name='test', count=i, active=True) for i in range(10)
        ])
        timing.benchmark('B_02__many_prims_w_kwargs_x10', lambda: [
            TS__Many_Primitives(attr_01='a', attr_02='b', attr_06=i) for i in range(10)
        ])


class test_perf__Hypothesis_D(TestCase):

    def test__hypothesis_d__skip_conversion(self):
        """
        HYPOTHESIS D: skip_conversion Flag Implementation

        Baseline: skip_validation=True, skip_conversion=False (conversion happens)
        Hypothesis: skip_validation=True, skip_conversion=True (conversion skipped)

        Expected: Savings when providing kwargs (conversion costs ~200-500 ns per kwarg)
        Focus: A_05, A_06, B_01, B_02 tests (with kwargs) should show improvement
        """
        output_path = path_combine(__file__, '../')

        hypothesis = Perf_Benchmark__Hypothesis(
            description        = 'Hypothesis D: skip_conversion=True vs False',
            target_improvement = 0.1,                                                         # Expect 10%+ improvement on kwargs tests
            comments           = 'Testing performance gain from skipping type conversion for kwargs'
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Run BEFORE: skip_conversion=False (full conversion)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_baseline_benchmarks)           # warm up functions
        hypothesis.run_before(run_baseline_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Run AFTER: skip_conversion=True (bypass conversion)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_after(run_hypothesis_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Evaluate and Report
        # ═══════════════════════════════════════════════════════════════════════

        if False:
            result = hypothesis.evaluate()

            if not_in_github_action():
                hypothesis.print_report()
                hypothesis.save_report(path_combine(output_path, 'hypothesis_d_report.txt'))
                hypothesis.save(path_combine(output_path, 'hypothesis_d_result.json'))

        # ═══════════════════════════════════════════════════════════════════════
        # Verify objects are created correctly
        # ═══════════════════════════════════════════════════════════════════════

        self.verify_object_creation()

    def verify_object_creation(self):                                                         # Verify objects work correctly
        # With skip_conversion=True - defaults should still work
        with Type_Safe__Config(skip_validation=True, skip_conversion=True):
            obj = TS__With_Primitives()
            assert obj.name   == ''   , f"Expected name='', got '{obj.name}'"
            assert obj.count  == 0    , f"Expected count=0, got {obj.count}"
            assert obj.active == False, f"Expected active=False, got {obj.active}"

            # Kwargs should work (just without conversion)
            obj_with_kwargs = TS__With_Primitives(name='test', count=42, active=True)
            assert obj_with_kwargs.name   == 'test', f"Expected name='test', got '{obj_with_kwargs.name}'"
            assert obj_with_kwargs.count  == 42    , f"Expected count=42, got {obj_with_kwargs.count}"
            assert obj_with_kwargs.active == True  , f"Expected active=True, got {obj_with_kwargs.active}"

        # Nested Type_Safe should still be created (via default_value, not conversion)
        with Type_Safe__Config(skip_validation=True, skip_conversion=True):
            obj_nested = TS__With_Nested()
            assert obj_nested.inner is not None, "Nested Type_Safe should still be created"
            assert isinstance(obj_nested.inner, TS__Inner), f"inner should be TS__Inner, got {type(obj_nested.inner)}"

        # Collections should still be created as defaults
        with Type_Safe__Config(skip_validation=True, skip_conversion=True):
            obj_collections = TS__With_Collections()
            assert obj_collections.items is not None, "items should be created"
            assert obj_collections.data is not None, "data should be created"

        # Both modes produce equivalent results for primitive kwargs
        with Type_Safe__Config(skip_validation=True, skip_conversion=True):
            obj_fast = TS__With_Primitives(name='compare', count=99, active=True)
        with Type_Safe__Config(skip_validation=True, skip_conversion=False):
            obj_normal = TS__With_Primitives(name='compare', count=99, active=True)

        assert obj_fast.name   == obj_normal.name  , "Fast and normal mode should produce same name"
        assert obj_fast.count  == obj_normal.count , "Fast and normal mode should produce same count"
        assert obj_fast.active == obj_normal.active, "Fast and normal mode should produce same active"