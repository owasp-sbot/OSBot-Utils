"""
Timestamp Collector Report
===========================

Formats and prints timing reports from collected timestamps.
"""

from osbot_utils.helpers.timestamp_capture.actions.Timestamp_Collector__Analysis import Timestamp_Collector__Analysis
from osbot_utils.helpers.timestamp_capture.static_methods.timestamp_utils        import method_timing__total_ms, method_timing__self_ms, method_timing__avg_ms
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector                   import Timestamp_Collector


class Timestamp_Collector__Report(Type_Safe):

    collector: Timestamp_Collector = None

    MIN_METHOD_WIDTH = 40                                                        # Minimum width for method column
    MAX_METHOD_WIDTH = 80                                                        # Maximum width to prevent excessive stretching

    def _calculate_method_width(self, names: list) -> int:                       # Calculate optimal column width
        if not names:
            return self.MIN_METHOD_WIDTH
        max_name_len = max(len(name) for name in names)
        return min(max(max_name_len + 2, self.MIN_METHOD_WIDTH), self.MAX_METHOD_WIDTH)

    def _calculate_total_width(self, method_width: int) -> int:                  # Calculate total line width
        return method_width + 50                                                 # method + calls + total + self + avg + %

    def format_report(self, show_self_time: bool = True) -> str:                 # Format comprehensive timing report
        analysis = Timestamp_Collector__Analysis(collector=self.collector)
        timings  = analysis.get_method_timings()

        method_names  = list(timings.keys()) if timings else []
        method_width  = self._calculate_method_width(method_names)
        total_width   = self._calculate_total_width(method_width)

        lines = []
        lines.append("=" * total_width)
        lines.append(f"Timestamp Report: {self.collector.name}")
        lines.append("=" * total_width)
        lines.append("")

        total_ms = self.collector.total_duration_ms()
        lines.append(f"  Total Duration : {total_ms:,.2f} ms")
        lines.append(f"  Entry Count    : {self.collector.entry_count():,}")
        lines.append(f"  Methods Traced : {self.collector.method_count()}")
        lines.append("")

        if timings:
            lines.append("Method Timings (sorted by total time):")
            lines.append("-" * total_width)

            if show_self_time:
                header = f"{'Method':<{method_width}} {'Calls':>6} {'Total':>10} {'Self':>10} {'Avg':>9} {'%Total':>7}"
            else:
                header = f"{'Method':<{method_width}} {'Calls':>6} {'Total(ms)':>10} {'Avg(ms)':>10} {'%Total':>7}"

            lines.append(header)
            lines.append("-" * total_width)

            sorted_timings = analysis.get_timings_by_total()
            total_ns       = self.collector.total_duration_ns()

            for mt in sorted_timings:
                pct = (mt.total_ns / total_ns * 100) if total_ns > 0 else 0

                if show_self_time:
                    lines.append(
                        f"{mt.name:<{method_width}} {mt.call_count:>6} "
                        f"{method_timing__total_ms(mt):>9.2f}ms {method_timing__self_ms(mt):>9.2f}ms "
                        f"{method_timing__avg_ms(mt):>8.3f}ms {pct:>6.1f}%"
                    )
                else:
                    lines.append(
                        f"{mt.name:<{method_width}} {mt.call_count:>6} "
                        f"{method_timing__total_ms(mt):>10.2f} {method_timing__avg_ms(mt):>10.3f} {pct:>6.1f}%"
                    )

        lines.append("")
        lines.append("=" * total_width)
        return "\n".join(lines)

    def format_timeline(self, max_entries: int = 100) -> str:                    # Format timeline view
        entries = self.collector.entries[:max_entries]

        # Calculate width based on deepest indent + longest name
        if entries:
            max_indent    = max(entry.depth for entry in entries) * 2
            max_name_len  = max(len(entry.name) for entry in entries)
            content_width = 12 + max_indent + 2 + max_name_len                   # timestamp + indent + marker + name
            total_width   = max(80, content_width + 2)
        else:
            total_width = 80

        lines = []
        lines.append("=" * total_width)
        lines.append("Execution Timeline")
        lines.append("=" * total_width)

        if len(self.collector.entries) > max_entries:
            lines.append(f"(showing first {max_entries} of {len(self.collector.entries)} entries)")

        for entry in entries:
            offset_ms = (entry.timestamp_ns - self.collector.start_time_ns) / 1_000_000
            indent    = "  " * entry.depth
            marker    = "▶" if entry.event == 'enter' else "◀"
            lines.append(f"{offset_ms:>10.3f}ms {indent}{marker} {entry.name}")

        lines.append("=" * total_width)
        return "\n".join(lines)

    def format_hotspots(self, top_n: int = 10) -> str:                           # Format hotspot analysis (by self-time)
        analysis = Timestamp_Collector__Analysis(collector=self.collector)
        hotspots = analysis.get_hotspots(top_n)
        total_ns = self.collector.total_duration_ns()

        # Calculate width based on longest method name
        if hotspots:
            method_names = [mt.name for mt in hotspots]
            method_width = self._calculate_method_width(method_names)
        else:
            method_width = self.MIN_METHOD_WIDTH

        total_width = method_width + 40                                          # method + rank + timing + percentage + calls

        lines = []
        lines.append("=" * total_width)
        lines.append(f"Top {top_n} Hotspots (by self-time)")
        lines.append("=" * total_width)

        for i, mt in enumerate(hotspots, 1):
            pct = (mt.self_ns / total_ns * 100) if total_ns > 0 else 0
            lines.append(
                f"  {i:>2}. {mt.name:<{method_width}} "
                f"{method_timing__self_ms(mt):>8.2f}ms ({pct:>5.1f}%) "
                f"[{mt.call_count} calls]"
            )

        lines.append("=" * total_width)
        return "\n".join(lines)

    def print_report(self, show_self_time: bool = True):
        print(self.format_report(show_self_time))

    def print_timeline(self, max_entries: int = 100):
        print(self.format_timeline(max_entries))

    def print_hotspots(self, top_n: int = 10):
        print(self.format_hotspots(top_n))

    def print_all(self):
        self.print_report()
        self.print_hotspots()
        self.print_timeline()
