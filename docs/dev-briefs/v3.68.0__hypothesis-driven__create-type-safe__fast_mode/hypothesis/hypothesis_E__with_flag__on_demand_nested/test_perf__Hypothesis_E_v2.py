# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Hypothesis E v2 - Simplified On-Demand Nested Creation
# Compares: on_demand_nested=False vs on_demand_nested=True
# ═══════════════════════════════════════════════════════════════════════════════
#
# BASELINE (Before): on_demand_nested=False
#                    All nested Type_Safe objects created during __init__
#
# HYPOTHESIS (After): on_demand_nested=True
#                     Nested Type_Safe objects created only on first access
#
# v2 IMPROVEMENTS over v1:
# - No permanent _on_demand__types dict
# - Temporary _on_demand__init_complete flag (deleted after init)
# - No _on_demand__clean_json hack needed
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import List, Dict
from unittest                                                                                 import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                         import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Hypothesis                     import Perf_Benchmark__Hypothesis
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import Type_Safe__Config
from osbot_utils.utils.Env                                                                    import not_in_github_action
from osbot_utils.utils.Files                                                                  import path_combine

from Type_Safe__Hypothesis_E_v2                                                               import Type_Safe__Hypothesis_E_v2


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes - Hierarchy to test on-demand creation
# ═══════════════════════════════════════════════════════════════════════════════

# Simple classes (no nesting - minimal impact expected)
class TS__Empty(Type_Safe__Hypothesis_E_v2):
    pass

class TS__With_Primitives(Type_Safe__Hypothesis_E_v2):
    name   : str  = ''
    count  : int  = 0
    active : bool = False


# Single level nesting
class TS__Inner(Type_Safe__Hypothesis_E_v2):
    value : str = ''
    count : int = 0

class TS__With_One_Nested(Type_Safe__Hypothesis_E_v2):
    inner : TS__Inner
    name  : str = ''


# Multiple nested at same level
class TS__With_Three_Nested(Type_Safe__Hypothesis_E_v2):
    child1 : TS__Inner
    child2 : TS__Inner
    child3 : TS__Inner
    name   : str = ''


# Deep nesting (3 levels)
class TS__Level3(Type_Safe__Hypothesis_E_v2):
    data : str = ''

class TS__Level2(Type_Safe__Hypothesis_E_v2):
    level3 : TS__Level3
    value  : int = 0

class TS__Level1(Type_Safe__Hypothesis_E_v2):
    level2 : TS__Level2
    name   : str = ''

class TS__Deep_Nested(Type_Safe__Hypothesis_E_v2):
    level1 : TS__Level1
    count  : int = 0


# Complex: Multiple nested with their own nested
class TS__Schema__Data(Type_Safe__Hypothesis_E_v2):
    items  : Dict[str, str]
    labels : Dict[str, str]

class TS__Index__Edges(Type_Safe__Hypothesis_E_v2):
    data : TS__Schema__Data
    name : str = ''

class TS__Index__Nodes(Type_Safe__Hypothesis_E_v2):
    data : TS__Schema__Data
    name : str = ''

class TS__MGraph_Like(Type_Safe__Hypothesis_E_v2):
    """Simulates MGraph__Index with multiple indexes"""
    edges_index : TS__Index__Edges
    nodes_index : TS__Index__Nodes
    count       : int = 0


# ═══════════════════════════════════════════════════════════════════════════════
# Benchmark Functions
# ═══════════════════════════════════════════════════════════════════════════════

def run_baseline_benchmarks(timing: Perf_Benchmark__Timing):                                  # on_demand_nested=FALSE
    with Type_Safe__Config(on_demand_nested=False):                                           # Normal mode (all nested created)

        # No nesting - should be similar
        timing.benchmark('A_01__empty'              , TS__Empty                                       )
        timing.benchmark('A_02__with_primitives'    , TS__With_Primitives                             )

        # Single nesting - should show improvement
        timing.benchmark('A_03__one_nested'         , TS__With_One_Nested                             )

        # Multiple nesting - should show bigger improvement
        timing.benchmark('A_04__three_nested'       , TS__With_Three_Nested                           )

        # Deep nesting - should show significant improvement
        timing.benchmark('A_05__deep_nested'        , TS__Deep_Nested                                 )

        # Complex (MGraph-like) - should show major improvement
        timing.benchmark('A_06__mgraph_like'        , TS__MGraph_Like                                 )

        # Batch creation
        timing.benchmark('B_01__one_nested_x10'     , lambda: [TS__With_One_Nested() for _ in range(10)])
        timing.benchmark('B_02__three_nested_x10'   , lambda: [TS__With_Three_Nested() for _ in range(10)])
        timing.benchmark('B_03__deep_nested_x10'    , lambda: [TS__Deep_Nested() for _ in range(10)]  )
        timing.benchmark('B_04__mgraph_like_x10'    , lambda: [TS__MGraph_Like() for _ in range(10)]  )


