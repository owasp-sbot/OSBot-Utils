# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Hypothesis F - Schema-Based Fast Create
# Compares: Normal Type_Safe vs fast_create
# ═══════════════════════════════════════════════════════════════════════════════
#
# BASELINE (Before): Normal Type_Safe.__init__ (full process)
#
# HYPOTHESIS (After): fast_create=True (schema-based direct __dict__ assignment)
#
# Expected: 25-50x faster for complex classes
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import Dict, List
from unittest                                                                                 import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                         import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Hypothesis                     import Perf_Benchmark__Hypothesis
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import Type_Safe__Config
from osbot_utils.utils.Env                                                                    import not_in_github_action
from osbot_utils.utils.Files                                                                  import path_combine

from Type_Safe__Fast_Create__Schema                                                           import clear_schema_cache, get_or_create_schema
from Type_Safe__Hypothesis_F                                                                  import Type_Safe__Hypothesis_F, fast_create, warm_schema_cache


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes - Various complexity levels
# ═══════════════════════════════════════════════════════════════════════════════

# Simple - no nesting, few fields
class TS__Empty(Type_Safe__Hypothesis_F):
    pass

class TS__Primitives_Only(Type_Safe__Hypothesis_F):
    name   : str  = ''
    count  : int  = 0
    active : bool = False
    value  : float = 0.0

class TS__With_Collections(Type_Safe__Hypothesis_F):
    name   : str = ''
    items  : List[str]
    data   : Dict[str, int]


# Nested classes
class TS__Inner(Type_Safe__Hypothesis_F):
    value : str = ''
    count : int = 0

class TS__One_Nested(Type_Safe__Hypothesis_F):
    inner : TS__Inner
    name  : str = ''

class TS__Three_Nested(Type_Safe__Hypothesis_F):
    child1 : TS__Inner
    child2 : TS__Inner
    child3 : TS__Inner
    name   : str = ''


# Deep nesting
class TS__Level3(Type_Safe__Hypothesis_F):
    data : str = ''

class TS__Level2(Type_Safe__Hypothesis_F):
    level3 : TS__Level3
    value  : int = 0

class TS__Level1(Type_Safe__Hypothesis_F):
    level2 : TS__Level2
    name   : str = ''

class TS__Deep_Nested(Type_Safe__Hypothesis_F):
    level1 : TS__Level1
    count  : int = 0


# Complex - simulates MGraph structures
class TS__Schema__Data(Type_Safe__Hypothesis_F):
    items  : Dict[str, str]
    labels : Dict[str, str]

class TS__Index__Edges(Type_Safe__Hypothesis_F):
    data : TS__Schema__Data
    name : str = ''

class TS__Index__Nodes(Type_Safe__Hypothesis_F):
    data : TS__Schema__Data
    name : str = ''

class TS__MGraph_Like(Type_Safe__Hypothesis_F):
    """Simulates MGraph__Index with multiple indexes"""
    edges_index : TS__Index__Edges
    nodes_index : TS__Index__Nodes
    count       : int = 0


# Many fields
class TS__Many_Fields(Type_Safe__Hypothesis_F):
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

def run_baseline_benchmarks(timing: Perf_Benchmark__Timing):                                  # fast_create=FALSE
    """Normal Type_Safe creation (full __init__ process)"""

    with Type_Safe__Config(fast_create=False):

        # Simple classes
        timing.benchmark('A_01__empty'              , TS__Empty                                       )
        timing.benchmark('A_02__primitives_only'    , TS__Primitives_Only                             )
        timing.benchmark('A_03__with_collections'   , TS__With_Collections                            )
        timing.benchmark('A_04__many_fields'        , TS__Many_Fields                                 )

        # Nested classes
        timing.benchmark('A_05__one_nested'         , TS__One_Nested                                  )
        timing.benchmark('A_06__three_nested'       , TS__Three_Nested                                )
        timing.benchmark('A_07__deep_nested'        , TS__Deep_Nested                                 )
        timing.benchmark('A_08__mgraph_like'        , TS__MGraph_Like                                 )

        # Batch creation
        timing.benchmark('B_01__primitives_x10'     , lambda: [TS__Primitives_Only() for _ in range(10)])
        timing.benchmark('B_02__many_fields_x10'    , lambda: [TS__Many_Fields() for _ in range(10)]  )
        timing.benchmark('B_03__three_nested_x10'   , lambda: [TS__Three_Nested() for _ in range(10)] )
        timing.benchmark('B_04__mgraph_like_x10'    , lambda: [TS__MGraph_Like() for _ in range(10)]  )


