"""
Timestamp Collector Export
===========================

Exports timestamp data in various formats using Type_Safe schemas:
- Full export (Schema__Export_Full)
- Summary export (Schema__Export_Summary)
- Speedscope format (Schema__Speedscope)
- Flame graph stacks (plain text)

All schema-based exports support .json() roundtrip serialization.
"""

from typing                                                                              import List
from osbot_utils.helpers.timestamp_capture.actions.Timestamp_Collector__Analysis         import Timestamp_Collector__Analysis
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Call_Tree_Node         import Schema__Call_Tree_Node
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Export_Metadata        import Schema__Export_Metadata
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Export_Entry           import Schema__Export_Entry
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Export_Method_Timing   import Schema__Export_Method_Timing
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Export_Full            import Schema__Export_Full
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Export_Hotspot         import Schema__Export_Hotspot
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Export_Summary         import Schema__Export_Summary
from osbot_utils.helpers.timestamp_capture.schemas.speedscope.Schema__Speedscope         import Schema__Speedscope
from osbot_utils.helpers.timestamp_capture.schemas.speedscope.Schema__Speedscope_Shared  import Schema__Speedscope_Shared
from osbot_utils.helpers.timestamp_capture.schemas.speedscope.Schema__Speedscope_Profile import Schema__Speedscope_Profile
from osbot_utils.helpers.timestamp_capture.schemas.speedscope.Schema__Speedscope_Frame   import Schema__Speedscope_Frame
from osbot_utils.helpers.timestamp_capture.schemas.speedscope.Schema__Speedscope_Event   import Schema__Speedscope_Event
from osbot_utils.helpers.timestamp_capture.static_methods.timestamp_utils                import method_timing__total_ms, method_timing__self_ms, method_timing__avg_ms
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector                           import Timestamp_Collector
from osbot_utils.utils.Json import json_to_str