def run_hypothesis_benchmarks(timing: Perf_Benchmark__Timing):                                # on_demand_nested=TRUE
    with Type_Safe__Config(on_demand_nested=True):                                            # On-demand mode

        # No nesting - should be similar
        timing.benchmark('A_01__empty'              , TS__Empty                                       )
        timing.benchmark('A_02__with_primitives'    , TS__With_Primitives                             )

        # Single nesting - should show improvement
        timing.benchmark('A_03__one_nested'         , TS__With_One_Nested                             )

        # Multiple nesting - should show bigger improvement
        timing.benchmark('A_04__three_nested'       , TS__With_Three_Nested                           )

        # Deep nesting - should show significant improvement
        timing.benchmark('A_05__deep_nested'        , TS__Deep_Nested                                 )

        # Complex (MGraph-like) - should show major improvement
        timing.benchmark('A_06__mgraph_like'        , TS__MGraph_Like                                 )

        # Batch creation
        timing.benchmark('B_01__one_nested_x10'     , lambda: [TS__With_One_Nested() for _ in range(10)])
        timing.benchmark('B_02__three_nested_x10'   , lambda: [TS__With_Three_Nested() for _ in range(10)])
        timing.benchmark('B_03__deep_nested_x10'    , lambda: [TS__Deep_Nested() for _ in range(10)]  )
        timing.benchmark('B_04__mgraph_like_x10'    , lambda: [TS__MGraph_Like() for _ in range(10)]  )


class test_perf__Hypothesis_E_v2(TestCase):

    def test__hypothesis_e_v2__on_demand_nested(self):
        """
        HYPOTHESIS E v2: Simplified on_demand_nested Implementation

        Baseline: on_demand_nested=False (all nested Type_Safe created during init)
        Hypothesis: on_demand_nested=True (nested created only on first access)

        v2 uses temporary _on_demand__init_complete flag (deleted after init)
        No permanent tracking dicts, no json cleanup needed.

        Expected: Major improvement for nested classes (similar to v1: ~60% overall)
        """
        output_path = path_combine(__file__, '../')

        hypothesis = Perf_Benchmark__Hypothesis(
            description        = 'Hypothesis E v2: on_demand_nested (simplified)',
            target_improvement = 0.3,                                                         # Expect 30%+ improvement
            comments           = 'v2: Temporary flag approach - no permanent tracking dicts'
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Warmup (run baseline twice to eliminate ordering effects)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_baseline_benchmarks)                                        # Warmup

        # ═══════════════════════════════════════════════════════════════════════
        # Run BEFORE: on_demand_nested=False (all nested created)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_baseline_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Run AFTER: on_demand_nested=True (nested created on demand)
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_after(run_hypothesis_benchmarks)

        # ═══════════════════════════════════════════════════════════════════════
        # Evaluate and Report
        # ═══════════════════════════════════════════════════════════════════════

        if False:
            result = hypothesis.evaluate()

            if not_in_github_action():
                hypothesis.print_report()
                hypothesis.save_report(path_combine(output_path, 'hypothesis_e_v2_report.txt'))
                hypothesis.save(path_combine(output_path, 'hypothesis_e_v2_result.json'))

        # ═══════════════════════════════════════════════════════════════════════
        # Verify on-demand behavior
        # ═══════════════════════════════════════════════════════════════════════

        self.verify_on_demand_behavior()
        self.verify_no_permanent_tracking()

    def verify_on_demand_behavior(self):                                                      # Verify on-demand works correctly

        # Test 1: Objects are None initially (use object.__getattribute__ to bypass auto-create)
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__With_Three_Nested()
            raw_child1 = object.__getattribute__(obj, 'child1')
            raw_child2 = object.__getattribute__(obj, 'child2')
            raw_child3 = object.__getattribute__(obj, 'child3')
            assert raw_child1 is None, f"child1 should be None, got {raw_child1}"
            assert raw_child2 is None, f"child2 should be None, got {raw_child2}"
            assert raw_child3 is None, f"child3 should be None, got {raw_child3}"

        # Test 2: Accessing creates the object
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__With_One_Nested()
            raw_inner = object.__getattribute__(obj, 'inner')
            assert raw_inner is None, "inner should be None initially"

            inner = obj.inner                                                                 # Access triggers creation
            assert inner is not None, "inner should be created on access"
            assert isinstance(inner, TS__Inner), f"inner should be TS__Inner, got {type(inner)}"

        # Test 3: Deep nesting works
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__Deep_Nested()
            data = obj.level1.level2.level3.data                                              # Each level created on access
            assert data == '', "Deep access should work"

        # Test 4: Normal mode creates everything upfront
        with Type_Safe__Config(on_demand_nested=False):
            obj = TS__With_Three_Nested()
            raw_child1 = object.__getattribute__(obj, 'child1')
            raw_child2 = object.__getattribute__(obj, 'child2')
            raw_child3 = object.__getattribute__(obj, 'child3')
            assert raw_child1 is not None, "child1 should exist in normal mode"
            assert raw_child2 is not None, "child2 should exist in normal mode"
            assert raw_child3 is not None, "child3 should exist in normal mode"

        # Test 5: User-provided kwargs bypass on-demand
        with Type_Safe__Config(on_demand_nested=True):
            custom_inner = TS__Inner(value='custom')
            obj = TS__With_One_Nested(inner=custom_inner)
            assert obj.inner.value == 'custom', "provided inner should be used"

    def verify_no_permanent_tracking(self):                                                   # Verify v2 has no permanent tracking attributes

        # After init completes, _on_demand__init_complete should NOT exist
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__With_Three_Nested()

            # Should NOT have _on_demand__init_complete (it's deleted after init)
            has_init_flag = '_on_demand__init_complete' in obj.__dict__
            assert not has_init_flag, "v2 should not have permanent _on_demand__init_complete"

            # Should NOT have _on_demand__types dict
            has_types_dict = '_on_demand__types' in obj.__dict__
            assert not has_types_dict, "v2 should not have _on_demand__types dict"

        # json() should not contain any _on_demand__ keys
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__With_One_Nested(name='test')
            json_data = obj.json()

            for key in json_data.keys():
                assert not key.startswith('_on_demand__'), f"json should not have {key}"