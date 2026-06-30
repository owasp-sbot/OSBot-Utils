# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Hypothesis E - on_demand_nested Flag Implementation
# Compares: on_demand_nested=False vs on_demand_nested=True
# ═══════════════════════════════════════════════════════════════════════════════
#
# BASELINE (Before): on_demand_nested=False
#                    All nested Type_Safe objects created during __init__
#
# HYPOTHESIS (After): on_demand_nested=True
#                     Nested Type_Safe objects created only on first access
#
# Focus: Tests with nested Type_Safe objects should show massive improvement
#        Tests with only primitives/collections should show minimal change
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import List, Dict
from unittest                                                                                 import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                         import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Hypothesis                     import Perf_Benchmark__Hypothesis
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import Type_Safe__Config, get_active_config
from osbot_utils.utils.Env                                                                    import not_in_github_action
from osbot_utils.utils.Files                                                                  import path_combine

from Type_Safe__Hypothesis_E                                                                  import Type_Safe__Hypothesis_E


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes - Hierarchy to test on-demand creation
# ═══════════════════════════════════════════════════════════════════════════════

# Simple classes (no nesting - minimal impact expected)
class TS__Empty(Type_Safe__Hypothesis_E):
    pass

class TS__With_Primitives(Type_Safe__Hypothesis_E):
    name   : str  = ''
    count  : int  = 0
    active : bool = False


# Single level nesting
class TS__Inner(Type_Safe__Hypothesis_E):
    value : str = ''
    count : int = 0

class TS__With_One_Nested(Type_Safe__Hypothesis_E):
    inner : TS__Inner
    name  : str = ''


# Multiple nested at same level
class TS__With_Three_Nested(Type_Safe__Hypothesis_E):
    child1 : TS__Inner
    child2 : TS__Inner
    child3 : TS__Inner
    name   : str = ''


# Deep nesting (3 levels)
class TS__Level3(Type_Safe__Hypothesis_E):
    data : str = ''

class TS__Level2(Type_Safe__Hypothesis_E):
    level3 : TS__Level3
    value  : int = 0

class TS__Level1(Type_Safe__Hypothesis_E):
    level2 : TS__Level2
    name   : str = ''

class TS__Deep_Nested(Type_Safe__Hypothesis_E):
    level1 : TS__Level1
    count  : int = 0


# Complex: Multiple nested with their own nested
class TS__Schema__Data(Type_Safe__Hypothesis_E):
    items  : Dict[str, str]
    labels : Dict[str, str]

class TS__Index__Edges(Type_Safe__Hypothesis_E):
    data : TS__Schema__Data
    name : str = ''

class TS__Index__Nodes(Type_Safe__Hypothesis_E):
    data : TS__Schema__Data
    name : str = ''

class TS__MGraph_Like(Type_Safe__Hypothesis_E):
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


class test_perf__Hypothesis_E(TestCase):

    def test__hypothesis_e__on_demand_nested(self):
        """
        HYPOTHESIS E: on_demand_nested Flag Implementation

        Baseline: on_demand_nested=False (all nested Type_Safe created during init)
        Hypothesis: on_demand_nested=True (nested created only on first access)

        Expected: Major improvement for nested classes (20x reported in docs)
        Focus: A_03-A_06, B_01-B_04 (nested classes) should show big gains
        """
        output_path = path_combine(__file__, '../')

        hypothesis = Perf_Benchmark__Hypothesis(
            description        = 'Hypothesis E: on_demand_nested=True vs False',
            target_improvement = 0.3,                                                         # Expect 30%+ improvement
            comments           = 'Testing performance gain from deferring nested Type_Safe creation'
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
                hypothesis.save_report(path_combine(output_path, 'hypothesis_e_report.txt'))
                hypothesis.save(path_combine(output_path, 'hypothesis_e_result.json'))

        # ═══════════════════════════════════════════════════════════════════════
        # Verify on-demand behavior
        # ═══════════════════════════════════════════════════════════════════════

        self.verify_on_demand_behavior()

    def verify_on_demand_behavior(self):                                                      # Verify on-demand works correctly

        # Test 1: Objects are pending initially
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__With_Three_Nested()
            on_demand_types = object.__getattribute__(obj, '_on_demand__types')
            assert len(on_demand_types) == 3, f"Expected 3 pending, got {len(on_demand_types)}"
            assert 'child1' in on_demand_types, "child1 should be pending"
            assert 'child2' in on_demand_types, "child2 should be pending"
            assert 'child3' in on_demand_types, "child3 should be pending"

        # Test 2: Accessing creates the object
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__With_One_Nested()
            on_demand_types = object.__getattribute__(obj, '_on_demand__types')
            assert 'inner' in on_demand_types, "inner should be pending"

            # Access the attribute
            inner = obj.inner
            assert inner is not None, "inner should be created"
            assert isinstance(inner, TS__Inner), f"inner should be TS__Inner, got {type(inner)}"

            # Should no longer be pending
            on_demand_types = object.__getattribute__(obj, '_on_demand__types')
            assert 'inner' not in on_demand_types, "inner should no longer be pending"

        # Test 3: Deep nesting works
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__Deep_Nested()

            # Nothing accessed yet - should have level1 pending
            on_demand_types = object.__getattribute__(obj, '_on_demand__types')
            assert 'level1' in on_demand_types, "level1 should be pending"

            # Access deep: level1.level2.level3.data
            data = obj.level1.level2.level3.data
            assert data == '', "Deep access should work"

        # Test 4: Normal mode creates everything upfront
        with Type_Safe__Config(on_demand_nested=False):
            obj = TS__With_Three_Nested()
            # Should NOT have _on_demand__types or it should be empty
            try:
                on_demand_types = object.__getattribute__(obj, '_on_demand__types')
                # If it exists, should be empty
                assert len(on_demand_types) == 0, "Normal mode should not have pending types"
            except AttributeError:
                pass  # Expected - attribute doesn't exist in normal mode

            # All children should exist
            assert obj.child1 is not None, "child1 should exist"
            assert obj.child2 is not None, "child2 should exist"
            assert obj.child3 is not None, "child3 should exist"

        # Test 5: Primitives are NOT deferred (they're cheap)
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__With_Primitives()
            assert obj.name == '', "name should be set"
            assert obj.count == 0, "count should be set"
            assert obj.active == False, "active should be set"

        # Test 6: User-provided kwargs bypass on-demand
        with Type_Safe__Config(on_demand_nested=True):
            custom_inner = TS__Inner(value='custom')
            obj = TS__With_One_Nested(inner=custom_inner)

            # inner was provided, should NOT be pending
            on_demand_types = object.__getattribute__(obj, '_on_demand__types')
            assert 'inner' not in on_demand_types, "provided inner should not be pending"
            assert obj.inner.value == 'custom', "provided inner should be used"