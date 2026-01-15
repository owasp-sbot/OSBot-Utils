# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Report__Renderer__Markdown - Markdown format renderer
# Creates formatted markdown tables and headers for documentation
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                          import List
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Base                    import Perf_Report__Renderer__Base
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report                              import Schema__Perf_Report
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Builder__Config             import Schema__Perf_Report__Builder__Config
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                       import type_safe


class Perf_Report__Renderer__Markdown(Perf_Report__Renderer__Base): # Markdown format renderer
    config: Schema__Perf_Report__Builder__Config                    # Optional config for conditional sections

    @type_safe
    def render(self, report: Schema__Perf_Report) -> str:           # Render report to markdown
        lines = []
        lines.extend(self.render_header(report))
        lines.extend(self.render_metadata(report))
        lines.extend(self.render_legend(report))
        lines.extend(self.render_benchmarks(report))
        lines.extend(self.render_categories(report))
        lines.extend(self.render_analysis(report))
        return '\n'.join(lines)

    # ═══════════════════════════════════════════════════════════════════════════
    # Section Renderers
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def render_header(self, report: Schema__Perf_Report) -> List[str]:
        title = str(report.metadata.title)
        return [f'# {title}'                                        ,
                ''                                                  ]

    @type_safe
    def render_metadata(self, report: Schema__Perf_Report) -> List[str]:
        m     = report.metadata
        lines = ['## Metadata'                                                      ,
                 ''                                                                 ,
                 '| Property | Value |'                                             ,
                 '|----------|-------|'                                             ]

        rows = [('Date'        , self.format_timestamp(int(m.timestamp)))           ,
                ('Version'     , self.escape_markdown(str(m.version))   )           ,
                ('Description' , self.escape_markdown(str(m.description)))          ,
                ('Test Input'  , self.escape_markdown(str(m.test_input)))           ,
                ('Mode'        , str(m.measure_mode.name)               )           ,
                ('Benchmarks'  , str(int(m.benchmark_count))            )           ]

        for label, value in rows:
            lines.append(f'| {label} | {value} |')

        lines.append('')
        return lines

    @type_safe
    def render_legend(self, report: Schema__Perf_Report) -> List[str]:

        lines = ['## Legend'                                                        ,
                 ''                                                                 ]

        for cat_id, description in report.legend.items():
            desc_escaped = self.escape_markdown(str(description))
            lines.append(f'- **{cat_id}**: {desc_escaped}')

        lines.append('')
        return lines

    @type_safe
    def render_benchmarks(self, report: Schema__Perf_Report) -> List[str]:
        lines = ['## Individual Benchmarks'                                         ,
                 ''                                                                 ,
                 '| Benchmark | Time | Percentage |'                                ,
                 '|-----------|------|------------|'                                ]

        for benchmark in report.benchmarks:
            bench_id = self.escape_markdown(str(benchmark.benchmark_id))
            time_str = self.format_ns(int(benchmark.time_ns))
            pct_str  = self.format_pct(float(benchmark.pct_of_total))
            lines.append(f'| {bench_id} | {time_str} | {pct_str} |')

        lines.append('')
        return lines

    @type_safe
    def render_categories(self, report: Schema__Perf_Report) -> List[str]:
        lines = ['## Category Totals'                                               ,
                 ''                                                                 ,
                 '| Category | Time | Percentage | Benchmarks |'                    ,
                 '|----------|------|------------|------------|'                    ]

        for category in report.categories:
            name     = self.escape_markdown(str(category.name))
            time_str = self.format_ns(int(category.total_ns))
            pct_str  = self.format_pct(float(category.pct_of_total))
            count    = int(category.benchmark_count)
            lines.append(f'| {name} | {time_str} | {pct_str} | {count} |')

        lines.append('')
        return lines

    @type_safe
    def render_analysis(self, report: Schema__Perf_Report) -> List[str]:
        a     = report.analysis
        lines = ['## Analysis'                                                      ,
                 ''                                                                 ,
                 '| Metric | Value |'                                               ,
                 '|--------|-------|'                                               ]

        bottleneck_id  = self.escape_markdown(str(a.bottleneck_id))
        bottleneck_ns  = self.format_ns(int(a.bottleneck_ns))
        bottleneck_pct = self.format_pct(float(a.bottleneck_pct))

        lines.append(f'| Bottleneck | {bottleneck_id} |')
        lines.append(f'| Bottleneck Time | {bottleneck_ns} ({bottleneck_pct}) |')
        lines.append(f'| Total Time | {self.format_ns(int(a.total_ns))} |')
        lines.append(f'| Overhead | {self.format_ns(abs(int(a.overhead_ns)))} ({self.format_pct(float(a.overhead_pct))}) |')

        lines.append('')

        if a.key_insight and self.config and self.config.include_auto_insight:
            insight_escaped = self.escape_markdown(str(a.key_insight))
            lines.append('## Key Insight'                                           )
            lines.append(''                                                         )
            lines.append(f'> {insight_escaped}'                                     )
            lines.append(''                                                         )

        return lines
