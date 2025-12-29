import sys
import pytest
from typing                                                                         import Dict
from unittest                                                                       import TestCase
from osbot_utils.testing.Pytest                                                     import skip__if_not__in_github_actions
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.Type_Safe__On_Demand                                     import Type_Safe__On_Demand
from osbot_utils.testing.performance.Performance_Measure__Session                   import Performance_Measure__Session
from osbot_utils.utils.Env                                                          import in_github_action


# =============================================================================
# Performance Tests
# =============================================================================

class test_perf__Type_Safe__On_Demand(TestCase):

    @classmethod
    def setUpClass(cls):                                                            # Warm up classes to ensure fair comparison
        skip__if_not__in_github_actions()                                           # although fast (about 320ms) we don't need to run this all the time locally :)
        _ = MGraph__Index__Eager()                                                  # Warm up eager
        _ = MGraph__Index__OnDemand()                                               # Warm up on-demand

    def test__object_creation_count__eager(self):                                   # Count objects created with eager (Type_Safe) initialization
        creation_count = {'value': 0}
        original_init = Type_Safe.__init__

        def counting_init(self, **kwargs):
            creation_count['value'] += 1
            original_init(self, **kwargs)

        Type_Safe.__init__ = counting_init
        try:
            _ = MGraph__Index__Eager()
            eager_count = creation_count['value']
        finally:
            Type_Safe.__init__ = original_init

        assert eager_count                        >= 40                             # Should create many objects
        # print(f"Eager objects created: {eager_count}")                            # Uncomment for debugging

    def test__object_creation_count__on_demand(self):                               # Count objects created with on-demand initialization
        creation_count = {'value': 0}
        original_init = Type_Safe.__init__

        def counting_init(self, **kwargs):
            creation_count['value'] += 1
            original_init(self, **kwargs)

        Type_Safe.__init__ = counting_init
        try:
            _ = MGraph__Index__OnDemand()
            on_demand_count = creation_count['value']
        finally:
            Type_Safe.__init__ = original_init

        assert on_demand_count                    == 1                              # Should create only 1 object
        # print(f"On-demand objects created: {on_demand_count}")                    # Uncomment for debugging

    def test__object_creation_count__comparison(self):                              # Compare object creation counts between both modes
        original_init = Type_Safe.__init__

        def count_creations(cls):
            count = {'value': 0}
            def counting_init(self, **kwargs):
                count['value'] += 1
                original_init(self, **kwargs)
            Type_Safe.__init__ = counting_init
            try:
                _ = cls()
                return count['value']
            finally:
                Type_Safe.__init__ = original_init

        eager_count     = count_creations(MGraph__Index__Eager)
        on_demand_count = count_creations(MGraph__Index__OnDemand)

        assert on_demand_count                    <  eager_count                    # On-demand creates fewer
        assert on_demand_count                    == 1                              # Specifically, just 1
        assert eager_count                        >= 40                             # Eager creates many

        reduction_pct = (eager_count - on_demand_count) / eager_count * 100
        assert reduction_pct                      >= 95                             # At least 95% reduction

    def test__construction_time__eager(self):                                       # Benchmark eager construction time
        with Performance_Measure__Session() as _:
            _.measure__quick(MGraph__Index__Eager)
            result = _.result

        # Eager should take significant time due to nested object creation
        assert result.final_score                 >  100_000                        # > 100µs (actually ~1.8ms)

    def test__construction_time__on_demand(self):                                   # Benchmark on-demand construction time
        with Performance_Measure__Session() as _:
            _.measure__quick(MGraph__Index__OnDemand)
            result = _.result

        target_ns = 200_000                                                         # 200µs target from original brief
        if in_github_action():
            target_ns = target_ns * 6                                               # CI is slower

        assert result.final_score                 <  target_ns                      # Must meet target

    def test__construction_time__comparison(self):                                  # Compare construction times and verify speedup
        with Performance_Measure__Session() as _:
            _.measure__quick(MGraph__Index__Eager)
            eager_result = _.result

        with Performance_Measure__Session() as _:
            _.measure__quick(MGraph__Index__OnDemand)
            on_demand_result = _.result

        eager_time     = eager_result.final_score
        on_demand_time = on_demand_result.final_score

        speedup = eager_time / on_demand_time

        # Verify significant speedup
        min_speedup = 5 if in_github_action() else 10                               # Lower threshold for CI
        assert speedup                            >= min_speedup                    # At least 10x speedup (5x in CI)
        # print(f"Speedup: {speedup:.1f}x")                                         # Uncomment for debugging

    def test__html_mgraph_simulation__six_indexes(self):                            # Simulate Html_MGraph's 6 index creation scenario
        with Performance_Measure__Session() as _:
            def create_six_eager():
                for i in range(6):
                    _ = MGraph__Index__Eager()
            _.measure__quick(create_six_eager)
            eager_6x = _.result

        with Performance_Measure__Session() as _:
            def create_six_on_demand():
                for i in range(6):
                    _ = MGraph__Index__OnDemand()
            _.measure__quick(create_six_on_demand)
            on_demand_6x = _.result

        eager_time_ms     = eager_6x.final_score / 1_000_000
        on_demand_time_ms = on_demand_6x.final_score / 1_000_000
        saved_ms          = eager_time_ms - on_demand_time_ms

        # Original problem: 6 indexes took ~11ms
        # Target: < 2ms for all 6
        target_ms = 12 if in_github_action() else 2                                 # Higher threshold for CI
        assert on_demand_time_ms                  <  target_ms

        # Verify meaningful savings
        assert saved_ms                           >  0                              # Must save time
        # print(f"6 indexes - Eager: {eager_time_ms:.1f}ms, On-demand: {on_demand_time_ms:.2f}ms, Saved: {saved_ms:.1f}ms")

    def test__target_200_microseconds(self):                                        # Explicit test for the 200µs target from the optimization brief
        with Performance_Measure__Session() as _:
            _.measure__quick(MGraph__Index__OnDemand)
            result = _.result

        target_ns   = 200_000                                                       # 200µs in nanoseconds
        actual_ns   = result.final_score
        actual_us   = actual_ns / 1000

        if in_github_action():
            target_ns = target_ns * 6                                               # CI multiplier

        assert actual_ns                          <= target_ns, f"Construction took {actual_us:.0f}µs, target was {target_ns/1000:.0f}µs"


    def test__construction_plus_partial_access(self):                               # Test construction + accessing some attributes
        with Performance_Measure__Session() as _:
            def eager_with_access():
                index = MGraph__Index__Eager()
                _ = index.edges_index                                               # Access one attribute
                _ = index.index_data
                return index
            _.measure__quick(eager_with_access)
            eager_result = _.result

        with Performance_Measure__Session() as _:
            def on_demand_with_access():
                index = MGraph__Index__OnDemand()
                _ = index.edges_index                                               # Triggers creation
                _ = index.index_data                                                # Triggers creation
                return index
            _.measure__quick(on_demand_with_access)
            on_demand_result = _.result

        # On-demand should still be faster even with partial access
        # because eager creates ALL objects while on-demand creates only what's accessed
        speedup = eager_result.final_score / on_demand_result.final_score

        min_speedup = 2 if in_github_action() else 5                                # Even with access, should be faster
        assert speedup                            >= min_speedup

    def test__construction_plus_full_access(self):                                  # Test construction + accessing all top-level attributes
        def access_all_eager():
            index = MGraph__Index__Eager()
            _ = index.index_data
            _ = index.edges_index
            _ = index.edit_index
            _ = index.labels_index
            _ = index.paths_index
            _ = index.query_index
            _ = index.stats_index
            _ = index.types_index
            _ = index.values_index
            _ = index.resolver
            return index

        def access_all_on_demand():
            index = MGraph__Index__OnDemand()
            _ = index.index_data
            _ = index.edges_index
            _ = index.edit_index
            _ = index.labels_index
            _ = index.paths_index
            _ = index.query_index
            _ = index.stats_index
            _ = index.types_index
            _ = index.values_index
            _ = index.resolver
            return index

        with Performance_Measure__Session() as _:
            _.measure__quick(access_all_eager)
            eager_result = _.result

        with Performance_Measure__Session() as _:
            _.measure__quick(access_all_on_demand)
            on_demand_result = _.result

        # Even with full top-level access, on-demand is still faster
        # because eager creates duplicate nested objects that are discarded
        speedup = eager_result.final_score / on_demand_result.final_score

        # With full access, speedup is smaller but should still exist
        # because on-demand avoids creating duplicate nested objects
        assert speedup                            >= 1.0                            # At minimum, not slower


