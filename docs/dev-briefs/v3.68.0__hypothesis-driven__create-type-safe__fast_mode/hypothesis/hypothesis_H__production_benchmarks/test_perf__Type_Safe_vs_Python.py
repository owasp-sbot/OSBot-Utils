# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Type_Safe fast_create vs Python Classes
# Compares: Plain Python classes vs Type_Safe with fast_create=True
# ═══════════════════════════════════════════════════════════════════════════════
#
# BASELINE (Before): Plain Python classes (fastest possible)
#
# HYPOTHESIS (After): Type_Safe with fast_create=True
#
# Goal: See how close Type_Safe can get to raw Python performance
#
# Reference from benchmark.txt:
#   - python__class_with_init: ~300 ns
#   - type_safe__with_primitives: ~6,000 ns (20x slower)
#   - With fast_create: targeting <1,000 ns (3x slower acceptable)
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
# Python Baseline Classes
# ═══════════════════════════════════════════════════════════════════════════════

class Py__Empty:
    pass


class Py__With_Primitives:
    def __init__(self):
        self.name   = ''
        self.count  = 0
        self.active = False
        self.value  = 0.0


class Py__With_Slots:
    __slots__ = ('name', 'count', 'active', 'value')
    def __init__(self):
        self.name   = ''
        self.count  = 0
        self.active = False
        self.value  = 0.0


class Py__Inner:
    def __init__(self):
        self.value = ''
        self.count = 0


class Py__With_Nested:
    def __init__(self):
        self.inner = Py__Inner()
        self.name  = ''


class Py__With_Collections:
    def __init__(self):
        self.items = []
        self.data  = {}


class Py__Many_Fields:
    def __init__(self):
        self.field_01 = ''
        self.field_02 = ''
        self.field_03 = ''
        self.field_04 = ''
        self.field_05 = ''
        self.field_06 = 0
        self.field_07 = 0
        self.field_08 = 0
        self.field_09 = False
        self.field_10 = False


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


# ═══════════════════════════════════════════════════════════════════════════════
# Benchmark Functions
# ═══════════════════════════════════════════════════════════════════════════════

def run_python_benchmarks(timing: Perf_Benchmark__Timing):                        # Python classes (baseline)

    # Single object creation
    timing.benchmark('A_01__empty'              , Py__Empty                                        )
    timing.benchmark('A_02__with_primitives'    , Py__With_Primitives                              )
    timing.benchmark('A_03__with_slots'         , Py__With_Slots                                   )
    timing.benchmark('A_04__with_nested'        , Py__With_Nested                                  )
    timing.benchmark('A_05__with_collections'   , Py__With_Collections                             )
    timing.benchmark('A_06__many_fields'        , Py__Many_Fields                                  )

    # Batch creation
    timing.benchmark('B_01__empty_x10'          , lambda: [Py__Empty() for _ in range(10)]         )
    timing.benchmark('B_02__with_primitives_x10', lambda: [Py__With_Primitives() for _ in range(10)])
    timing.benchmark('B_03__with_nested_x10'    , lambda: [Py__With_Nested() for _ in range(10)]   )
    timing.benchmark('B_04__many_fields_x10'    , lambda: [Py__Many_Fields() for _ in range(10)]   )

    # Large batch
    timing.benchmark('C_01__empty_x100'         , lambda: [Py__Empty() for _ in range(100)]        )
    timing.benchmark('C_02__with_primitives_x100', lambda: [Py__With_Primitives() for _ in range(100)])


def run_type_safe_benchmarks(timing: Perf_Benchmark__Timing):                     # Type_Safe with fast_create
    type_safe_fast_create_cache.clear_cache()

    # Pre-warm schema cache
    type_safe_fast_create_cache.warm_cache(TS__Empty)
    type_safe_fast_create_cache.warm_cache(TS__With_Primitives)
    type_safe_fast_create_cache.warm_cache(TS__With_Nested)
    type_safe_fast_create_cache.warm_cache(TS__With_Collections)
    type_safe_fast_create_cache.warm_cache(TS__Many_Fields)

    with Type_Safe__Config(fast_create=True):

        # Single object creation
        timing.benchmark('A_01__empty'              , TS__Empty                                        )
        timing.benchmark('A_02__with_primitives'    , TS__With_Primitives                              )
        timing.benchmark('A_03__with_slots'         , TS__With_Primitives                              )  # No slots equivalent
        timing.benchmark('A_04__with_nested'        , TS__With_Nested                                  )
        timing.benchmark('A_05__with_collections'   , TS__With_Collections                             )
        timing.benchmark('A_06__many_fields'        , TS__Many_Fields                                  )

        # Batch creation
        timing.benchmark('B_01__empty_x10'          , lambda: [TS__Empty() for _ in range(10)]         )
        timing.benchmark('B_02__with_primitives_x10', lambda: [TS__With_Primitives() for _ in range(10)])
        timing.benchmark('B_03__with_nested_x10'    , lambda: [TS__With_Nested() for _ in range(10)]   )
        timing.benchmark('B_04__many_fields_x10'    , lambda: [TS__Many_Fields() for _ in range(10)]   )

        # Large batch
        timing.benchmark('C_01__empty_x100'         , lambda: [TS__Empty() for _ in range(100)]        )
        timing.benchmark('C_02__with_primitives_x100', lambda: [TS__With_Primitives() for _ in range(100)])


# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test Class
# ═══════════════════════════════════════════════════════════════════════════════

class test_perf__Type_Safe_vs_Python(TestCase):

    def test__type_safe_fast_create_vs_python(self):
        """
        Compare Type_Safe with fast_create vs Plain Python Classes

        Baseline: Plain Python classes (fastest possible)
        Target: Type_Safe with fast_create=True

        Goal: Minimize the performance gap while retaining Type_Safe benefits
        """
        type_safe_fast_create_cache.clear_cache()

        output_path = path_combine(__file__, '../')

        hypothesis = Perf_Benchmark__Hypothesis(
            description        = 'Type_Safe fast_create vs Python Classes',
            target_improvement = -2.0,                                            # Expect to be ~2-3x slower (negative = slower is ok)
            comments           = 'Python classes are baseline; Type_Safe adds type safety overhead'
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Warmup
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_python_benchmarks)                              # Warmup (discarded)

        # ═══════════════════════════════════════════════════════════════════════
        # Run BEFORE: Python Classes (baseline)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_python_benchmarks)

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
            hypothesis.save_report(path_combine(output_path, 'type_safe_vs_python_report.txt'))