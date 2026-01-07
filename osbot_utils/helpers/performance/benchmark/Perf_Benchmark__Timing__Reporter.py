# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Benchmark__Timing__Reporter - Report generation for benchmark results
# Generates text, JSON, markdown, and HTML outputs using Print_Table
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.Print_Table                                                                      import Print_Table
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Result          import Schema__Perf__Benchmark__Result
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Markdown                          import Safe_Str__Markdown
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                              import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Time_Formatted                    import Safe_Str__Time_Formatted
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path                         import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Html                                 import Safe_Str__Html
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Javascript                           import Safe_Str__Javascript
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                            import type_safe
from osbot_utils.utils.Files                                                                              import file_create, folder_create
from osbot_utils.utils.Json                                                                               import json_dumps, json_load_file
from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config      import Schema__Perf_Benchmark__Timing__Config
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results                import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark__Legend                import Dict__Benchmark__Legend
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Time_Unit                              import Enum__Time_Unit
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section              import Safe_Str__Benchmark__Section
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title                import Safe_Str__Benchmark__Title


class Perf_Benchmark__Timing__Reporter(Type_Safe):                               # Report generator
    results : Dict__Benchmark_Results                                            # Benchmark results
    config  : Schema__Perf_Benchmark__Timing__Config                                     # Configuration


    # ═══════════════════════════════════════════════════════════════════════════════
    # Output Generation Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def build_text(self) -> Safe_Str__Text:                                      # Formatted text output
        table = self.create_results_table()
        table.map_texts()
        return '\n'.join(table.text__all)

    @type_safe
    def build_json(self) -> dict:                                                # Dict for JSON serialization
        sections = self.detect_sections()
        return {'title'           : self.config.title                                             ,
                'description'     : self.config.description                                       ,
                'total_benchmarks': len(self.results)                                             ,
                'sections'        : {k: v for k, v in sections.items()}                           ,
                'results'         : {k: v.json() for k, v in self.results.items()}                }

    @type_safe
    def build_markdown(self) -> Safe_Str__Markdown:                              # Markdown tables
        lines    = []
        title    = self.config.title
        sections = self.detect_sections()

        lines.append(f'# {title}')
        lines.append('')

        current_section = None
        for benchmark_id in sorted(self.results.keys()):
            result  = self.results[benchmark_id]
            section = result.section

            if section != current_section:
                if current_section is not None:
                    lines.append('')
                section_desc = sections.get(Safe_Str__Benchmark__Section(section), Safe_Str__Benchmark__Title(section))
                lines.append(f'## Section {section}: {section_desc}')
                lines.append('')
                lines.append('| ID | Benchmark | Score | Raw |')
                lines.append('|----|-----------|-------|-----|')
                current_section = section

            score_str = self.format_time(result.final_score)
            raw_str   = self.format_time(result.raw_score)
            lines.append(f'| {result.section}_{result.index} | {result.name} | {score_str} | {raw_str} |')

        lines.append('')
        lines.append(f'**Total: {len(self.results)} benchmarks**')

        return '\n'.join(lines)

    @type_safe
    def build_html(self) -> Safe_Str__Html:                                      # HTML with Chart.js
        title      = self.config.title
        chart_data = self.create_chart_js_data()
        table_html = self.create_html_table()

        html = f'''<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 20px; }}
        .chart-container {{ max-width: 900px; margin: 20px auto; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f4f4f4; }}
        tr:nth-child(even) {{ background-color: #fafafa; }}
        .footer {{ margin-top: 20px; color: #666; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="chart-container">
        <canvas id="benchmarkChart"></canvas>
    </div>
    {table_html}
    <p class="footer">Total: {len(self.results)} benchmarks</p>
    <script>
        {chart_data}
    </script>
</body>
</html>'''
        return html


    # ═══════════════════════════════════════════════════════════════════════════════
    # File Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def save_all(self) -> None:                                                  # Save all formats
        if not self.config.output_path:
            return

        output_path = self.config.output_path
        prefix      = self.config.output_prefix or 'benchmark'

        folder_create(output_path)

        self.save_text    (f'{output_path}/{prefix}.txt' )
        self.save_json    (f'{output_path}/{prefix}.json')
        self.save_markdown(f'{output_path}/{prefix}.md'  )
        self.save_html    (f'{output_path}/{prefix}.html')

    @type_safe
    def save_text(self, filepath: Safe_Str__File__Path) -> None:                 # Save text file
        content = self.build_text()
        file_create(filepath, content)

    @type_safe
    def save_json(self, filepath: Safe_Str__File__Path) -> None:                 # Save JSON file
        content = self.build_json()
        file_create(filepath, json_dumps(content, indent=2))

    @type_safe
    def save_markdown(self, filepath: Safe_Str__File__Path) -> None:             # Save markdown file
        content = self.build_markdown()
        file_create(filepath, content)

    @type_safe
    def save_html(self, filepath: Safe_Str__File__Path) -> None:                 # Save HTML file
        content = self.build_html()
        file_create(filepath, content)


    # ═══════════════════════════════════════════════════════════════════════════════
    # Comparison Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def compare(self, other: 'Perf_Benchmark__Timing__Reporter') -> Safe_Str__Text:
        return self.compare_results(other.results)

    @type_safe
    def compare_from_json(self, filepath: Safe_Str__File__Path) -> Safe_Str__Text:
        data = json_load_file(filepath)
        if data is None:
            return ''

        other_results = Dict__Benchmark_Results()

        for benchmark_id, result_data in data.get('results', {}).items():
            result = Schema__Perf__Benchmark__Result.from_json(result_data)
            other_results[benchmark_id] = result

        return self.compare_results(other_results)

    @type_safe
    def compare_results(self                            ,                        # Compare with another results dict
                        other: Dict__Benchmark_Results  ) -> Safe_Str__Text:
        table = Print_Table()
        table.set_title('Comparison: Before vs After')
        table.add_headers('Benchmark', 'Before', 'After', 'Change')

        for benchmark_id in sorted(self.results.keys()):
            if benchmark_id not in other:
                continue

            before = other[benchmark_id]
            after  = self.results[benchmark_id]

            before_score = int(before.final_score)
            after_score  = int(after.final_score)

            if before_score > 0:
                change_pct = ((before_score - after_score) / before_score) * 100
                if change_pct > 0:
                    change_str = f'-{change_pct:.1f}% ▼'
                elif change_pct < 0:
                    change_str = f'+{abs(change_pct):.1f}% ▲'
                else:
                    change_str = '0%'
            else:
                change_str = 'N/A'

            table.add_row([after.name                                           ,
                           self.format_time(before.final_score)                 ,
                           self.format_time(after.final_score)                  ,
                           change_str                                           ])

        table.map_texts()
        return '\n'.join(table.text__all)


    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def detect_sections(self) -> Dict__Benchmark__Legend:                        # Auto-detect sections
        sections = Dict__Benchmark__Legend()

        if self.config.legend and len(self.config.legend) > 0:
            return self.config.legend

        for benchmark_id in self.results.keys():
            result  = self.results[benchmark_id]
            section = result.section
            if section not in sections:
                sections[section] = Safe_Str__Benchmark__Title(section)

        return sections

    @type_safe
    def print_summary(self) -> None:                                             # Print to console
        table = self.create_results_table()
        table.print()

    @type_safe
    def format_time(self, ns_value: Safe_UInt) -> Safe_Str__Time_Formatted:      # Format time with unit
        value = int(ns_value)
        unit  = self.config.time_unit

        if unit == Enum__Time_Unit.NANOSECONDS:
            return f'{value:,} ns'
        elif unit == Enum__Time_Unit.MICROSECONDS:
            return f'{value / 1_000:,.3f} µs'
        elif unit == Enum__Time_Unit.MILLISECONDS:
            return f'{value / 1_000_000:,.3f} ms'
        elif unit == Enum__Time_Unit.SECONDS:
            return f'{value / 1_000_000_000:,.6f} s'
        return f'{value:,} ns'

    @type_safe
    def create_results_table(self) -> Print_Table:                               # Create Print_Table
        table = Print_Table()
        table.set_title(self.config.title)
        table.add_headers('ID', 'Benchmark', 'Score', 'Raw')

        current_section = None

        for benchmark_id in sorted(self.results.keys()):
            result  = self.results[benchmark_id]
            section = result.section

            if section != current_section:
                if current_section is not None:
                    table.add_row(['─' * 6, '─' * 30, '─' * 12, '─' * 12])
                current_section = section

            score_str = self.format_time(result.final_score)
            raw_str   = self.format_time(result.raw_score)

            table.add_row([f'{result.section}_{result.index}'                   ,
                           result.name                                          ,
                           score_str                                            ,
                           raw_str                                              ])

        table.set_footer(f'Total: {len(self.results)} benchmarks')
        return table

    @type_safe
    def create_html_table(self) -> Safe_Str__Html:                               # Create HTML table
        lines = ['<table>', '<tr><th>ID</th><th>Benchmark</th><th>Score</th><th>Raw</th></tr>']

        for benchmark_id in sorted(self.results.keys()):
            result    = self.results[benchmark_id]
            score_str = self.format_time(result.final_score)
            raw_str   = self.format_time(result.raw_score)
            lines.append(f'<tr><td>{result.section}_{result.index}</td>'
                         f'<td>{result.name}</td>'
                         f'<td>{score_str}</td>'
                         f'<td>{raw_str}</td></tr>')

        lines.append('</table>')
        return '\n'.join(lines)

    @type_safe
    def create_chart_js_data(self) -> Safe_Str__Javascript:                      # Create Chart.js script
        labels = []
        scores = []

        for benchmark_id in sorted(self.results.keys()):
            result = self.results[benchmark_id]
            labels.append(result.name)
            scores.append(int(result.final_score))

        return f'''
const ctx = document.getElementById('benchmarkChart').getContext('2d');
new Chart(ctx, {{
    type: 'bar',
    data: {{
        labels: {labels},
        datasets: [{{
            label: 'Score (ns)',
            data: {scores},
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }}]
    }},
    options: {{
        responsive: true,
        scales: {{
            y: {{
                beginAtZero: true,
                title: {{ display: true, text: 'Nanoseconds' }}
            }}
        }}
    }}
}});'''