class test_perf_Type_Safe__On_Demand__memory(TestCase):                             # Memory-related performance tests

    def test__pending_attributes_count(self):                                       # Verify correct number of attributes are pending
        index = MGraph__Index__OnDemand()
        pending_count = len(index._on_demand__types)

        # Should have 10 Type_Safe attributes pending
        assert pending_count                      == 10                             # All 10 top-level Type_Safe attrs

    def test__pending_reduces_on_access(self):                                      # Verify pending count reduces as attributes accessed
        index = MGraph__Index__OnDemand()
        initial_pending = len(index._on_demand__types)

        _ = index.edges_index                                                       # Access one
        after_one = len(index._on_demand__types)

        _ = index.labels_index                                                      # Access another
        after_two = len(index._on_demand__types)

        assert initial_pending                    == 10
        assert after_one                          == 9
        assert after_two                          == 8


# =============================================================================
# Test Classes: Simulated MGraph__Index Hierarchy (Type_Safe - Eager)
# =============================================================================

class Schema__Edges__Eager(Type_Safe):                                              # Leaf schema for edge data
    edges_to_nodes         : Dict[str, str]
    nodes_to_outgoing_edges: Dict[str, str]
    nodes_to_incoming_edges: Dict[str, str]

class Schema__Labels__Eager(Type_Safe):                                             # Leaf schema for label data
    edges_predicates       : Dict[str, str]
    edges_by_predicate     : Dict[str, str]
    edges_incoming_labels  : Dict[str, str]
    edges_by_incoming_label: Dict[str, str]
    edges_outgoing_labels  : Dict[str, str]
    edges_by_outgoing_label: Dict[str, str]

