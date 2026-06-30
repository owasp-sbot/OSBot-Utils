# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Type_Safe fast_create vs Pydantic
# Compares: Pydantic BaseModel vs Type_Safe with fast_create=True
# ═══════════════════════════════════════════════════════════════════════════════
#
# BASELINE (Before): Pydantic BaseModel (with validation)
#
# HYPOTHESIS (After): Type_Safe with fast_create=True
#
# Goal: Type_Safe fast_create should be FASTER than Pydantic
#       (Pydantic validates, fast_create skips validation)
#
# Reference from benchmark.txt:
#   - pydantic__with_primitives: ~1,000 ns
#   - pydantic__with_nested: ~5,000 ns
#   - type_safe__with_primitives: ~6,000 ns (6x slower than pydantic primitives)
#   - With fast_create: targeting <1,000 ns (faster than pydantic!)
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                       import Dict, List, Optional
from unittest                                                                     import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing             import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Hypothesis         import Perf_Benchmark__Hypothesis
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                import Type_Safe__Config
from osbot_utils.type_safe.type_safe_core.fast_create.Type_Safe__Fast_Create__Cache import type_safe_fast_create_cache
from osbot_utils.utils.Env                                                        import not_in_github_action
from osbot_utils.utils.Files                                                      import path_combine

# ═══════════════════════════════════════════════════════════════════════════════
# Pydantic Import (optional dependency)
# ═══════════════════════════════════════════════════════════════════════════════

try:
    from pydantic import BaseModel
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    BaseModel = None


# ═══════════════════════════════════════════════════════════════════════════════
# Pydantic Classes (Baseline) - only defined if pydantic available
# ═══════════════════════════════════════════════════════════════════════════════

if HAS_PYDANTIC:

    class PD__Empty(BaseModel):
        pass


    class PD__With_Primitives(BaseModel):
        name   : str   = ''
        count  : int   = 0
        active : bool  = False
        value  : float = 0.0


    class PD__Inner(BaseModel):
        value : str = ''
        count : int = 0


    class PD__With_Nested(BaseModel):
        inner : PD__Inner = None
        name  : str       = ''

        def __init__(self, **data):
            if 'inner' not in data or data['inner'] is None:
                data['inner'] = PD__Inner()
            super().__init__(**data)


    class PD__With_Collections(BaseModel):
        items : List[str]      = []
        data  : Dict[str, int] = {}


    class PD__Many_Fields(BaseModel):
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


    # Deep nesting for Pydantic
    class PD__Level3(BaseModel):
        data : str = ''


    class PD__Level2(BaseModel):
        level3 : PD__Level3 = None
        value  : int        = 0

        def __init__(self, **data):
            if 'level3' not in data or data['level3'] is None:
                data['level3'] = PD__Level3()
            super().__init__(**data)


    class PD__Level1(BaseModel):
        level2 : PD__Level2 = None
        name   : str        = ''

        def __init__(self, **data):
            if 'level2' not in data or data['level2'] is None:
                data['level2'] = PD__Level2()
            super().__init__(**data)


    class PD__Deep_Nested(BaseModel):
        level1 : PD__Level1 = None
        count  : int        = 0

        def __init__(self, **data):
            if 'level1' not in data or data['level1'] is None:
                data['level1'] = PD__Level1()
            super().__init__(**data)


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

def run_pydantic_benchmarks(timing: Perf_Benchmark__Timing):                      # Pydantic (baseline)
    if not HAS_PYDANTIC:
        return

    # Single object creation
    timing.benchmark('A_01__empty'              , PD__Empty                                        )
    timing.benchmark('A_02__with_primitives'    , PD__With_Primitives                              )
    timing.benchmark('A_03__with_nested'        , PD__With_Nested                                  )
    timing.benchmark('A_04__with_collections'   , PD__With_Collections                             )
    timing.benchmark('A_05__many_fields'        , PD__Many_Fields                                  )
    timing.benchmark('A_06__deep_nested'        , PD__Deep_Nested                                  )

    # Batch creation
    timing.benchmark('B_01__empty_x10'          , lambda: [PD__Empty() for _ in range(10)]         )
    timing.benchmark('B_02__with_primitives_x10', lambda: [PD__With_Primitives() for _ in range(10)])
    timing.benchmark('B_03__with_nested_x10'    , lambda: [PD__With_Nested() for _ in range(10)]   )
    timing.benchmark('B_04__many_fields_x10'    , lambda: [PD__Many_Fields() for _ in range(10)]   )
    timing.benchmark('B_05__deep_nested_x10'    , lambda: [PD__Deep_Nested() for _ in range(10)]   )

    # Large batch
    timing.benchmark('C_01__empty_x100'         , lambda: [PD__Empty() for _ in range(100)]        )
    timing.benchmark('C_02__with_primitives_x100', lambda: [PD__With_Primitives() for _ in range(100)])


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

class test_perf__Type_Safe_vs_Pydantic(TestCase):

    def test__type_safe_fast_create_vs_pydantic(self):
        """
        Compare Type_Safe with fast_create vs Pydantic BaseModel

        Baseline: Pydantic BaseModel (with validation)
        Target: Type_Safe with fast_create=True (no validation)

        Goal: Type_Safe fast_create should be FASTER than Pydantic
              because Pydantic validates on every creation while
              fast_create skips validation entirely.

        Trade-off:
              - Pydantic: Always validates (safe but slower)
              - Type_Safe fast_create: No validation (fast but requires trusted data)
              - Type_Safe normal: Full validation (similar to Pydantic)
        """
        if not HAS_PYDANTIC:
            self.skipTest("Pydantic not installed")

        type_safe_fast_create_cache.clear_cache()

        output_path = path_combine(__file__, '../')

        hypothesis = Perf_Benchmark__Hypothesis(
            description        = 'Type_Safe fast_create vs Pydantic',
            target_improvement = 0.3,                                             # Expect to be 30%+ faster than Pydantic
            comments           = 'Pydantic validates; fast_create skips validation (should be faster)'
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Warmup
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_pydantic_benchmarks)                            # Warmup (discarded)

        # ═══════════════════════════════════════════════════════════════════════
        # Run BEFORE: Pydantic (baseline)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_pydantic_benchmarks)

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
            hypothesis.save_report(path_combine(output_path, 'type_safe_vs_pydantic_report.txt'))