# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Hypothesis H - Default vs fast_create
# Compares: Normal Type_Safe vs fast_create=True
# ═══════════════════════════════════════════════════════════════════════════════
#
# BASELINE (Before): Normal Type_Safe.__init__ (full validation)
#
# HYPOTHESIS (After): fast_create=True (schema-based direct __dict__ assignment)
#
# Expected: 50-85% improvement for complex classes
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
# Test Classes - Various complexity levels
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Empty(Type_Safe):
    pass


class TS__Primitives_Only(Type_Safe):
    name   : str   = ''
    count  : int   = 0
    active : bool  = False
    value  : float = 0.0


class TS__With_Collections(Type_Safe):
    name  : str = ''
    items : List[str]
    data  : Dict[str, int]


class TS__Inner(Type_Safe):
    value : str = ''
    count : int = 0


class TS__One_Nested(Type_Safe):
    inner : TS__Inner
    name  : str = ''


class TS__Three_Nested(Type_Safe):
    child1 : TS__Inner
    child2 : TS__Inner
    child3 : TS__Inner
    name   : str = ''


class TS__Level3(Type_Safe):
    data : str = ''


class TS__Level2(Type_Safe):
    level3 : TS__Level3
    value  : int = 0


class TS__Level1(Type_Safe):
    level2 : TS__Level2
    name   : str = ''


class TS__Deep_Nested(Type_Safe):
    level1 : TS__Level1
    count  : int = 0


class TS__Schema__Data(Type_Safe):
    items  : Dict[str, str]
    labels : Dict[str, str]


class TS__Index__Edges(Type_Safe):
    data : TS__Schema__Data
    name : str = ''


class TS__Index__Nodes(Type_Safe):
    data : TS__Schema__Data
    name : str = ''


class TS__MGraph_Like(Type_Safe):
    edges_index : TS__Index__Edges
    nodes_index : TS__Index__Nodes
    count       : int = 0


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


# ═══════════════════════════════════════════════════════════════════════════════
# Benchmark Functions
# ═══════════════════════════════════════════════════════════════════════════════

def run_baseline_benchmarks(timing: Perf_Benchmark__Timing):                      # Default Type_Safe
    type_safe_fast_create_cache.clear_cache()

    # No config = normal Type_Safe behavior (full validation)

    # Simple classes
    timing.benchmark('A_01__empty'            , TS__Empty                                        )
    timing.benchmark('A_02__primitives_only'  , TS__Primitives_Only                              )
    timing.benchmark('A_03__with_collections' , TS__With_Collections                             )
    timing.benchmark('A_04__many_fields'      , TS__Many_Fields                                  )

    # Nested classes
    timing.benchmark('A_05__one_nested'       , TS__One_Nested                                   )
    timing.benchmark('A_06__three_nested'     , TS__Three_Nested                                 )
    timing.benchmark('A_07__deep_nested'      , TS__Deep_Nested                                  )
    timing.benchmark('A_08__mgraph_like'      , TS__MGraph_Like                                  )

    # Batch creation
    timing.benchmark('B_01__primitives_x10'   , lambda: [TS__Primitives_Only() for _ in range(10)])
    timing.benchmark('B_02__many_fields_x10'  , lambda: [TS__Many_Fields()     for _ in range(10)])
    timing.benchmark('B_03__three_nested_x10' , lambda: [TS__Three_Nested()    for _ in range(10)])
    timing.benchmark('B_04__mgraph_like_x10'  , lambda: [TS__MGraph_Like()     for _ in range(10)])


def run_hypothesis_benchmarks(timing: Perf_Benchmark__Timing):                    # fast_create=True
    type_safe_fast_create_cache.clear_cache()

    # Pre-warm schema cache
    type_safe_fast_create_cache.warm_cache(TS__Empty)
    type_safe_fast_create_cache.warm_cache(TS__Primitives_Only)
    type_safe_fast_create_cache.warm_cache(TS__With_Collections)
    type_safe_fast_create_cache.warm_cache(TS__Many_Fields)
    type_safe_fast_create_cache.warm_cache(TS__One_Nested)
    type_safe_fast_create_cache.warm_cache(TS__Three_Nested)
    type_safe_fast_create_cache.warm_cache(TS__Deep_Nested)
    type_safe_fast_create_cache.warm_cache(TS__MGraph_Like)

    with Type_Safe__Config(fast_create=True):                                     # fast_create enabled

        # Simple classes
        timing.benchmark('A_01__empty'            , TS__Empty                                        )
        timing.benchmark('A_02__primitives_only'  , TS__Primitives_Only                              )
        timing.benchmark('A_03__with_collections' , TS__With_Collections                             )
        timing.benchmark('A_04__many_fields'      , TS__Many_Fields                                  )

        # Nested classes
        timing.benchmark('A_05__one_nested'       , TS__One_Nested                                   )
        timing.benchmark('A_06__three_nested'     , TS__Three_Nested                                 )
        timing.benchmark('A_07__deep_nested'      , TS__Deep_Nested                                  )
        timing.benchmark('A_08__mgraph_like'      , TS__MGraph_Like                                  )

        # Batch creation
        timing.benchmark('B_01__primitives_x10'   , lambda: [TS__Primitives_Only() for _ in range(10)])
        timing.benchmark('B_02__many_fields_x10'  , lambda: [TS__Many_Fields()     for _ in range(10)])
        timing.benchmark('B_03__three_nested_x10' , lambda: [TS__Three_Nested()    for _ in range(10)])
        timing.benchmark('B_04__mgraph_like_x10'  , lambda: [TS__MGraph_Like()     for _ in range(10)])


# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test Class
# ═══════════════════════════════════════════════════════════════════════════════

class test_perf__Hypothesis_H__fast_create(TestCase):

    def test__hypothesis_h__fast_create(self):
        """
        HYPOTHESIS H: Default Type_Safe vs fast_create=True

        Baseline: Normal Type_Safe.__init__ (full validation process)
        Hypothesis: fast_create=True (schema-based direct __dict__ assignment)

        Expected: 50-85% improvement for complex classes
        """
        type_safe_fast_create_cache.clear_cache()

        output_path = path_combine(__file__, '../')

        hypothesis = Perf_Benchmark__Hypothesis(
            description        = 'Hypothesis H: Default vs fast_create=True',
            target_improvement = 0.5,                                             # Expect 50%+ improvement
            comments           = 'Bypasses __init__ validation, uses pre-computed schemas'
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Warmup
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_baseline_benchmarks)                            # Warmup (discarded)

        # ═══════════════════════════════════════════════════════════════════════
        # Run BEFORE: Normal Type_Safe
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_baseline_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Run AFTER: fast_create=True
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_after(run_hypothesis_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Evaluate and Report
        # ═══════════════════════════════════════════════════════════════════════

        if False:
            result = hypothesis.evaluate()
            hypothesis.print_report()
            hypothesis.save_report(path_combine(output_path, 'hypothesis_h_fast_create_report.txt'))
            hypothesis.save(path_combine(output_path, 'hypothesis_h_fast_create_result.json'))