class Schema__Paths__Eager(Type_Safe):                                              # Leaf schema for path data
    nodes_by_path: Dict[str, str]
    edges_by_path: Dict[str, str]

class Schema__Types__Eager(Type_Safe):                                              # Leaf schema for type data
    nodes_types                    : Dict[str, str]
    nodes_by_type                  : Dict[str, str]
    edges_types                    : Dict[str, str]
    edges_by_type                  : Dict[str, str]
    nodes_to_incoming_edges_by_type: Dict[str, str]
    nodes_to_outgoing_edges_by_type: Dict[str, str]

class Schema__Values__Eager(Type_Safe):                                             # Leaf schema for value data
    hash_to_node  : Dict[str, str]
    node_to_hash  : Dict[str, str]
    values_by_type: Dict[str, str]
    type_by_value : Dict[str, str]

class Schema__Data__Eager(Type_Safe):                                               # Composite schema containing all leaf schemas
    edges : Schema__Edges__Eager
    labels: Schema__Labels__Eager
    paths : Schema__Paths__Eager
    types : Schema__Types__Eager

class Index__Edges__Eager(Type_Safe):                                               # Edge index component
    data: Schema__Edges__Eager

class Index__Labels__Eager(Type_Safe):                                              # Labels index component
    enabled: bool = True
    data   : Schema__Labels__Eager

class Index__Paths__Eager(Type_Safe):                                               # Paths index component
    enabled: bool = True
    data   : Schema__Paths__Eager

class Index__Types__Eager(Type_Safe):                                               # Types index component
    enabled: bool = True
    data   : Schema__Types__Eager

class Index__Values__Eager(Type_Safe):                                              # Values index component
    enabled   : bool = True
    index_data: Schema__Values__Eager

class Type__Resolver__Eager(Type_Safe):                                             # Type resolver component
    default_node_type: str = ""
    default_edge_type: str = ""

class Index__Edit__Eager(Type_Safe):                                                # Edit index - references multiple sub-indexes
    edges_index : Index__Edges__Eager
    labels_index: Index__Labels__Eager
    paths_index : Index__Paths__Eager
    types_index : Index__Types__Eager
    values_index: Index__Values__Eager
    resolver    : Type__Resolver__Eager

class Index__Query__Eager(Type_Safe):                                               # Query index - references multiple sub-indexes
    edges_index : Index__Edges__Eager
    labels_index: Index__Labels__Eager
    types_index : Index__Types__Eager
    values_index: Index__Values__Eager

class Index__Stats__Eager(Type_Safe):                                               # Stats index - references multiple sub-indexes
    edges_index : Index__Edges__Eager
    labels_index: Index__Labels__Eager
    paths_index : Index__Paths__Eager
    types_index : Index__Types__Eager

class MGraph__Index__Eager(Type_Safe):                                              # Main index class - simulates MGraph__Index
    index_data  : Schema__Data__Eager                                               # Contains all the hierarchy above
    edges_index : Index__Edges__Eager
    edit_index  : Index__Edit__Eager
    labels_index: Index__Labels__Eager
    paths_index : Index__Paths__Eager
    query_index : Index__Query__Eager
    stats_index : Index__Stats__Eager
    types_index : Index__Types__Eager
    values_index: Index__Values__Eager
    resolver    : Type__Resolver__Eager