def run_hypothesis_benchmarks(timing: Perf_Benchmark__Timing):                                # fast_create=TRUE
    """Schema-based fast creation (bypasses __init__)"""

    # Pre-warm schema cache (normally done once at startup)
    warm_schema_cache(TS__Empty)
    warm_schema_cache(TS__Primitives_Only)
    warm_schema_cache(TS__With_Collections)
    warm_schema_cache(TS__Many_Fields)
    warm_schema_cache(TS__One_Nested)
    warm_schema_cache(TS__Three_Nested)
    warm_schema_cache(TS__Deep_Nested)
    warm_schema_cache(TS__MGraph_Like)

    with Type_Safe__Config(fast_create=True):

        # Simple classes
        timing.benchmark('A_01__empty'              , TS__Empty                                       )
        timing.benchmark('A_02__primitives_only'    , TS__Primitives_Only                             )
        timing.benchmark('A_03__with_collections'   , TS__With_Collections                            )
        timing.benchmark('A_04__many_fields'        , TS__Many_Fields                                 )

        # Nested classes
        timing.benchmark('A_05__one_nested'         , TS__One_Nested                                  )
        timing.benchmark('A_06__three_nested'       , TS__Three_Nested                                )
        timing.benchmark('A_07__deep_nested'        , TS__Deep_Nested                                 )
        timing.benchmark('A_08__mgraph_like'        , TS__MGraph_Like                                 )

        # Batch creation
        timing.benchmark('B_01__primitives_x10'     , lambda: [TS__Primitives_Only() for _ in range(10)])
        timing.benchmark('B_02__many_fields_x10'    , lambda: [TS__Many_Fields() for _ in range(10)]  )
        timing.benchmark('B_03__three_nested_x10'   , lambda: [TS__Three_Nested() for _ in range(10)] )
        timing.benchmark('B_04__mgraph_like_x10'    , lambda: [TS__MGraph_Like() for _ in range(10)]  )


