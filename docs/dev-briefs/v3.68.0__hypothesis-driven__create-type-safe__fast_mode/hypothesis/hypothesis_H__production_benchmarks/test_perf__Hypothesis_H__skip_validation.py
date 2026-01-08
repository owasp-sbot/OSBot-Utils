# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Hypothesis H - Default vs skip_validation
# Compares: Normal Type_Safe vs skip_validation=True (during __setattr__)
# ═══════════════════════════════════════════════════════════════════════════════
#
# BASELINE (Before): Normal Type_Safe.__setattr__ (full validation)
#
# HYPOTHESIS (After): skip_validation=True (direct object.__setattr__)
#
# NOTE: This tests POST-CREATION attribute assignment performance
#       Not object creation itself
#
# NOTE: Uses REAL Type_Safe with wiring in place (not prototype subclass)
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                       import Dict, List
from unittest                                                                     import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing             import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Hypothesis         import Perf_Benchmark__Hypothesis
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                import Type_Safe__Config
from osbot_utils.type_safe.type_safe_core.fast_create.Type_Safe__Fast_Create__Cache import type_safe_fast_create_cache
from osbot_utils.utils.Env                                                        import not_in_github_action
from osbot_utils.utils.Files                                                      import path_combine


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Simple(Type_Safe):
    name   : str   = ''
    count  : int   = 0
    active : bool  = False
    value  : float = 0.0


class TS__Many_Fields(Type_Safe):
    field_01 : str  = ''
    field_02 : str  = ''
    field_03 : str  = ''
    field_04 : str  = ''
    field_05 : str  = ''
    field_06 : int  = 0
    field_07 : int  = 0
    field_08 : int  = 0
    field_09 : bool = False
    field_10 : bool = False


class TS__Inner(Type_Safe):
    value : str = ''
    count : int = 0


class TS__With_Nested(Type_Safe):
    inner : TS__Inner
    name  : str = ''


# ═══════════════════════════════════════════════════════════════════════════════
# Benchmark Functions
# ═══════════════════════════════════════════════════════════════════════════════

def run_baseline_benchmarks(timing: Perf_Benchmark__Timing):                      # Default __setattr__
    # Create objects first (outside benchmark)
    simple_objs = [TS__Simple() for _ in range(100)]
    many_objs   = [TS__Many_Fields() for _ in range(100)]
    nested_objs = [TS__With_Nested() for _ in range(100)]

    # No config = normal Type_Safe behavior (full validation on setattr)

    def assign_simple():
        for obj in simple_objs:
            obj.name   = 'updated'
            obj.count  = 42
            obj.active = True
            obj.value  = 3.14

    def assign_many_fields():
        for obj in many_objs:
            obj.field_01 = 'a'
            obj.field_02 = 'b'
            obj.field_03 = 'c'
            obj.field_04 = 'd'
            obj.field_05 = 'e'
            obj.field_06 = 1
            obj.field_07 = 2
            obj.field_08 = 3
            obj.field_09 = True
            obj.field_10 = False

    def assign_nested():
        for obj in nested_objs:
            obj.name        = 'parent'
            obj.inner.value = 'child_value'
            obj.inner.count = 99

    timing.benchmark('C_01__simple_x100_assign'      , assign_simple                                )
    timing.benchmark('C_02__many_fields_x100_assign' , assign_many_fields                           )
    timing.benchmark('C_03__nested_x100_assign'      , assign_nested                                )

    # Single object, many assignments
    def single_obj_many_assigns():
        obj = TS__Simple()
        for i in range(100):
            obj.name   = f'name_{i}'
            obj.count  = i
            obj.active = i % 2 == 0
            obj.value  = float(i)

    timing.benchmark('C_04__single_obj_400_assigns'  , single_obj_many_assigns                      )


def run_hypothesis_benchmarks(timing: Perf_Benchmark__Timing):                    # skip_validation=True
    # Create objects first (outside benchmark, outside context)
    simple_objs = [TS__Simple() for _ in range(100)]
    many_objs   = [TS__Many_Fields() for _ in range(100)]
    nested_objs = [TS__With_Nested() for _ in range(100)]

    with Type_Safe__Config(skip_validation=True):                                 # skip_validation enabled

        def assign_simple():
            for obj in simple_objs:
                obj.name   = 'updated'
                obj.count  = 42
                obj.active = True
                obj.value  = 3.14

        def assign_many_fields():
            for obj in many_objs:
                obj.field_01 = 'a'
                obj.field_02 = 'b'
                obj.field_03 = 'c'
                obj.field_04 = 'd'
                obj.field_05 = 'e'
                obj.field_06 = 1
                obj.field_07 = 2
                obj.field_08 = 3
                obj.field_09 = True
                obj.field_10 = False

        def assign_nested():
            for obj in nested_objs:
                obj.name        = 'parent'
                obj.inner.value = 'child_value'
                obj.inner.count = 99

        timing.benchmark('C_01__simple_x100_assign'      , assign_simple                            )
        timing.benchmark('C_02__many_fields_x100_assign' , assign_many_fields                       )
        timing.benchmark('C_03__nested_x100_assign'      , assign_nested                            )

        # Single object, many assignments
        def single_obj_many_assigns():
            obj = TS__Simple()
            for i in range(100):
                obj.name   = f'name_{i}'
                obj.count  = i
                obj.active = i % 2 == 0
                obj.value  = float(i)

        timing.benchmark('C_04__single_obj_400_assigns'  , single_obj_many_assigns                  )


# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test Class
# ═══════════════════════════════════════════════════════════════════════════════

class test_perf__Hypothesis_H__skip_validation(TestCase):

    def test__hypothesis_h__skip_validation(self):
        """
        HYPOTHESIS H: Default Type_Safe vs skip_validation=True

        Baseline: Normal Type_Safe.__setattr__ (full validation process)
        Hypothesis: skip_validation=True (direct object.__setattr__)

        NOTE: This tests attribute ASSIGNMENT performance, not object creation
        """
        type_safe_fast_create_cache.clear_cache()

        output_path = path_combine(__file__, '../')

        hypothesis = Perf_Benchmark__Hypothesis(
            description        = 'Hypothesis H: Default vs skip_validation=True',
            target_improvement = 0.5,                                             # Expect 50%+ improvement
            comments           = 'Bypasses __setattr__ validation, uses direct object.__setattr__'
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Warmup
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_baseline_benchmarks)                            # Warmup (discarded)

        # ═══════════════════════════════════════════════════════════════════════
        # Run BEFORE: Normal Type_Safe __setattr__
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_baseline_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Run AFTER: skip_validation=True
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_after(run_hypothesis_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Evaluate and Report
        # ═══════════════════════════════════════════════════════════════════════

        if False:
            result = hypothesis.evaluate()
            hypothesis.print_report()
            hypothesis.save_report(path_combine(output_path, 'hypothesis_h_skip_validation_report.txt'))
            hypothesis.save(path_combine(output_path, 'hypothesis_h_skip_validation_result.json'))