# =============================================================================
# Test Classes: Simulated MGraph__Index Hierarchy (Type_Safe__On_Demand - Lazy)
# =============================================================================

class Schema__Edges__OnDemand(Type_Safe__On_Demand):                                # Leaf schema for edge data
    edges_to_nodes         : Dict[str, str]
    nodes_to_outgoing_edges: Dict[str, str]
    nodes_to_incoming_edges: Dict[str, str]

class Schema__Labels__OnDemand(Type_Safe__On_Demand):                               # Leaf schema for label data
    edges_predicates       : Dict[str, str]
    edges_by_predicate     : Dict[str, str]
    edges_incoming_labels  : Dict[str, str]
    edges_by_incoming_label: Dict[str, str]
    edges_outgoing_labels  : Dict[str, str]
    edges_by_outgoing_label: Dict[str, str]

class Schema__Paths__OnDemand(Type_Safe__On_Demand):                                # Leaf schema for path data
    nodes_by_path: Dict[str, str]
    edges_by_path: Dict[str, str]

class Schema__Types__OnDemand(Type_Safe__On_Demand):                                # Leaf schema for type data
    nodes_types                    : Dict[str, str]
    nodes_by_type                  : Dict[str, str]
    edges_types                    : Dict[str, str]
    edges_by_type                  : Dict[str, str]
    nodes_to_incoming_edges_by_type: Dict[str, str]
    nodes_to_outgoing_edges_by_type: Dict[str, str]

class Schema__Values__OnDemand(Type_Safe__On_Demand):                               # Leaf schema for value data
    hash_to_node  : Dict[str, str]
    node_to_hash  : Dict[str, str]
    values_by_type: Dict[str, str]
    type_by_value : Dict[str, str]

class Schema__Data__OnDemand(Type_Safe__On_Demand):                                 # Composite schema containing all leaf schemas
    edges : Schema__Edges__OnDemand
    labels: Schema__Labels__OnDemand
    paths : Schema__Paths__OnDemand
    types : Schema__Types__OnDemand

class Index__Edges__OnDemand(Type_Safe__On_Demand):                                 # Edge index component
    data: Schema__Edges__OnDemand

class Index__Labels__OnDemand(Type_Safe__On_Demand):                                # Labels index component
    enabled: bool = True
    data   : Schema__Labels__OnDemand

class Index__Paths__OnDemand(Type_Safe__On_Demand):                                 # Paths index component
    enabled: bool = True
    data   : Schema__Paths__OnDemand

class Index__Types__OnDemand(Type_Safe__On_Demand):                                 # Types index component
    enabled: bool = True
    data   : Schema__Types__OnDemand

class Index__Values__OnDemand(Type_Safe__On_Demand):                                # Values index component
    enabled   : bool = True
    index_data: Schema__Values__OnDemand

class Type__Resolver__OnDemand(Type_Safe__On_Demand):                               # Type resolver component
    default_node_type: str = ""
    default_edge_type: str = ""

class Index__Edit__OnDemand(Type_Safe__On_Demand):                                  # Edit index - references multiple sub-indexes
    edges_index : Index__Edges__OnDemand
    labels_index: Index__Labels__OnDemand
    paths_index : Index__Paths__OnDemand
    types_index : Index__Types__OnDemand
    values_index: Index__Values__OnDemand
    resolver    : Type__Resolver__OnDemand

class Index__Query__OnDemand(Type_Safe__On_Demand):                                 # Query index - references multiple sub-indexes
    edges_index : Index__Edges__OnDemand
    labels_index: Index__Labels__OnDemand
    types_index : Index__Types__OnDemand
    values_index: Index__Values__OnDemand

class Index__Stats__OnDemand(Type_Safe__On_Demand):                                 # Stats index - references multiple sub-indexes
    edges_index : Index__Edges__OnDemand
    labels_index: Index__Labels__OnDemand
    paths_index : Index__Paths__OnDemand
    types_index : Index__Types__OnDemand

class MGraph__Index__OnDemand(Type_Safe__On_Demand):                                # Main index class - simulates MGraph__Index with on-demand
    index_data  : Schema__Data__OnDemand
    edges_index : Index__Edges__OnDemand
    edit_index  : Index__Edit__OnDemand
    labels_index: Index__Labels__OnDemand
    paths_index : Index__Paths__OnDemand
    query_index : Index__Query__OnDemand
    stats_index : Index__Stats__OnDemand
    types_index : Index__Types__OnDemand
    values_index: Index__Values__OnDemand
    resolver    : Type__Resolver__OnDemand

