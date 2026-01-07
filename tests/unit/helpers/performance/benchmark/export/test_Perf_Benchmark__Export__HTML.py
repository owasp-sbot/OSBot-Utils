# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Benchmark__Export__HTML - Tests for HTML + Chart.js exporter
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Comparison      import Schema__Perf__Benchmark__Comparison
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Evolution       import Schema__Perf__Benchmark__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Comparison__Two            import Schema__Perf__Comparison__Two
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.helpers.performance.benchmark.export.Perf_Benchmark__Export                              import Perf_Benchmark__Export
from osbot_utils.helpers.performance.benchmark.export.Perf_Benchmark__Export__HTML import Perf_Benchmark__Export__HTML, CHART_COLORS
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Evolution                            import Schema__Perf__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Statistics                           import Schema__Perf__Statistics
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Benchmark_Comparisons            import List__Benchmark_Comparisons
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Benchmark_Evolutions             import List__Benchmark_Evolutions
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Titles                           import List__Titles
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Scores                           import List__Scores
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Comparison__Status                     import Enum__Comparison__Status
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Benchmark__Trend                       import Enum__Benchmark__Trend


class test_Perf_Benchmark__Export__HTML(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Shared test data
        cls.exporter = Perf_Benchmark__Export__HTML()

        # Create sample comparison - improvement
        cls.comparison = Schema__Perf__Benchmark__Comparison(benchmark_id   = 'A_01__test'                          ,
                                                             name           = 'test_benchmark'                      ,
                                                             score_a        = Safe_UInt(1000)                       ,
                                                             score_b        = Safe_UInt(800)                        ,
                                                             change_percent = Safe_Float(20.0)                      ,
                                                             trend          = Enum__Benchmark__Trend.IMPROVEMENT    )

        # Create sample comparison - regression
        cls.comparison_regression = Schema__Perf__Benchmark__Comparison(benchmark_id   = 'A_02__test'               ,
                                                                        name           = 'test_regression'          ,
                                                                        score_a        = Safe_UInt(500)             ,
                                                                        score_b        = Safe_UInt(600)             ,
                                                                        change_percent = Safe_Float(-20.0)          ,
                                                                        trend          = Enum__Benchmark__Trend.REGRESSION)

        # Create comparisons list
        cls.comparisons = List__Benchmark_Comparisons()
        cls.comparisons.append(cls.comparison)
        cls.comparisons.append(cls.comparison_regression)

        # Create sample evolution
        scores = List__Scores()
        scores.append(Safe_UInt(1000))
        scores.append(Safe_UInt(900))
        scores.append(Safe_UInt(800))

        cls.evolution = Schema__Perf__Benchmark__Evolution(benchmark_id   = 'A_01__test'                       ,
                                                           name           = 'test_benchmark'                   ,
                                                           scores         = scores                             ,
                                                           first_score    = Safe_UInt(1000)                    ,
                                                           last_score     = Safe_UInt(800)                     ,
                                                           change_percent = Safe_Float(20.0)                   ,
                                                           trend          = Enum__Benchmark__Trend.IMPROVEMENT )

        cls.evolutions = List__Benchmark_Evolutions()
        cls.evolutions.append(cls.evolution)

        cls.titles = List__Titles()
        cls.titles.append('Session 1')
        cls.titles.append('Session 2')
        cls.titles.append('Session 3')


    def test__init__(self):                                                      # Test initialization
        with Perf_Benchmark__Export__HTML() as _:
            assert type(_)              is Perf_Benchmark__Export__HTML
            assert isinstance(_, Type_Safe)
            assert type(CHART_COLORS) is list
            assert len(CHART_COLORS)  == 6

    def test_inheritance(self):                                                  # Test inheritance
        assert issubclass(Perf_Benchmark__Export__HTML, Perf_Benchmark__Export)
        assert issubclass(Perf_Benchmark__Export__HTML, Type_Safe)

    def test_chart_colors(self):                                                 # Test colors defined
        with self.exporter as _:
            assert 'rgba(54, 162, 235, 0.8)' in CHART_COLORS
            assert 'rgba(255, 99, 132, 0.8)' in CHART_COLORS


    # ═══════════════════════════════════════════════════════════════════════════════
    # html_wrapper Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_html_wrapper(self):                                                 # Test HTML wrapper
        with self.exporter as _:
            html = _.html_wrapper('Test Title', '<p>Test Body</p>')

            assert '<!DOCTYPE html>' in html
            assert '<html>'          in html
            assert '</html>'         in html
            assert '<title>Test Title</title>' in html
            assert '<p>Test Body</p>' in html
            assert 'chart.js'        in html
            assert '<style>'         in html

    def test_html_wrapper__css_included(self):                                   # Test CSS styles
        with self.exporter as _:
            html = _.html_wrapper('Title', '<p>Body</p>')

            assert '.improvement'    in html
            assert '.regression'     in html
            assert '.unchanged'      in html
            assert 'font-family'     in html


    # ═══════════════════════════════════════════════════════════════════════════════
    # trend_class Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_trend_class__strong_improvement(self):                              # Test CSS class
        with self.exporter as _:
            css_class = _.trend_class(Enum__Benchmark__Trend.STRONG_IMPROVEMENT)
            assert css_class == 'improvement'

    def test_trend_class__improvement(self):                                     # Test CSS class
        with self.exporter as _:
            css_class = _.trend_class(Enum__Benchmark__Trend.IMPROVEMENT)
            assert css_class == 'improvement'

    def test_trend_class__unchanged(self):                                       # Test CSS class
        with self.exporter as _:
            css_class = _.trend_class(Enum__Benchmark__Trend.UNCHANGED)
            assert css_class == 'unchanged'

    def test_trend_class__regression(self):                                      # Test CSS class
        with self.exporter as _:
            css_class = _.trend_class(Enum__Benchmark__Trend.REGRESSION)
            assert css_class == 'regression'

    def test_trend_class__strong_regression(self):                               # Test CSS class
        with self.exporter as _:
            css_class = _.trend_class(Enum__Benchmark__Trend.STRONG_REGRESSION)
            assert css_class == 'regression'


    # ═══════════════════════════════════════════════════════════════════════════════
    # export_comparison Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_export_comparison(self):                                            # Test comparison export
        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Before'                        ,
                                               title_b     = 'After'                         ,
                                               comparisons = self.comparisons                )

        with self.exporter as _:
            html = _.export_comparison(result)

            assert type(html)        is str
            assert '<html>'          in html
            assert '<table>'         in html
            assert 'Comparison'      in html
            assert 'Before'          in html
            assert 'After'           in html
            assert 'test_benchmark'  in html
            assert '1,000 ns'        in html

    def test_export_comparison__improvement_class(self):                         # Test improvement CSS
        comparisons = List__Benchmark_Comparisons()
        comparisons.append(self.comparison)

        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Before'                        ,
                                               title_b     = 'After'                         ,
                                               comparisons = comparisons                     )

        with self.exporter as _:
            html = _.export_comparison(result)

            assert 'class="improvement"' in html
            assert '-20.0%'              in html

    def test_export_comparison__regression_class(self):                          # Test regression CSS
        comparisons = List__Benchmark_Comparisons()
        comparisons.append(self.comparison_regression)

        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Before'                        ,
                                               title_b     = 'After'                         ,
                                               comparisons = comparisons                     )

        with self.exporter as _:
            html = _.export_comparison(result)

            assert 'class="regression"' in html
            assert '+20.0%'             in html

    def test_export_comparison__table_structure(self):                           # Test table structure
        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Session A'                     ,
                                               title_b     = 'Session B'                     ,
                                               comparisons = self.comparisons                )

        with self.exporter as _:
            html = _.export_comparison(result)

            assert '<th>Benchmark</th>' in html
            assert '<th>Session A</th>' in html
            assert '<th>Session B</th>' in html
            assert '<th>Change</th>'    in html
            assert '<tr>'               in html
            assert '<td>'               in html

    def test_export_comparison__error_status(self):                              # Test error status
        result = Schema__Perf__Comparison__Two(status = Enum__Comparison__Status.ERROR_NO_SESSIONS,
                                               error  = 'No sessions loaded'                      )

        with self.exporter as _:
            html = _.export_comparison(result)

            assert '<html>'          in html
            assert 'No sessions'     in html


    # ═══════════════════════════════════════════════════════════════════════════════
    # export_evolution Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_export_evolution(self):                                             # Test evolution export
        result = Schema__Perf__Evolution(status        = Enum__Comparison__Status.SUCCESS,
                                         session_count = Safe_UInt(3)                    ,
                                         titles        = self.titles                     ,
                                         evolutions    = self.evolutions                 )

        with self.exporter as _:
            html = _.export_evolution(result)

            assert type(html)        is str
            assert '<html>'          in html
            assert 'chart.js'        in html
            assert 'evolutionChart'  in html
            assert '3 Sessions'      in html
            assert 'test_benchmark'  in html

    def test_export_evolution__chart_data(self):                                 # Test Chart.js data
        result = Schema__Perf__Evolution(status        = Enum__Comparison__Status.SUCCESS,
                                         session_count = Safe_UInt(3)                    ,
                                         titles        = self.titles                     ,
                                         evolutions    = self.evolutions                 )

        with self.exporter as _:
            html = _.export_evolution(result)

            assert 'new Chart'       in html
            assert 'type: \'line\''  in html
            assert 'datasets'        in html
            assert 'labels'          in html
            assert 'Session 1'       in html
            assert 'Session 2'       in html

    def test_export_evolution__canvas(self):                                     # Test canvas element
        result = Schema__Perf__Evolution(status        = Enum__Comparison__Status.SUCCESS,
                                         session_count = Safe_UInt(3)                    ,
                                         titles        = self.titles                     ,
                                         evolutions    = self.evolutions                 )

        with self.exporter as _:
            html = _.export_evolution(result)

            assert '<canvas id="evolutionChart">' in html
            assert 'chart-container'              in html

    def test_export_evolution__error_status(self):                               # Test error status
        result = Schema__Perf__Evolution(status = Enum__Comparison__Status.ERROR_NO_SESSIONS,
                                         error  = 'No sessions loaded'                      )

        with self.exporter as _:
            html = _.export_evolution(result)

            assert '<html>'      in html
            assert 'No sessions' in html


    # ═══════════════════════════════════════════════════════════════════════════════
    # export_statistics Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_export_statistics(self):                                            # Test statistics export
        result = Schema__Perf__Statistics(status            = Enum__Comparison__Status.SUCCESS,
                                          session_count     = Safe_UInt(3)                    ,
                                          benchmark_count   = Safe_UInt(10)                   ,
                                          improvement_count = Safe_UInt(5)                    ,
                                          regression_count  = Safe_UInt(2)                    ,
                                          avg_improvement   = Safe_Float(15.5)                ,
                                          avg_regression    = Safe_Float(8.2)                 )

        with self.exporter as _:
            html = _.export_statistics(result)

            assert type(html)             is str
            assert '<html>'               in html
            assert 'Statistics'           in html
            assert 'Sessions compared'    in html
            assert 'Benchmarks tracked'   in html
            assert 'class="improvement"'  in html
            assert 'class="regression"'   in html

    def test_export_statistics__with_best_improvement(self):                     # Test best improvement
        result = Schema__Perf__Statistics(status            = Enum__Comparison__Status.SUCCESS,
                                          session_count     = Safe_UInt(3)                    ,
                                          benchmark_count   = Safe_UInt(5)                    ,
                                          improvement_count = Safe_UInt(3)                    ,
                                          regression_count  = Safe_UInt(0)                    ,
                                          avg_improvement   = Safe_Float(20.0)                ,
                                          avg_regression    = Safe_Float(0.0)                 ,
                                          best_improvement  = self.comparison                 )

        with self.exporter as _:
            html = _.export_statistics(result)

            assert 'Best:'          in html
            assert 'test_benchmark' in html

    def test_export_statistics__no_changes(self):                                # Test no changes
        result = Schema__Perf__Statistics(status            = Enum__Comparison__Status.SUCCESS,
                                          session_count     = Safe_UInt(3)                    ,
                                          benchmark_count   = Safe_UInt(5)                    ,
                                          improvement_count = Safe_UInt(0)                    ,
                                          regression_count  = Safe_UInt(0)                    ,
                                          avg_improvement   = Safe_Float(0.0)                 ,
                                          avg_regression    = Safe_Float(0.0)                 )

        with self.exporter as _:
            html = _.export_statistics(result)

            assert 'No significant changes' in html
            assert 'class="unchanged"'      in html

    def test_export_statistics__error_status(self):                              # Test error status
        result = Schema__Perf__Statistics(status = Enum__Comparison__Status.ERROR_NO_SESSIONS,
                                          error  = 'No sessions loaded'                      )

        with self.exporter as _:
            html = _.export_statistics(result)

            assert '<html>'      in html
            assert 'No sessions' in html
