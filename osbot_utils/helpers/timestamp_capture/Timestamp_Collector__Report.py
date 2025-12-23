"""
Timestamp Collector Report
===========================

Formats and prints timing reports from collected timestamps.
"""
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector import Timestamp_Collector
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector__Analysis         import Timestamp_Collector__Analysis
from osbot_utils.helpers.timestamp_capture.static_methods.timestamp_utils        import method_timing__total_ms, method_timing__self_ms, method_timing__avg_ms
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe


class Timestamp_Collector__Report(Type_Safe):

    collector: Timestamp_Collector = None

    def format_report(self, show_self_time: bool = True) -> str:                # Format comprehensive timing report
        lines = []
        lines.append("=" * 100)
        lines.append(f"Timestamp Report: {self.collector.name}")
        lines.append("=" * 100)
        lines.append("")

        total_ms = self.collector.total_duration_ms()
        lines.append(f"  Total Duration : {total_ms:,.2f} ms")
        lines.append(f"  Entry Count    : {self.collector.entry_count():,}")
        lines.append(f"  Methods Traced : {self.collector.method_count()}")
        lines.append("")

        analysis = Timestamp_Collector__Analysis(collector=self.collector)
        timings  = analysis.get_method_timings()

        if timings:
            lines.append("Method Timings (sorted by total time):")
            lines.append("-" * 100)

            if show_self_time:
                header = f"{'Method':<50} {'Calls':>6} {'Total':>10} {'Self':>10} {'Avg':>8} {'%Total':>7}"
            else:
                header = f"{'Method':<50} {'Calls':>6} {'Total(ms)':>10} {'Avg(ms)':>10} {'%Total':>7}"

            lines.append(header)
            lines.append("-" * 100)

            sorted_timings = analysis.get_timings_by_total()
            total_ns       = self.collector.total_duration_ns()

            for mt in sorted_timings:
                pct = (mt.total_ns / total_ns * 100) if total_ns > 0 else 0

                if show_self_time:
                    lines.append(
                        f"{mt.name:<50} {mt.call_count:>6} "
                        f"{method_timing__total_ms(mt):>9.2f}ms {method_timing__self_ms(mt):>9.2f}ms "
                        f"{method_timing__avg_ms(mt):>7.3f}ms {pct:>6.1f}%"
                    )
                else:
                    lines.append(
                        f"{mt.name:<50} {mt.call_count:>6} "
                        f"{method_timing__total_ms(mt):>10.2f} {method_timing__avg_ms(mt):>10.3f} {pct:>6.1f}%"
                    )

        lines.append("")
        lines.append("=" * 100)
        return "\n".join(lines)

    def format_timeline(self, max_entries: int = 100) -> str:                   # Format timeline view
        lines = []
        lines.append("=" * 80)
        lines.append("Execution Timeline")
        lines.append("=" * 80)

        entries = self.collector.entries[:max_entries]
        if len(self.collector.entries) > max_entries:
            lines.append(f"(showing first {max_entries} of {len(self.collector.entries)} entries)")

        for entry in entries:
            offset_ms = (entry.timestamp_ns - self.collector.start_time_ns) / 1_000_000
            indent    = "  " * entry.depth
            marker    = "▶" if entry.event == 'enter' else "◀"
            lines.append(f"{offset_ms:>10.3f}ms {indent}{marker} {entry.name}")

        lines.append("=" * 80)
        return "\n".join(lines)

    def format_hotspots(self, top_n: int = 10) -> str:                          # Format hotspot analysis (by self-time)
        lines = []
        lines.append("=" * 80)
        lines.append(f"Top {top_n} Hotspots (by self-time)")
        lines.append("=" * 80)

        analysis = Timestamp_Collector__Analysis(collector=self.collector)
        hotspots = analysis.get_hotspots(top_n)
        total_ns = self.collector.total_duration_ns()

        for i, mt in enumerate(hotspots, 1):
            pct = (mt.self_ns / total_ns * 100) if total_ns > 0 else 0
            lines.append(
                f"  {i:>2}. {mt.name:<45} "
                f"{method_timing__self_ms(mt):>8.2f}ms ({pct:>5.1f}%) "
                f"[{mt.call_count} calls]"
            )

        lines.append("=" * 80)
        return "\n".join(lines)

    def print_all(self):
        self.print_report  ()
        self.print_timeline()
        self.print_hotspots()

    def print_report(self, show_self_time: bool = True):
        print(self.format_report(show_self_time))

    def print_timeline(self, max_entries: int = 100):
        print(self.format_timeline(max_entries))

    def print_hotspots(self, top_n: int = 10):
        print(self.format_hotspots(top_n))