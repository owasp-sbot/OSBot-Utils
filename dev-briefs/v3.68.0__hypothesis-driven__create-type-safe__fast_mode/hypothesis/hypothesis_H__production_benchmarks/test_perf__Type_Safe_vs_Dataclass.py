# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Type_Safe fast_create vs @dataclass
# Compares: Python dataclasses vs Type_Safe with fast_create=True
# ═══════════════════════════════════════════════════════════════════════════════
#
# BASELINE (Before): Python @dataclass (stdlib, no validation)
#
# HYPOTHESIS (After): Type_Safe with fast_create=True
#
# Goal: See how close Type_Safe can get to dataclass performance
#
# Reference from benchmark.txt:
#   - dataclass__with_primitives: ~500 ns
#   - dataclass__with_nested: ~600 ns
#   - type_safe__with_primitives: ~6,000 ns (12x slower)
#   - With fast_create: targeting <1,500 ns (3x slower acceptable)
#
# ═══════════════════════════════════════════════════════════════════════════════

from dataclasses                                                                  import dataclass, field
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
# @dataclass Classes (Baseline)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class DC__Empty:
    pass


@dataclass
class DC__With_Primitives:
    name   : str   = ''
    count  : int   = 0
    active : bool  = False
    value  : float = 0.0


@dataclass
class DC__Inner:
    value : str = ''
    count : int = 0


@dataclass
class DC__With_Nested:
    inner : DC__Inner = field(default_factory=DC__Inner)
    name  : str       = ''


@dataclass
class DC__With_Collections:
    items : List[str]       = field(default_factory=list)
    data  : Dict[str, int]  = field(default_factory=dict)


@dataclass
class DC__Many_Fields:
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


# Deep nesting for dataclass
@dataclass
class DC__Level3:
    data : str = ''


@dataclass
class DC__Level2:
    level3 : DC__Level3 = field(default_factory=DC__Level3)
    value  : int        = 0


@dataclass
class DC__Level1:
    level2 : DC__Level2 = field(default_factory=DC__Level2)
    name   : str        = ''


@dataclass
class DC__Deep_Nested:
    level1 : DC__Level1 = field(default_factory=DC__Level1)
    count  : int        = 0


# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe Classes (equivalent structure)
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Empty(Type_Safe):
    pass


class TS__With_Primitives(Type_Safe):
    name   : str   = ''
    count  : int   = 0
    active : bool  = False
    value  : float = 0.0


class TS__Inner(Type_Safe):
    value : str = ''
    count : int = 0


class TS__With_Nested(Type_Safe):
    inner : TS__Inner
    name  : str = ''


class TS__With_Collections(Type_Safe):
    items : List[str]
    data  : Dict[str, int]


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


# Deep nesting for Type_Safe
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


# ═══════════════════════════════════════════════════════════════════════════════
# Benchmark Functions
# ═══════════════════════════════════════════════════════════════════════════════

def run_dataclass_benchmarks(timing: Perf_Benchmark__Timing):                     # @dataclass (baseline)

    # Single object creation
    timing.benchmark('A_01__empty'              , DC__Empty                                        )
    timing.benchmark('A_02__with_primitives'    , DC__With_Primitives                              )
    timing.benchmark('A_03__with_nested'        , DC__With_Nested                                  )
    timing.benchmark('A_04__with_collections'   , DC__With_Collections                             )
    timing.benchmark('A_05__many_fields'        , DC__Many_Fields                                  )
    timing.benchmark('A_06__deep_nested'        , DC__Deep_Nested                                  )

    # Batch creation
    timing.benchmark('B_01__empty_x10'          , lambda: [DC__Empty() for _ in range(10)]         )
    timing.benchmark('B_02__with_primitives_x10', lambda: [DC__With_Primitives() for _ in range(10)])
    timing.benchmark('B_03__with_nested_x10'    , lambda: [DC__With_Nested() for _ in range(10)]   )
    timing.benchmark('B_04__many_fields_x10'    , lambda: [DC__Many_Fields() for _ in range(10)]   )
    timing.benchmark('B_05__deep_nested_x10'    , lambda: [DC__Deep_Nested() for _ in range(10)]   )

    # Large batch
    timing.benchmark('C_01__empty_x100'         , lambda: [DC__Empty() for _ in range(100)]        )
    timing.benchmark('C_02__with_primitives_x100', lambda: [DC__With_Primitives() for _ in range(100)])


