# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Report__Renderer__Base - Abstract base for report renderers
# Provides shared formatting helpers for time and percentage values
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report import Schema__Perf_Report
from osbot_utils.type_safe.type_safe_core.decorators.type_safe          import type_safe
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe


class Perf_Report__Renderer__Base(Type_Safe):                       # Abstract base for renderers

    @type_safe
    def render(self, report: Schema__Perf_Report) -> str:           # Render report to string
        raise NotImplementedError()

    # ═══════════════════════════════════════════════════════════════════════════
    # Formatting Helpers
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def format_ns(self, ns: int) -> str:                            # Format nanoseconds to human-readable
        if ns < 1_000:
            return f'{ns}ns'
        elif ns < 1_000_000:
            return f'{ns / 1_000:.2f}µs'
        elif ns < 1_000_000_000:
            return f'{ns / 1_000_000:.2f}ms'
        else:
            return f'{ns / 1_000_000_000:.2f}s'

    @type_safe
    def format_pct(self, pct: float, width: int = 5) -> str:        # Format percentage with padding
        return f'{pct:>{width}.1f}%'

    @type_safe
    def format_timestamp(self, timestamp_ms: int) -> str:           # Format timestamp to readable date
        from datetime import datetime, timezone
        dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @type_safe
    def escape_markdown(self, text: str) -> str:                    # Escape special markdown characters
        special_chars = ['|', '`', '*', '_', '[', ']', '<', '>']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text
