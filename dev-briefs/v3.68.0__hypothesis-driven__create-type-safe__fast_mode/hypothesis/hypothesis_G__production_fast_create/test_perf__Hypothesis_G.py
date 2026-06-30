# ═══════════════════════════════════════════════════════════════════════════════
# Performance Test: Hypothesis G - Production-Ready Fast Create
# Compares: Normal Type_Safe vs fast_create (schema-based)
# ═══════════════════════════════════════════════════════════════════════════════
#
# BASELINE (Before): Normal Type_Safe.__init__ (full process)
#
# HYPOTHESIS (After): fast_create=True (schema-based direct __dict__ assignment)
#
# Expected: 50%+ improvement (targeting parity with Hypothesis F)
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                       import Dict, List
from unittest                                                                     import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing             import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Hypothesis         import Perf_Benchmark__Hypothesis
from osbot_utils.utils.Env                                                        import not_in_github_action
from osbot_utils.utils.Files                                                      import path_combine
from Type_Safe__Config                                                            import Type_Safe__Config
from Type_Safe__Hypothesis_G                                                      import Type_Safe__Hypothesis_G
from Type_Safe__Fast_Create__Cache                                                import type_safe_fast_create_cache


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes - Various complexity levels
# ═══════════════════════════════════════════════════════════════════════════════

# Simple - no nesting, few fields
class TS__Empty(Type_Safe__Hypothesis_G):
    pass


class TS__Primitives_Only(Type_Safe__Hypothesis_G):
    name   : str   = ''
    count  : int   = 0
    active : bool  = False
    value  : float = 0.0


class TS__With_Collections(Type_Safe__Hypothesis_G):
    name  : str = ''
    items : List[str]
    data  : Dict[str, int]


# Nested classes
class TS__Inner(Type_Safe__Hypothesis_G):
    value : str = ''
    count : int = 0


class TS__One_Nested(Type_Safe__Hypothesis_G):
    inner : TS__Inner
    name  : str = ''


class TS__Three_Nested(Type_Safe__Hypothesis_G):
    child1 : TS__Inner
    child2 : TS__Inner
    child3 : TS__Inner
    name   : str = ''


# Deep nesting
class TS__Level3(Type_Safe__Hypothesis_G):
    data : str = ''


class TS__Level2(Type_Safe__Hypothesis_G):
    level3 : TS__Level3
    value  : int = 0


class TS__Level1(Type_Safe__Hypothesis_G):
    level2 : TS__Level2
    name   : str = ''


class TS__Deep_Nested(Type_Safe__Hypothesis_G):
    level1 : TS__Level1
    count  : int = 0


# Complex - simulates MGraph structures
class TS__Schema__Data(Type_Safe__Hypothesis_G):
    items  : Dict[str, str]
    labels : Dict[str, str]


class TS__Index__Edges(Type_Safe__Hypothesis_G):
    data : TS__Schema__Data
    name : str = ''


class TS__Index__Nodes(Type_Safe__Hypothesis_G):
    data : TS__Schema__Data
    name : str = ''


class TS__MGraph_Like(Type_Safe__Hypothesis_G):
    edges_index : TS__Index__Edges
    nodes_index : TS__Index__Nodes
    count       : int = 0


# Many fields
class TS__Many_Fields(Type_Safe__Hypothesis_G):
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

def run_baseline_benchmarks(timing: Perf_Benchmark__Timing):                      # fast_create=FALSE
    type_safe_fast_create_cache.clear_cache()

    with Type_Safe__Config(fast_create=False):

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


def run_hypothesis_benchmarks(timing: Perf_Benchmark__Timing):                    # fast_create=TRUE
    type_safe_fast_create_cache.clear_cache()

    # Pre-warm schema cache (normally done once at startup)
    type_safe_fast_create_cache.warm_cache(TS__Empty)
    type_safe_fast_create_cache.warm_cache(TS__Primitives_Only)
    type_safe_fast_create_cache.warm_cache(TS__With_Collections)
    type_safe_fast_create_cache.warm_cache(TS__Many_Fields)
    type_safe_fast_create_cache.warm_cache(TS__One_Nested)
    type_safe_fast_create_cache.warm_cache(TS__Three_Nested)
    type_safe_fast_create_cache.warm_cache(TS__Deep_Nested)
    type_safe_fast_create_cache.warm_cache(TS__MGraph_Like)

    with Type_Safe__Config(fast_create=True):

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

