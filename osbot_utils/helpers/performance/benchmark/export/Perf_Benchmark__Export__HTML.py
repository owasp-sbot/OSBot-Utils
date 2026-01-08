# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Benchmark__Export__HTML - HTML + Chart.js export format
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.performance.benchmark.export.Perf_Benchmark__Export                    import Perf_Benchmark__Export
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Evolution                  import Schema__Perf__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Statistics                 import Schema__Perf__Statistics
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Comparison__Two  import Schema__Perf__Comparison__Two
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Comparison__Status           import Enum__Comparison__Status
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Benchmark__Trend             import Enum__Benchmark__Trend

CHART_COLORS : list = ['rgba(54, 162, 235, 0.8)' ,
                       'rgba(255, 99, 132, 0.8)' ,
                       'rgba(75, 192, 192, 0.8)' ,
                       'rgba(255, 206, 86, 0.8)' ,
                       'rgba(153, 102, 255, 0.8)',
                       'rgba(255, 159, 64, 0.8)' ]


class Perf_Benchmark__Export__HTML(Perf_Benchmark__Export):                      # HTML exporter



    # ═══════════════════════════════════════════════════════════════════════════════
    # HTML Templates
    # ═══════════════════════════════════════════════════════════════════════════════

    def html_wrapper(self, title: str, body: str) -> str:                        # Wrap content in HTML
        return f'''<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 20px; }}
        .chart-container {{ max-width: 1000px; margin: 20px auto; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .improvement {{ color: green; }}
        .regression {{ color: red; }}
        .unchanged {{ color: gray; }}
    </style>
</head>
<body>
{body}
</body>
</html>'''

    def trend_class(self, trend: Enum__Benchmark__Trend) -> str:                 # CSS class for trend
        if trend in [Enum__Benchmark__Trend.STRONG_IMPROVEMENT, Enum__Benchmark__Trend.IMPROVEMENT]:
            return 'improvement'
        if trend in [Enum__Benchmark__Trend.STRONG_REGRESSION, Enum__Benchmark__Trend.REGRESSION]:
            return 'regression'
        return 'unchanged'


    # ═══════════════════════════════════════════════════════════════════════════════
    # Export Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def export_comparison(self, result: Schema__Perf__Comparison__Two) -> str:   # Export comparison
        if result.status != Enum__Comparison__Status.SUCCESS:
            return self.html_wrapper('Error', f'<p>{result.error}</p>')

        rows = []
        for comparison in result.comparisons:
            change_pct = comparison.change_percent
            css_class  = self.trend_class(comparison.trend)

            if change_pct > 0:
                change_str = f'-{change_pct:.1f}%'
            elif change_pct < 0:
                change_str = f'+{abs(change_pct):.1f}%'
            else:
                change_str = '0%'

            rows.append(f'''        <tr>
            <td>{comparison.name}</td>
            <td>{comparison.score_a:,} ns</td>
            <td>{comparison.score_b:,} ns</td>
            <td class="{css_class}">{change_str}</td>
        </tr>''')

        body = f'''    <h1>Comparison: {result.title_a} vs {result.title_b}</h1>
    <table>
        <tr>
            <th>Benchmark</th>
            <th>{result.title_a}</th>
            <th>{result.title_b}</th>
            <th>Change</th>
        </tr>
{chr(10).join(rows)}
    </table>'''

        return self.html_wrapper('Benchmark Comparison', body)

    def export_evolution(self, result: Schema__Perf__Evolution) -> str:          # Export evolution
        if result.status != Enum__Comparison__Status.SUCCESS:
            return self.html_wrapper('Error', f'<p>{result.error}</p>')

        labels   = [title for title in result.titles]
        datasets = []

        for i, evolution in enumerate(result.evolutions):
            color      = CHART_COLORS[i % len(CHART_COLORS)]
            bg_color   = color.replace('0.8', '0.2')
            scores     = [int(s) for s in evolution.scores]

            datasets.append(f'''{{
                label: '{evolution.name}',
                data: {scores},
                borderColor: '{color}',
                backgroundColor: '{bg_color}',
                tension: 0.1
            }}''')

        chart_data = f'''
const ctx = document.getElementById('evolutionChart').getContext('2d');
new Chart(ctx, {{
    type: 'line',
    data: {{
        labels: {labels},
        datasets: [{', '.join(datasets)}]
    }},
    options: {{
        responsive: true,
        plugins: {{
            title: {{ display: true, text: 'Performance Evolution' }}
        }},
        scales: {{
            y: {{
                beginAtZero: true,
                title: {{ display: true, text: 'Nanoseconds' }}
            }}
        }}
    }}
}});'''

        body = f'''    <h1>Performance Evolution: {result.session_count} Sessions</h1>
    <div class="chart-container">
        <canvas id="evolutionChart"></canvas>
    </div>
    <script>
        {chart_data}
    </script>'''

        return self.html_wrapper('Performance Evolution', body)

    def export_statistics(self, result: Schema__Perf__Statistics) -> str:        # Export statistics
        if result.status != Enum__Comparison__Status.SUCCESS:
            return self.html_wrapper('Error', f'<p>{result.error}</p>')

        lines = [f'<p><strong>Sessions compared:</strong> {result.session_count}</p>',
                 f'<p><strong>Benchmarks tracked:</strong> {result.benchmark_count}</p>']

        if result.improvement_count > 0:
            lines.append(f'<p class="improvement"><strong>Improvements:</strong> {result.improvement_count} benchmarks (avg {result.avg_improvement:.1f}%)</p>')
            if result.best_improvement is not None:
                lines.append(f'<p class="improvement">Best: {result.best_improvement.name} (-{result.best_improvement.change_percent:.1f}%)</p>')

        if result.regression_count > 0:
            lines.append(f'<p class="regression"><strong>Regressions:</strong> {result.regression_count} benchmarks (avg +{result.avg_regression:.1f}%)</p>')
            if result.worst_regression is not None:
                lines.append(f'<p class="regression">Worst: {result.worst_regression.name} (+{abs(result.worst_regression.change_percent):.1f}%)</p>')

        if result.improvement_count == 0 and result.regression_count == 0:
            lines.append('<p class="unchanged">No significant changes detected</p>')

        body = f'''    <h1>Performance Statistics</h1>
{chr(10).join(lines)}'''

        return self.html_wrapper('Performance Statistics', body)
