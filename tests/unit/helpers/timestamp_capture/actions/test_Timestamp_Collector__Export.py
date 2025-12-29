import json
import time
from unittest                                                                         import TestCase
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector                        import Timestamp_Collector
from osbot_utils.helpers.timestamp_capture.actions.Timestamp_Collector__Export        import Timestamp_Collector__Export
from osbot_utils.helpers.timestamp_capture.decorators.timestamp                       import timestamp
from osbot_utils.helpers.timestamp_capture.context_managers.timestamp_block           import timestamp_block
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Call_Tree_Node      import Schema__Call_Tree_Node
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Export_Full         import Schema__Export_Full
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Export_Summary      import Schema__Export_Summary
from osbot_utils.helpers.timestamp_capture.schemas.speedscope.Schema__Speedscope      import Schema__Speedscope
from osbot_utils.testing.Pytest import skip_if_in_github_action
from osbot_utils.testing.__                                                           import __, __LESS_THAN__, __BETWEEN__, __SKIP__
from osbot_utils.utils.Env import in_github_action
from osbot_utils.utils.Json                                                           import json_to_str


class test_Timestamp_Collector__Export(TestCase):

    @classmethod
    def setUpClass(cls):                                                                  # Create collector with sample data
        cls.collector = Timestamp_Collector(name="export_test")
        _timestamp_collector_ = cls.collector
        cls.create_timestamp_entries()

    @classmethod
    def create_timestamp_entries(cls):

        @timestamp
        def outer():
            inner_a()
            inner_b()

        @timestamp
        def inner_a():
            leaf()

        @timestamp
        def inner_b():
            pass

        @timestamp
        def leaf():
            pass

        with cls.collector:            # this starts and stop the collector
            outer()

        cls.export = Timestamp_Collector__Export(collector=cls.collector)

    def test__setup(self):                                          # name with __ so that it executes first
        skip_if_in_github_action()                                  # even with delta this test was very flaky in GH actions
        assert len(self.collector.entries)        == 8
        assert type(self.export)                  is Timestamp_Collector__Export

        if in_github_action():
            delta = 5
        else:
            delta = 1
        with self.export.to_export_summary() as _:
            assert type(_)                        is Schema__Export_Summary
            assert _.total_duration_ms            < 0.30 * delta
            assert _.hotspots[0].self_ms          < 0.08 * delta

            # explicit asserts derived from _.obj() comparison
            assert _.name                         == 'export_test'
            assert _.method_count                 == 4
            assert _.entry_count                  == 8
            assert len(_.hotspots)                == 4

            # hotspot 0
            assert _.hotspots[0].name             == 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.outer'
            assert _.hotspots[0].self_ms           < 0.08 * delta
            assert 20                             <= _.hotspots[0].percentage <= 45
            assert _.hotspots[0].calls            == 1

            # hotspot 1
            assert _.hotspots[1].name             == 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.inner_a'
            assert _.hotspots[1].self_ms           < 0.05 * delta
            assert 20                             <= _.hotspots[1].percentage <= 25
            assert _.hotspots[1].calls            == 1

            # hotspot 2
            assert _.hotspots[2].name             == 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.leaf'
            assert _.hotspots[2].self_ms           < 0.05 * delta
            assert 10                             <= _.hotspots[2].percentage <= 15
            assert _.hotspots[2].calls            == 1

            # hotspot 3
            assert _.hotspots[3].name             == 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.inner_b'
            assert _.hotspots[3].self_ms           < 0.05 * delta
            assert 5                              <= _.hotspots[3].percentage <= 15
            assert _.hotspots[3].calls            == 1

            # full object comparison (authoritative)
            assert _.obj() == __(name              = 'export_test' ,
                                 total_duration_ms= __LESS_THAN__(0.20 * delta),
                                 method_count     = 4              ,
                                 entry_count      = 8              ,
                                 hotspots         = [
                                     __(name       = 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.outer'  ,
                                        self_ms    = __LESS_THAN__(0.08 * delta),
                                        percentage = __BETWEEN__(35, 45),
                                        calls      = 1),
                                     __(name       = 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.inner_a',
                                        self_ms    = __LESS_THAN__(0.05 * delta),
                                        percentage = __BETWEEN__(20, 25),
                                        calls      = 1),
                                     __(name       = 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.leaf'   ,
                                        self_ms    = __LESS_THAN__(0.05 * delta),
                                        percentage = __BETWEEN__(10, 15),
                                        calls      = 1),
                                     __(name       = 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.inner_b',
                                        self_ms    = __LESS_THAN__(0.05 * delta),
                                        percentage = __BETWEEN__(5 , 15),
                                        calls      = 1)
                                 ])


    # ═══════════════════════════════════════════════════════════════════════════════
    # Call Tree Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_build_call_tree(self):                                                   # Test call tree construction
        roots = self.export.build_call_tree()

        assert len(roots) == 1                                                        # One top-level call (outer)
        root = roots[0]

        assert isinstance(root, Schema__Call_Tree_Node)
        assert root.name       == 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.outer'
        assert root.depth      == 0
        assert len(root.children) == 2                                                # inner_a and inner_b

        inner_a = root.children[0]
        assert inner_a.name == 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.inner_a'
        assert inner_a.depth == 1
        assert len(inner_a.children) == 1                                             # leaf

        inner_b = root.children[1]
        assert inner_b.name == 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.inner_b'
        assert inner_b.depth == 1
        assert len(inner_b.children) == 0                                             # No children

        leaf = inner_a.children[0]
        assert leaf.name == 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.leaf'
        assert leaf.depth == 2
        assert len(leaf.children) == 0

    def test_build_call_tree__durations(self):                                        # Test duration calculations
        roots = self.export.build_call_tree()
        root  = roots[0]

        # All nodes should have duration > 0
        assert root.duration_ns > 0
        assert root.duration_ms > 0
        for child in root.children:
            assert child.duration_ns > 0

        # Parent duration should be >= sum of children
        child_total = sum(c.duration_ns for c in root.children)
        assert root.duration_ns >= child_total

    def test_build_call_tree__self_time(self):                                        # Test self-time calculation
        roots = self.export.build_call_tree()
        root  = roots[0]

        # Self-time = duration - children duration
        child_total = sum(c.duration_ns for c in root.children)
        assert root.self_ns == root.duration_ns - child_total

        # Leaf nodes have self_ns == duration_ns
        leaf = root.children[0].children[0]
        assert leaf.self_ns == leaf.duration_ns

    def test_call_tree_node__json_roundtrip(self):                                    # Test Type_Safe JSON roundtrip
        roots    = self.export.build_call_tree()
        root     = roots[0]
        json_str = root.json()

        # Verify it's valid JSON
        parsed = json.loads(json_to_str(json_str))
        assert parsed['name'] == 'test_Timestamp_Collector__Export.create_timestamp_entries.<locals>.outer'
        assert 'children' in parsed

        # Roundtrip back to object
        restored = Schema__Call_Tree_Node.from_json(json_str)
        assert restored.name        == root.name
        assert restored.duration_ns == root.duration_ns
        assert len(restored.children) == len(root.children)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Flame Graph Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_to_flame_graph_stacks(self):                                             # Test flame graph format
        stacks = self.export.to_flame_graph_stacks()

        assert isinstance(stacks, list)
        assert len(stacks) > 0

        # Each stack should be "path;path;path value"
        for stack in stacks:
            parts = stack.rsplit(' ', 1)
            assert len(parts) == 2
            path, value = parts
            assert path                                                               # Non-empty path
            assert value.isdigit()

    def test_to_flame_graph_stacks__paths(self):                                      # Test stack paths are correct
        stacks = self.export.to_flame_graph_stacks()
        paths  = [s.rsplit(' ', 1)[0] for s in stacks]

        # Should have a path with outer -> inner_a -> leaf nesting (separated by ;)
        def has_nested_sequence(path, *names):
            parts = path.split(';')
            part_names = [p.split('.')[-1] for p in parts]                            # Get last segment of each qualified name
            return list(names) == part_names

        assert any(has_nested_sequence(p, 'outer', 'inner_a', 'leaf') for p in paths)

    def test_to_flame_graph_string(self):                                             # Test flame graph as string
        result = self.export.to_flame_graph_string()

        assert isinstance(result, str)
        assert '\n' in result                                                         # Multiple lines
        assert 'outer' in result

    # ═══════════════════════════════════════════════════════════════════════════════
    # Full Export Tests (Type_Safe Schema)
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_to_export_full(self):                                                    # Test full export schema
        export_full = self.export.to_export_full()
        perf_counter__now = time.perf_counter_ns()
        assert type(export_full) is Schema__Export_Full
        assert export_full.obj() == __(metadata=__(name='export_test',
                                                   total_duration_ns =__LESS_THAN__(500000),
                                                   total_duration_ms =__LESS_THAN__(1),
                                                   entry_count       = 8,
                                                   method_count      = 4,
                                                   start_time_ns     = __LESS_THAN__(perf_counter__now),
                                                   end_time_ns       = __LESS_THAN__(perf_counter__now)),
                                       entries=__SKIP__,
                                       method_timings=__SKIP__,
                                       call_tree=__SKIP__)


        assert isinstance(export_full, Schema__Export_Full)
        assert export_full.metadata.name == 'export_test'
        assert export_full.metadata.total_duration_ns > 0
        assert export_full.metadata.entry_count == 8                                  # 4 methods × 2 (enter/exit)

        assert len(export_full.entries) == 8
        assert len(export_full.method_timings) == 4                                   # outer, inner_a, inner_b, leaf
        assert len(export_full.call_tree) == 1

    def test_to_export_full__json_roundtrip(self):                                    # Test full export JSON roundtrip
        export_full         = self.export.to_export_full()
        export_full__dict   = export_full.json()
        export_full__str    = json_to_str(export_full__dict)
        restored            = Schema__Export_Full.from_json(export_full__dict)
        parsed              = json.loads(export_full__str)

        # Verify valid JSON
        assert type(export_full) is Schema__Export_Full
        assert 'metadata'  in parsed
        assert 'call_tree' in parsed

        # Roundtrip
        assert restored.metadata.name        == export_full.metadata.name
        assert restored.metadata.entry_count == export_full.metadata.entry_count
        assert len(restored.entries)         == len(export_full.entries)

    def test_to_json(self):                                                           # Test JSON export convenience method
        json_str = self.export.to_json()

        assert isinstance(json_str, dict)
        parsed = json.loads(json_to_str(json_str))
        assert parsed['metadata']['name'] == 'export_test'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Summary Export Tests (Type_Safe Schema)
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_to_export_summary(self):                                                 # Test summary export schema
        summary = self.export.to_export_summary()

        assert isinstance(summary, Schema__Export_Summary)
        assert summary.name == 'export_test'
        assert summary.total_duration_ms > 0
        assert summary.method_count == 4
        assert len(summary.hotspots) <= 10

    def test_to_export_summary__json_roundtrip(self):                                 # Test summary JSON roundtrip
        summary  = self.export.to_export_summary()
        json_str = summary.json()

        parsed = json.loads(json_to_str(json_str))
        assert parsed['name'] == 'export_test'
        assert 'hotspots' in parsed

        # Roundtrip
        restored = Schema__Export_Summary.from_json(json_str)
        assert restored.name         == summary.name
        assert restored.method_count == summary.method_count

    def test_to_summary_json(self):                                                   # Test summary JSON convenience method
        json_str = self.export.to_summary_json()
        parsed   = json.loads(json_to_str(json_str))

        assert parsed['name'] == 'export_test'
        assert 'hotspots' in parsed

    # ═══════════════════════════════════════════════════════════════════════════════
    # Speedscope Format Tests (Type_Safe Schema)
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_to_speedscope(self):                                                     # Test speedscope schema
        speedscope = self.export.to_speedscope()

        assert isinstance(speedscope, Schema__Speedscope)
        assert speedscope.name == 'export_test'
        assert len(speedscope.profiles) == 1

        profile = speedscope.profiles[0]
        assert profile.type == 'evented'
        assert profile.unit == 'microseconds'
        assert len(profile.events) == 8                                               # 4 methods × 2 (O/C)

    def test_to_speedscope__events(self):                                             # Test speedscope events
        speedscope = self.export.to_speedscope()
        events     = speedscope.profiles[0].events

        assert len(events) == 8

        # First event should be Open for outer
        assert events[0].type == 'O'

        # Should have matching O/C pairs
        opens  = sum(1 for e in events if e.type == 'O')
        closes = sum(1 for e in events if e.type == 'C')
        assert opens == closes == 4

    def test_to_speedscope_json(self):                                                # Test speedscope JSON
        json_str = self.export.to_speedscope_json()
        parsed   = json.loads(json_str)

        assert parsed['$schema'] == 'https://www.speedscope.app/file-format-schema.json'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_empty_collector(self):                                                   # Test with no entries
        empty_collector = Timestamp_Collector(name="empty")
        export = Timestamp_Collector__Export(collector=empty_collector)

        # Should not crash
        tree      = export.build_call_tree()
        stacks    = export.to_flame_graph_stacks()
        full      = export.to_export_full()
        summary   = export.to_export_summary()
        speedscope = export.to_speedscope()

        assert tree    == []
        assert stacks  == []
        assert len(full.entries) == 0

    def test_multiple_roots(self):                                                    # Test multiple top-level calls
        _timestamp_collector_ = Timestamp_Collector(name="multi_root")

        @timestamp(name='first')
        def first():
            pass

        @timestamp(name='second')
        def second():
            pass

        with _timestamp_collector_:
            first()
            second()

        export = Timestamp_Collector__Export(collector=_timestamp_collector_)
        roots  = export.build_call_tree()

        assert len(roots) == 2
        assert roots[0].name == 'first'
        assert roots[1].name == 'second'

    def test_with_timestamp_block(self):                                              # Test with timestamp_block
        _timestamp_collector_ = Timestamp_Collector(name="with_blocks")

        with _timestamp_collector_:
            with timestamp_block("phase_1"):
                with timestamp_block("phase_1.sub"):
                    pass
            with timestamp_block("phase_2"):
                pass

        export = Timestamp_Collector__Export(collector=_timestamp_collector_)
        roots  = export.build_call_tree()

        assert len(roots) == 2
        assert roots[0].name == 'phase_1'
        assert roots[1].name == 'phase_2'
        assert len(roots[0].children) == 1
        assert roots[0].children[0].name == 'phase_1.sub'

    # def test__create_speedscope_file(self):
    #     speedscope = self.export.to_speedscope_file('./speedscope-test-file.js')
    #     print(speedscope)