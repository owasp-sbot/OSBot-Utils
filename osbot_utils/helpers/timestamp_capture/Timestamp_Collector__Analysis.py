"""
Timestamp Collector Analysis
=============================

Analyzes collected timestamps to compute method timings and hotspots.
"""

from typing                                                                import List, Dict
from osbot_utils.helpers.timestamp_capture.schemas.Schema__Method_Timing   import Schema__Method_Timing
from osbot_utils.type_safe.Type_Safe                                       import Type_Safe
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector             import Timestamp_Collector


class Timestamp_Collector__Analysis(Type_Safe):

    collector: Timestamp_Collector = None

    def get_method_timings(self) -> Dict[str, Schema__Method_Timing]:           # Calculate per-method timing with self-time
        timings  : Dict[str, Schema__Method_Timing] = {}
        stack    : List[tuple]                      = []                        # (entry_index, entry)
        children : Dict[int, int]                   = {}                        # entry_index -> child_time_ns

        for i, entry in enumerate(self.collector.entries):
            if entry.event == 'enter':
                stack.append((i, entry))
                children[i] = 0

            elif entry.event == 'exit' and stack:
                for j in range(len(stack) - 1, -1, -1):                         # Find matching enter (reverse search)
                    enter_idx, enter_entry = stack[j]
                    if enter_entry.name == entry.name:
                        stack.pop(j)

                        duration_ns = entry.timestamp_ns - enter_entry.timestamp_ns
                        child_time  = children.pop(enter_idx, 0)
                        self_time   = duration_ns - child_time

                        if stack:                                               # Add child time to parent
                            parent_idx = stack[-1][0]
                            children[parent_idx] = children.get(parent_idx, 0) + duration_ns

                        if entry.name not in timings:                           # Update timing stats
                            timings[entry.name] = Schema__Method_Timing(name   = entry.name  ,
                                                                        min_ns = duration_ns ,
                                                                        max_ns = duration_ns )

                        mt             = timings[entry.name]
                        mt.call_count += 1
                        mt.total_ns   += duration_ns
                        mt.self_ns    += self_time
                        mt.min_ns      = min(mt.min_ns, duration_ns)
                        mt.max_ns      = max(mt.max_ns, duration_ns)
                        break

        return timings

    def get_hotspots(self, top_n: int = 10) -> List[Schema__Method_Timing]:     # Get top N methods by self-time
        timings = self.get_method_timings()
        return sorted(timings.values(), key=lambda t: t.self_ns, reverse=True)[:top_n]

    def get_timings_by_total(self) -> List[Schema__Method_Timing]:              # Get all timings sorted by total time
        timings = self.get_method_timings()
        return sorted(timings.values(), key=lambda t: t.total_ns, reverse=True)

    def get_timings_by_call_count(self) -> List[Schema__Method_Timing]:         # Get all timings sorted by call count
        timings = self.get_method_timings()
        return sorted(timings.values(), key=lambda t: t.call_count, reverse=True)