class test_perf__Hypothesis_F(TestCase):

    def test__hypothesis_f__fast_create(self):
        """
        HYPOTHESIS F: Schema-Based Fast Create

        Baseline: Normal Type_Safe.__init__ (full process)
        Hypothesis: fast_create=True (schema-based direct __dict__ assignment)

        Expected: 25-50x faster for complex classes
        """
        # Clear schema cache to ensure fair comparison
        clear_schema_cache()

        output_path = path_combine(__file__, '../')

        hypothesis = Perf_Benchmark__Hypothesis(
            description        = 'Hypothesis F: fast_create (schema-based)',
            target_improvement = 0.5,                                                         # Expect 50%+ improvement
            comments           = 'Schema-based creation bypassing Type_Safe.__init__'
        )

        # ═══════════════════════════════════════════════════════════════════════
        # Warmup
        # ═══════════════════════════════════════════════════════════════════════

        hypothesis.run_before(run_baseline_benchmarks)                                        # Warmup

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

            if not_in_github_action():
                hypothesis.print_report()
                hypothesis.save_report(path_combine(output_path, 'hypothesis_f_report.txt'))
                hypothesis.save(path_combine(output_path, 'hypothesis_f_result.json'))

        # ═══════════════════════════════════════════════════════════════════════
        # Verify fast_create behavior
        # ═══════════════════════════════════════════════════════════════════════

        self.verify_fast_create_behavior()

    def verify_fast_create_behavior(self):
        """Verify fast_create produces correct objects"""

        # Test 1: Object type is correct
        with Type_Safe__Config(fast_create=True):
            obj = TS__Primitives_Only()
            assert type(obj) is TS__Primitives_Only, f"Type should be TS__Primitives_Only, got {type(obj)}"
            assert isinstance(obj, Type_Safe__Hypothesis_F), "Should be Type_Safe__Hypothesis_F instance"

        # Test 2: Default values are set
        with Type_Safe__Config(fast_create=True):
            obj = TS__Primitives_Only()
            assert obj.name == '', f"name should be '', got {obj.name}"
            assert obj.count == 0, f"count should be 0, got {obj.count}"
            assert obj.active == False, f"active should be False, got {obj.active}"

        # Test 3: kwargs are applied
        with Type_Safe__Config(fast_create=True):
            obj = TS__Primitives_Only(name='test', count=42)
            assert obj.name == 'test', f"name should be 'test', got {obj.name}"
            assert obj.count == 42, f"count should be 42, got {obj.count}"

        # Test 4: Collections are fresh instances (not shared)
        with Type_Safe__Config(fast_create=True):
            obj1 = TS__With_Collections()
            obj2 = TS__With_Collections()
            obj1.items.append('item')
            assert len(obj2.items) == 0, "Collections should not be shared"

        # Test 5: Nested objects are created
        with Type_Safe__Config(fast_create=True):
            obj = TS__One_Nested()
            assert obj.inner is not None, "inner should be created"
            assert isinstance(obj.inner, TS__Inner), f"inner should be TS__Inner, got {type(obj.inner)}"

        # Test 6: Deep nesting works
        with Type_Safe__Config(fast_create=True):
            obj = TS__Deep_Nested()
            assert obj.level1 is not None, "level1 should exist"
            assert obj.level1.level2 is not None, "level2 should exist"
            assert obj.level1.level2.level3 is not None, "level3 should exist"
            assert obj.level1.level2.level3.data == '', "deep access should work"

        # Test 7: json() works on fast_created objects
        with Type_Safe__Config(fast_create=True):
            obj = TS__Primitives_Only(name='json_test', count=99)
            json_data = obj.json()
            assert json_data['name'] == 'json_test', "json() should work"
            assert json_data['count'] == 99, "json() should include all fields"

        # Test 8: __setattr__ validation still works after creation
        with Type_Safe__Config(fast_create=True):
            obj = TS__Primitives_Only()
            obj.name = 'valid'  # Should work
            assert obj.name == 'valid'

            # Type validation should still work on subsequent sets
            # (This tests that the object is properly set up)
            try:
                obj.count = 'not_an_int'  # Should fail validation
                assert False, "Should have raised TypeError"
            except (TypeError, ValueError):
                pass  # Expected

    def test__schema_generation(self):
        """Test that schema is generated correctly"""
        clear_schema_cache()

        schema = get_or_create_schema(TS__Primitives_Only)

        # Check schema structure
        assert schema.target_class is TS__Primitives_Only
        assert len(schema.fields) == 4  # name, count, active, value

        # All fields should be static (primitives)
        for field in schema.fields:
            assert field.mode == 'static', f"Field {field.name} should be static"

        # Static dict should have all defaults
        assert schema.static_dict['name'] == ''
        assert schema.static_dict['count'] == 0
        assert schema.static_dict['active'] == False

    def test__schema_with_collections(self):
        """Test schema for class with collections"""
        clear_schema_cache()

        schema = get_or_create_schema(TS__With_Collections)

        # name is static, items and data are factory
        assert len(schema.factory_fields) == 2

        factory_names = [f.name for f in schema.factory_fields]
        assert 'items' in factory_names
        assert 'data' in factory_names

    def test__schema_with_nested(self):
        """Test schema for class with nested Type_Safe"""
        clear_schema_cache()

        schema = get_or_create_schema(TS__One_Nested)

        # Should have one nested field
        assert len(schema.nested_fields) == 1
        assert schema.nested_fields[0].name == 'inner'
        assert schema.nested_fields[0].nested_class is TS__Inner