class test_perf__Hypothesis_G(TestCase):

    def test__hypothesis_g__fast_create(self):
        """
        HYPOTHESIS G: Production-Ready Fast Create

        Baseline: Normal Type_Safe.__init__ (full process)
        Hypothesis: fast_create=True (schema-based direct __dict__ assignment)

        Expected: 50%+ improvement (matching Hypothesis F)
        """
        type_safe_fast_create_cache.clear_cache()

        output_path = path_combine(__file__, '../')

        hypothesis = Perf_Benchmark__Hypothesis(description        = 'Hypothesis G: fast_create (production-ready)',
                                                target_improvement = 0.5                                           ,
                                                comments           = 'Schema-based creation bypassing Type_Safe.__init__')

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
            hypothesis.save_report(path_combine(output_path, 'hypothesis_g_report.txt'))
            hypothesis.save(path_combine(output_path, 'hypothesis_g_result.json'))



        # ═══════════════════════════════════════════════════════════════════════
        # Verify fast_create behavior
        # ═══════════════════════════════════════════════════════════════════════

        self.verify_fast_create_behavior()

    def verify_fast_create_behavior(self):                                        # Verify fast_create produces correct objects
        type_safe_fast_create_cache.clear_cache()

        # Test 1: Object type is correct
        with Type_Safe__Config(fast_create=True):
            obj = TS__Primitives_Only()
            assert type(obj)       is TS__Primitives_Only
            assert isinstance(obj, Type_Safe__Hypothesis_G)

        # Test 2: Default values are set
        with Type_Safe__Config(fast_create=True):
            obj = TS__Primitives_Only()
            assert obj.name   == ''
            assert obj.count  == 0
            assert obj.active == False
            assert obj.value  == 0.0

        # Test 3: kwargs are applied
        with Type_Safe__Config(fast_create=True):
            obj = TS__Primitives_Only(name='test', count=42)
            assert obj.name  == 'test'
            assert obj.count == 42

        # Test 4: Collections are fresh instances (not shared)
        with Type_Safe__Config(fast_create=True):
            obj1 = TS__With_Collections()
            obj2 = TS__With_Collections()
            obj1.items.append('item')
            assert len(obj2.items) == 0

        # Test 5: Nested objects are created
        with Type_Safe__Config(fast_create=True):
            obj = TS__One_Nested()
            assert obj.inner is not None
            assert isinstance(obj.inner, TS__Inner)

        # Test 6: Deep nesting works
        with Type_Safe__Config(fast_create=True):
            obj = TS__Deep_Nested()
            assert obj.level1                 is not None
            assert obj.level1.level2          is not None
            assert obj.level1.level2.level3   is not None
            assert obj.level1.level2.level3.data == ''

        # Test 7: json() works on fast_created objects
        with Type_Safe__Config(fast_create=True):
            obj       = TS__Primitives_Only(name='json_test', count=99)
            json_data = obj.json()
            assert json_data['name']  == 'json_test'
            assert json_data['count'] == 99

        # Test 8: __setattr__ validation still works after creation
        with Type_Safe__Config(fast_create=True):
            obj      = TS__Primitives_Only()
            obj.name = 'valid'
            assert obj.name == 'valid'

    def test__schema_generation(self):                                            # Test schema generation
        type_safe_fast_create_cache.clear_cache()

        schema = type_safe_fast_create_cache.get_schema(TS__Primitives_Only)

        assert schema.target_class is TS__Primitives_Only
        assert len(schema.fields)  == 4                                           # name, count, active, value

        for field in schema.fields:
            assert field.mode == 'static'

        assert schema.static_dict['name']   == ''
        assert schema.static_dict['count']  == 0
        assert schema.static_dict['active'] == False
        assert schema.static_dict['value']  == 0.0

    def test__schema_with_collections(self):                                      # Test schema with collections
        type_safe_fast_create_cache.clear_cache()

        schema = type_safe_fast_create_cache.get_schema(TS__With_Collections)

        assert len(schema.factory_fields) == 2

        factory_names = [f.name for f in schema.factory_fields]
        assert 'items' in factory_names
        assert 'data'  in factory_names

    def test__schema_with_nested(self):                                           # Test schema with nested Type_Safe
        type_safe_fast_create_cache.clear_cache()

        schema = type_safe_fast_create_cache.get_schema(TS__One_Nested)

        assert len(schema.nested_fields)          == 1
        assert schema.nested_fields[0].name       == 'inner'
        assert schema.nested_fields[0].nested_class is TS__Inner