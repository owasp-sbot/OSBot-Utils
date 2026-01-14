# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Report__Renderer__Text - Plain text format renderer
# Creates formatted tables with visual bars for terminal/file output
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                          import List
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Base                    import Perf_Report__Renderer__Base
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report                              import Schema__Perf_Report
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Builder__Config             import Schema__Perf_Report__Builder__Config
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                       import type_safe


class Perf_Report__Renderer__Text(Perf_Report__Renderer__Base):     # Plain text format renderer
    config: Schema__Perf_Report__Builder__Config                    # Optional config for conditional sections

    @type_safe
    def render(self, report: Schema__Perf_Report) -> str:           # Render report to plain text
        lines = []
        lines.extend(self.render_header(report))
        lines.extend(self.render_metadata(report))
        lines.extend(self.render_legend(report))
        lines.extend(self.render_benchmarks(report))
        lines.extend(self.render_categories(report))
        lines.extend(self.render_stage_breakdown(report))
        lines.extend(self.render_percentage_analysis(report))
        lines.extend(self.render_analysis(report))
        return '\n'.join(lines)

    # ═══════════════════════════════════════════════════════════════════════════
    # Section Renderers
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def render_header(self, report: Schema__Perf_Report) -> List[str]:
        title = report.metadata.title.upper()
        border = '═' * 80
        return [border                           ,
                title.center(80)                 ,
                border                           ,
                ''                               ]

    @type_safe
    def render_metadata(self, report: Schema__Perf_Report) -> List[str]:
        m = report.metadata
        lines = ['┌' + '─' * 78 + '┐'                                               ,
                 '│ BENCHMARK METADATA' + ' ' * 59 + '│'                            ,
                 '├' + '─' * 78 + '┤'                                               ]

        rows = [('Date'        , self.format_timestamp(int(m.timestamp)))           ,
                ('Version'     , str(m.version)                         )           ,
                ('Description' , str(m.description)                     )           ,
                ('Test Input'  , str(m.test_input)                      )           ,
                ('Mode'        , str(m.measure_mode.name)               )           ,
                ('Benchmarks'  , str(int(m.benchmark_count))            )           ]

        for label, value in rows:
            value_truncated = value[:55] if len(value) > 55 else value
            lines.append(f'│ {label:<15}│ {value_truncated:<60} │')

        lines.append('└' + '─' * 78 + '┘')
        lines.append('')
        return lines

    @type_safe
    def render_legend(self, report: Schema__Perf_Report) -> List[str]:
        if not report.legend:
            return []

        lines = ['LEGEND'                                                           ,
                 '=' * 60                                                           ]

        for cat_id, description in report.legend.items():
            lines.append(f'  {cat_id} = {description}')

        lines.append('')
        return lines

    @type_safe
    def render_benchmarks(self, report: Schema__Perf_Report) -> List[str]:
        lines = ['INDIVIDUAL BENCHMARKS'                                            ,
                 '=' * 60                                                           ]

        for benchmark in report.benchmarks:
            time_str = self.format_ns(int(benchmark.time_ns))
            pct_str  = self.format_pct(float(benchmark.pct_of_total))
            lines.append(f'  {benchmark.benchmark_id:<40} {time_str:>10} ({pct_str})')

        lines.append('')
        return lines

    @type_safe
    def render_categories(self, report: Schema__Perf_Report) -> List[str]:
        lines = ['CATEGORY TOTALS'                                                  ,
                 '=' * 60                                                           ]

        for category in report.categories:
            time_str = self.format_ns(int(category.total_ns))
            pct_str  = self.format_pct(float(category.pct_of_total))
            count    = int(category.benchmark_count)
            lines.append(f'  {category.name:<30} {time_str:>10} ({pct_str}) [{count} benchmarks]')

        lines.append('')
        return lines

    @type_safe
    def render_stage_breakdown(self, report: Schema__Perf_Report) -> List[str]:
        if self.config and self.config.include_stage_breakdown is False:
            return []

        lines = ['STAGE BREAKDOWN'                                                  ,
                 '=' * 60                                                           ]

        max_pct = max((c.pct_of_total for c in report.categories), default=100)

        for category in report.categories:
            time_str  = self.format_ns(int(category.total_ns))
            pct       = float(category.pct_of_total)
            pct_str   = self.format_pct(pct)
            bar_width = int((pct / max(max_pct, 1)) * 50) if max_pct > 0 else 0
            bar       = '█' * bar_width
            lines.append(f'  {category.name:<20} {time_str:>10} ({pct_str}) {bar}')

        lines.append('')
        return lines

    @type_safe
    def render_percentage_analysis(self, report: Schema__Perf_Report) -> List[str]:
        if self.config and self.config.include_percentage_analysis is False:
            return []

        full_cat_id    = self.config.full_category_id    if self.config else 'A'
        create_cat_id  = self.config.create_category_id  if self.config else 'B'
        convert_cat_id = self.config.convert_category_id if self.config else 'C'

        full_total = 0
        cat_totals = {}

        for category in report.categories:
            cat_id = category.category_id
            cat_totals[cat_id] = category.total_ns
            if cat_id == full_cat_id:
                full_total = category.total_ns

        if full_total == 0:
            return []

        lines = [f'PERCENTAGE ANALYSIS (relative to {full_cat_id})'                 ,
                 '=' * 60                                                           ]

        for cat_id in [create_cat_id, convert_cat_id]:
            if cat_id in cat_totals:
                cat_ns  = cat_totals[cat_id]
                pct     = (cat_ns / full_total) * 100 if full_total > 0 else 0
                pct_str = self.format_pct(pct)
                lines.append(f'  {cat_id} / {full_cat_id} = {pct_str}')

        lines.append('')
        return lines

    @type_safe
    def render_analysis(self, report: Schema__Perf_Report) -> List[str]:
        a     = report.analysis
        lines = ['ANALYSIS'                                                         ,
                 '=' * 60                                                           ]

        lines.append(f'  Bottleneck: {a.bottleneck_id}')
        lines.append(f'    Time:     {self.format_ns(int(a.bottleneck_ns))} ({self.format_pct(float(a.bottleneck_pct))})')
        lines.append(f'  Total:      {self.format_ns(int(a.total_ns))}')
        lines.append(f'  Overhead:   {self.format_ns(abs(int(a.overhead_ns)))} ({self.format_pct(float(a.overhead_pct))})')

        if a.key_insight and self.config and self.config.include_auto_insight:
            lines.append('')
            lines.append(f'  Key Insight: {a.key_insight}')

        lines.append('')
        return lines