def run_type_safe_benchmarks(timing: Perf_Benchmark__Timing):                     # Type_Safe with fast_create
    type_safe_fast_create_cache.clear_cache()

    # Pre-warm schema cache
    type_safe_fast_create_cache.warm_cache(TS__Empty)
    type_safe_fast_create_cache.warm_cache(TS__With_Primitives)
    type_safe_fast_create_cache.warm_cache(TS__With_Nested)
    type_safe_fast_create_cache.warm_cache(TS__With_Collections)
    type_safe_fast_create_cache.warm_cache(TS__Many_Fields)
    type_safe_fast_create_cache.warm_cache(TS__Deep_Nested)

    with Type_Safe__Config(fast_create=True):

        # Single object creation
        timing.benchmark('A_01__empty'              , TS__Empty                                        )
        timing.benchmark('A_02__with_primitives'    , TS__With_Primitives                              )
        timing.benchmark('A_03__with_nested'        , TS__With_Nested                                  )
        timing.benchmark('A_04__with_collections'   , TS__With_Collections                             )
        timing.benchmark('A_05__many_fields'        , TS__Many_Fields                                  )
        timing.benchmark('A_06__deep_nested'        , TS__Deep_Nested                                  )

        # Batch creation
        timing.benchmark('B_01__empty_x10'          , lambda: [TS__Empty() for _ in range(10)]         )
        timing.benchmark('B_02__with_primitives_x10', lambda: [TS__With_Primitives() for _ in range(10)])
        timing.benchmark('B_03__with_nested_x10'    , lambda: [TS__With_Nested() for _ in range(10)]   )
        timing.benchmark('B_04__many_fields_x10'    , lambda: [TS__Many_Fields() for _ in range(10)]   )
        timing.benchmark('B_05__deep_nested_x10'    , lambda: [TS__Deep_Nested() for _ in range(10)]   )

        # Large batch
        timing.benchmark('C_01__empty_x100'         , lambda: [TS__Empty() for _ in range(100)]        )
        timing.benchmark('C_02__with_primitives_x100', lambda: [TS__With_Primitives() for _ in range(100)])


# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test Class
# ═══════════════════════════════════════════════════════════════════════════════

class test_perf__Type_Safe_vs_Dataclass(TestCase):

    def test__type_safe_fast_create_vs_dataclass(self):
        """
        Compare Type_Safe with fast_create vs Python @dataclass

        Baseline: Python @dataclass (stdlib, no runtime validation)
        Target: Type_Safe with fast_create=True

        Goal: Minimize the performance gap while retaining Type_Safe benefits
              - Type_Safe provides runtime type checking (when not in fast mode)
              - Type_Safe provides auto-conversion
              - Type_Safe provides nested object creation
              - @dataclass provides none of these
        """
        type_safe_fast_create_cache.clear_cache()

        output_path = path_combine(__file__, '../')

        hypothesis = Perf_Benchmark__Hypothesis(
            description        = 'Type_Safe fast_create vs @dataclass',
            target_improvement = -2.0,                                            # Expect to be ~2-3x slower
            comments           = '@dataclass is baseline; Type_Safe adds type safety infrastructure'
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Warmup
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_dataclass_benchmarks)                           # Warmup (discarded)

        # ═══════════════════════════════════════════════════════════════════════
        # Run BEFORE: @dataclass (baseline)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_dataclass_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Run AFTER: Type_Safe with fast_create
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_after(run_type_safe_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Evaluate and Report
        # ═══════════════════════════════════════════════════════════════════════

        if False:
            result = hypothesis.evaluate()
            hypothesis.print_report()
            hypothesis.save_report(path_combine(output_path, 'type_safe_vs_dataclass_report.txt'))