class Timestamp_Collector__Export(Type_Safe):

    collector: Timestamp_Collector = None

    # ═══════════════════════════════════════════════════════════════════════════════
    # Call Tree Building
    # ═══════════════════════════════════════════════════════════════════════════════

    def build_call_tree(self) -> List[Schema__Call_Tree_Node]:                   # Build hierarchical call tree from flat entries
        entries = self.collector.entries
        if not entries:
            return []

        roots      = []                                                          # Top-level calls
        stack      = []                                                          # Stack of nodes for matching enter/exit
        call_index = 0

        i = 0
        while i < len(entries):
            entry = entries[i]

            if entry.event == 'enter':
                node = Schema__Call_Tree_Node(
                    name       = entry.name,
                    start_ns   = entry.timestamp_ns,
                    depth      = entry.depth,
                    call_index = call_index
                )
                call_index += 1

                if stack:
                    stack[-1].children.append(node)                              # Add as child of current
                else:
                    roots.append(node)                                           # Top-level call

                stack.append(node)

            elif entry.event == 'exit' and stack:
                node             = stack.pop()
                node.end_ns      = entry.timestamp_ns
                node.duration_ns = node.end_ns - node.start_ns
                node.duration_ms = node.duration_ns / 1_000_000

                # Calculate self-time (duration minus children)
                child_time   = sum(child.duration_ns for child in node.children)
                node.self_ns = node.duration_ns - child_time
                node.self_ms = node.self_ns / 1_000_000

            i += 1

        return roots

    # ═══════════════════════════════════════════════════════════════════════════════
    # Flame Graph Format
    # ═══════════════════════════════════════════════════════════════════════════════

    def to_flame_graph_stacks(self) -> List[str]:                                # Generate folded stack format for flame graphs
        """
        Generates folded stack format:
            root;child;grandchild 1234
            root;child;other 567

        Where the number is duration in microseconds.
        Compatible with flamegraph.pl and speedscope.
        """
        stacks = []
        roots  = self.build_call_tree()

        def traverse(node: Schema__Call_Tree_Node, path: List[str]):
            current_path = path + [node.name]

            if node.children:
                for child in node.children:
                    traverse(child, current_path)
                # Add self-time as a separate entry if significant
                if node.self_ns > 0:
                    stack_str = ";".join(current_path)
                    stacks.append(f"{stack_str} {node.self_ns // 1000}")         # Convert to μs
            else:
                # Leaf node - add full duration
                stack_str = ";".join(current_path)
                stacks.append(f"{stack_str} {node.duration_ns // 1000}")

        for root in roots:
            traverse(root, [])

        return stacks

    def to_flame_graph_string(self) -> str:                                      # Get flame graph data as single string
        return "\n".join(self.to_flame_graph_stacks())

    # ═══════════════════════════════════════════════════════════════════════════════
    # Full Export (Type_Safe Schema)
    # ═══════════════════════════════════════════════════════════════════════════════

    def to_export_full(self) -> Schema__Export_Full:                             # Export all data as Type_Safe schema
        analysis = Timestamp_Collector__Analysis(collector=self.collector)

        # Build metadata
        metadata = Schema__Export_Metadata(
            name              = self.collector.name,
            total_duration_ns = self.collector.total_duration_ns(),
            total_duration_ms = self.collector.total_duration_ms(),
            entry_count       = self.collector.entry_count(),
            method_count      = self.collector.method_count(),
            start_time_ns     = self.collector.start_time_ns,
            end_time_ns       = self.collector.end_time_ns,
        )

        # Build entries list
        entries = [Schema__Export_Entry(name         = e.name,
                                        event        = e.event,
                                        timestamp_ns = e.timestamp_ns,
                                        clock_ns     = e.clock_ns,
                                        depth        = e.depth,
                                        thread_id    = e.thread_id)
                for e in self.collector.entries]

        # Build method timings list
        method_timings = [Schema__Export_Method_Timing( name       = mt.name,
                                                        call_count = mt.call_count,
                                                        total_ns   = mt.total_ns,
                                                        total_ms   = method_timing__total_ms(mt),
                                                        self_ns    = mt.self_ns,
                                                        self_ms    = method_timing__self_ms(mt),
                                                        avg_ms     = method_timing__avg_ms(mt),
                                                        min_ns     = mt.min_ns,
                                                        max_ns     = mt.max_ns,)
                            for mt in analysis.get_timings_by_total()]

        # Build call tree
        call_tree = self.build_call_tree()

        return Schema__Export_Full(metadata       = metadata        ,
                                   entries        = entries         ,
                                   method_timings = method_timings  ,
                                   call_tree      = call_tree       )

    def to_json(self) -> str:                                   # Export as JSON string via Type_Safe
        return self.to_export_full().json()

    def to_json_file(self, filepath: str) -> str:                                # Export to JSON file
        json_str = self.to_json()
        with open(filepath, 'w') as f:
            f.write(json_str)
        return filepath

    # ═══════════════════════════════════════════════════════════════════════════════
    # Summary Export (Type_Safe Schema)
    # ═══════════════════════════════════════════════════════════════════════════════

    def to_export_summary(self) -> Schema__Export_Summary:                       # Compact summary as Type_Safe schema
        analysis = Timestamp_Collector__Analysis(collector=self.collector)
        hotspots = analysis.get_hotspots(top_n=10)
        total_ns = self.collector.total_duration_ns()

        hotspot_schemas = [
            Schema__Export_Hotspot(
                name       = mt.name,
                self_ms    = round(method_timing__self_ms(mt), 2),
                percentage = round((mt.self_ns / total_ns * 100) if total_ns > 0 else 0, 1),
                calls      = mt.call_count,
            )
            for mt in hotspots
        ]

        return Schema__Export_Summary(
            name              = self.collector.name,
            total_duration_ms = round(self.collector.total_duration_ms(), 2),
            method_count      = self.collector.method_count(),
            entry_count       = self.collector.entry_count(),
            hotspots          = hotspot_schemas,
        )

    def to_summary_json(self, indent: int = 2) -> str:                           # Export summary as JSON
        return self.to_export_summary().json()

    # ═══════════════════════════════════════════════════════════════════════════════
    # Speedscope Format (Type_Safe Schema)
    # ═══════════════════════════════════════════════════════════════════════════════

    def to_speedscope(self) -> Schema__Speedscope:                               # Export in speedscope.app format
        """
        Generates speedscope format for visualization at https://speedscope.app
        Uses the 'evented' profile type for accurate timing.
        """
        frames_dict = {}                                                         # name -> frame_index
        frame_list  = []
        events      = []

        for entry in self.collector.entries:
            if entry.name not in frames_dict:
                frames_dict[entry.name] = len(frame_list)
                frame_list.append(Schema__Speedscope_Frame(name=entry.name))

            frame_idx = frames_dict[entry.name]
            # Convert to microseconds from start
            at_us = (entry.timestamp_ns - self.collector.start_time_ns) / 1000

            events.append(Schema__Speedscope_Event(
                type  = 'O' if entry.event == 'enter' else 'C',                  # O=Open, C=Close
                frame = frame_idx,
                at    = at_us
            ))

        profile = Schema__Speedscope_Profile(
            type       = 'evented',
            name       = self.collector.name,
            unit       = 'microseconds',
            startValue = 0,
            endValue   = self.collector.total_duration_ns() / 1000,
            events     = events
        )

        shared = Schema__Speedscope_Shared(frames=frame_list)

        return Schema__Speedscope(
            shared             = shared,
            profiles           = [profile],
            name               = self.collector.name,
            activeProfileIndex = 0
        )

    def to_speedscope_json(self) -> str:                                         # Export speedscope format as JSON
        json_data = self.to_speedscope().json()
        json_data['$schema'] = json_data.pop('schema')                           # Speedscope requires '$schema' key
        return json_to_str(json_data)


    def to_speedscope_file(self, filepath: str) -> str:                          # Export to speedscope JSON file
        json_str = self.to_speedscope_json()
        with open(filepath, 'w') as f:
            f.write(json_str)
        return filepath
