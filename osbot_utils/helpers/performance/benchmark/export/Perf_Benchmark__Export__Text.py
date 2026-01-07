# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Benchmark__Export__Text - Text/Print_Table export format
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.Print_Table                                                            import Print_Table
from osbot_utils.helpers.performance.benchmark.export.Perf_Benchmark__Export                    import Perf_Benchmark__Export
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Evolution                  import Schema__Perf__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Statistics                 import Schema__Perf__Statistics
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Comparison__Two  import Schema__Perf__Comparison__Two
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Comparison__Status           import Enum__Comparison__Status
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Benchmark__Trend             import Enum__Benchmark__Trend


class Perf_Benchmark__Export__Text(Perf_Benchmark__Export):                      # Text exporter


    # ═══════════════════════════════════════════════════════════════════════════════
    # Trend Symbols
    # ═══════════════════════════════════════════════════════════════════════════════

    def trend_symbol(self, trend: Enum__Benchmark__Trend) -> str:                # Convert trend to symbol
        symbols = {Enum__Benchmark__Trend.STRONG_IMPROVEMENT : '▼▼▼',
                   Enum__Benchmark__Trend.IMPROVEMENT        : '▼'  ,
                   Enum__Benchmark__Trend.UNCHANGED          : '─'  ,
                   Enum__Benchmark__Trend.REGRESSION         : '▲'  ,
                   Enum__Benchmark__Trend.STRONG_REGRESSION  : '▲▲▲'}
        return symbols.get(trend, '?')


    # ═══════════════════════════════════════════════════════════════════════════════
    # Export Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def export_comparison(self, result: Schema__Perf__Comparison__Two) -> str:   # Export comparison
        if result.status != Enum__Comparison__Status.SUCCESS:
            return result.error

        table = Print_Table()
        table.set_title(f'Comparison: {result.title_a} vs {result.title_b}')
        table.add_headers('Benchmark', result.title_a, result.title_b, 'Change')

        for comparison in result.comparisons:
            change_pct = comparison.change_percent
            symbol     = self.trend_symbol(comparison.trend)

            if change_pct > 0:
                change_str = f'-{change_pct:.1f}% {symbol}'
            elif change_pct < 0:
                change_str = f'+{abs(change_pct):.1f}% {symbol}'
            else:
                change_str = f'0% {symbol}'

            table.add_row([comparison.name                ,
                           f'{comparison.score_a:,} ns'   ,
                           f'{comparison.score_b:,} ns'   ,
                           change_str                     ])

        table.map_texts()
        return '\n'.join(table.text__all)

    def export_evolution(self, result: Schema__Perf__Evolution) -> str:          # Export evolution
        if result.status != Enum__Comparison__Status.SUCCESS:
            return result.error

        table = Print_Table()
        table.set_title(f'Performance Evolution: {result.session_count} sessions')

        headers = ['Benchmark']
        for title in result.titles:
            headers.append(title[:15])                                           # Truncate for table width
        headers.append('Trend')
        table.add_headers(*headers)

        for evolution in result.evolutions:
            row    = [evolution.name]
            for score in evolution.scores:
                if score > 0:
                    row.append(f'{score:,} ns')
                else:
                    row.append('-')

            change_pct = evolution.change_percent
            symbol     = self.trend_symbol(evolution.trend)

            if change_pct > 0:
                trend_str = f'{symbol} -{change_pct:.0f}%'
            elif change_pct < 0:
                trend_str = f'{symbol} +{abs(change_pct):.0f}%'
            else:
                trend_str = symbol

            row.append(trend_str)
            table.add_row(row)

        table.map_texts()
        return '\n'.join(table.text__all)

    def export_statistics(self, result: Schema__Perf__Statistics) -> str:        # Export statistics
        if result.status != Enum__Comparison__Status.SUCCESS:
            return result.error

        lines = ['# Performance Statistics', '']
        lines.append(f'Sessions compared: {result.session_count}')
        lines.append(f'Benchmarks tracked: {result.benchmark_count}')
        lines.append('')

        if result.improvement_count > 0:
            lines.append(f'Improvements: {result.improvement_count} benchmarks (avg {result.avg_improvement:.1f}%)')
            if result.best_improvement is not None:
                lines.append(f'  Best: {result.best_improvement.name} (-{result.best_improvement.change_percent:.1f}%)')

        if result.regression_count > 0:
            lines.append(f'Regressions: {result.regression_count} benchmarks (avg +{result.avg_regression:.1f}%)')
            if result.worst_regression is not None:
                lines.append(f'  Worst: {result.worst_regression.name} (+{abs(result.worst_regression.change_percent):.1f}%)')

        if result.improvement_count == 0 and result.regression_count == 0:
            lines.append('No significant changes detected')

        return '\n'.join(lines)
