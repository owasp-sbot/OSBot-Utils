# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Benchmark__Export__Text - Tests for text/Print_Table exporter
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Comparison      import Schema__Perf__Benchmark__Comparison
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Evolution       import Schema__Perf__Benchmark__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Comparison__Two            import Schema__Perf__Comparison__Two
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.helpers.performance.benchmark.export.Perf_Benchmark__Export                              import Perf_Benchmark__Export
from osbot_utils.helpers.performance.benchmark.export.Perf_Benchmark__Export__Text                        import Perf_Benchmark__Export__Text
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Evolution                            import Schema__Perf__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Statistics                           import Schema__Perf__Statistics
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Benchmark_Comparisons            import List__Benchmark_Comparisons
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Benchmark_Evolutions             import List__Benchmark_Evolutions
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Titles                           import List__Titles
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Scores                           import List__Scores
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Comparison__Status                     import Enum__Comparison__Status
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Benchmark__Trend                       import Enum__Benchmark__Trend


class test_Perf_Benchmark__Export__Text(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Shared test data
        cls.exporter = Perf_Benchmark__Export__Text()

        # Create sample comparison
        cls.comparison = Schema__Perf__Benchmark__Comparison(benchmark_id   = 'A_01__test'                          ,
                                                             name           = 'test_benchmark'                      ,
                                                             score_a        = Safe_UInt(1000)                       ,
                                                             score_b        = Safe_UInt(800)                        ,
                                                             change_percent = Safe_Float(20.0)                      ,
                                                             trend          = Enum__Benchmark__Trend.IMPROVEMENT    )

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
        with Perf_Benchmark__Export__Text() as _:
            assert type(_)         is Perf_Benchmark__Export__Text
            assert isinstance(_, Type_Safe)

    def test_inheritance(self):                                                  # Test inheritance
        assert issubclass(Perf_Benchmark__Export__Text, Perf_Benchmark__Export)
        assert issubclass(Perf_Benchmark__Export__Text, Type_Safe)


    # ═══════════════════════════════════════════════════════════════════════════════
    # trend_symbol Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_trend_symbol__strong_improvement(self):                             # Test strong improvement
        with self.exporter as _:
            symbol = _.trend_symbol(Enum__Benchmark__Trend.STRONG_IMPROVEMENT)
            assert symbol == '▼▼▼'

    def test_trend_symbol__improvement(self):                                    # Test improvement
        with self.exporter as _:
            symbol = _.trend_symbol(Enum__Benchmark__Trend.IMPROVEMENT)
            assert symbol == '▼'

    def test_trend_symbol__unchanged(self):                                      # Test unchanged
        with self.exporter as _:
            symbol = _.trend_symbol(Enum__Benchmark__Trend.UNCHANGED)
            assert symbol == '─'

    def test_trend_symbol__regression(self):                                     # Test regression
        with self.exporter as _:
            symbol = _.trend_symbol(Enum__Benchmark__Trend.REGRESSION)
            assert symbol == '▲'

    def test_trend_symbol__strong_regression(self):                              # Test strong regression
        with self.exporter as _:
            symbol = _.trend_symbol(Enum__Benchmark__Trend.STRONG_REGRESSION)
            assert symbol == '▲▲▲'


    # ═══════════════════════════════════════════════════════════════════════════════
    # export_comparison Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_export_comparison(self):                                            # Test comparison export
        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Before'                        ,
                                               title_b     = 'After'                         ,
                                               comparisons = self.comparisons                )

        with self.exporter as _:
            text = _.export_comparison(result)

            assert type(text)       is str
            assert 'Comparison'     in text
            assert 'Before'         in text
            assert 'After'          in text
            assert 'test_benchmark' in text
            assert '1,000 ns'       in text
            assert '800 ns'         in text

    def test_export_comparison__with_improvement(self):                          # Test improvement display
        comparisons = List__Benchmark_Comparisons()
        comparisons.append(self.comparison)

        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Before'                        ,
                                               title_b     = 'After'                         ,
                                               comparisons = comparisons                     )

        with self.exporter as _:
            text = _.export_comparison(result)

            assert '-20.0%' in text                                              # Improvement shown as negative
            assert '▼'      in text

    def test_export_comparison__with_regression(self):                           # Test regression display
        comparisons = List__Benchmark_Comparisons()
        comparisons.append(self.comparison_regression)

        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Before'                        ,
                                               title_b     = 'After'                         ,
                                               comparisons = comparisons                     )

        with self.exporter as _:
            text = _.export_comparison(result)

            assert '+20.0%' in text                                              # Regression shown as positive
            assert '▲'      in text

    def test_export_comparison__error_status(self):                              # Test error status
        result = Schema__Perf__Comparison__Two(status = Enum__Comparison__Status.ERROR_NO_SESSIONS,
                                               error  = 'No sessions loaded'                      )

        with self.exporter as _:
            text = _.export_comparison(result)

            assert text == 'No sessions loaded'


    # ═══════════════════════════════════════════════════════════════════════════════
    # export_evolution Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_export_evolution(self):                                             # Test evolution export
        result = Schema__Perf__Evolution(status        = Enum__Comparison__Status.SUCCESS,
                                         session_count = Safe_UInt(3)                    ,
                                         titles        = self.titles                     ,
                                         evolutions    = self.evolutions                 )

        with self.exporter as _:
            text = _.export_evolution(result)

            assert type(text)       is str
            assert 'Evolution'      in text
            assert '3 sessions'     in text
            assert 'test_benchmark' in text
            assert '1,000 ns'       in text
            assert '800 ns'         in text

    def test_export_evolution__truncated_titles(self):                           # Test title truncation
        titles = List__Titles()
        titles.append('Very Long Session Title That Exceeds Limit')
        titles.append('Another Long Title')

        result = Schema__Perf__Evolution(status        = Enum__Comparison__Status.SUCCESS,
                                         session_count = Safe_UInt(2)                    ,
                                         titles        = titles                          ,
                                         evolutions    = self.evolutions                 )

        with self.exporter as _:
            text = _.export_evolution(result)

            assert 'Very Long Sessi' in text                                     # Truncated to 15 chars

    def test_export_evolution__error_status(self):                               # Test error status
        result = Schema__Perf__Evolution(status = Enum__Comparison__Status.ERROR_INSUFFICIENT_SESSIONS,
                                         error  = 'Need at least 2 sessions'                          )

        with self.exporter as _:
            text = _.export_evolution(result)

            assert text == 'Need at least 2 sessions'


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
            text = _.export_statistics(result)

            assert type(text)          is str
            assert 'Statistics'        in text
            assert 'Sessions compared' in text
            assert '3'                 in text
            assert '10'                in text
            assert 'Improvements'      in text
            assert '5 benchmarks'      in text
            assert '15.5%'             in text

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
            text = _.export_statistics(result)

            assert 'Best:'          in text
            assert 'test_benchmark' in text
            assert '-20.0%'         in text

    def test_export_statistics__with_worst_regression(self):                     # Test worst regression
        result = Schema__Perf__Statistics(status            = Enum__Comparison__Status.SUCCESS,
                                          session_count     = Safe_UInt(3)                    ,
                                          benchmark_count   = Safe_UInt(5)                    ,
                                          improvement_count = Safe_UInt(0)                    ,
                                          regression_count  = Safe_UInt(2)                    ,
                                          avg_improvement   = Safe_Float(0.0)                 ,
                                          avg_regression    = Safe_Float(15.0)                ,
                                          worst_regression  = self.comparison_regression      )

        with self.exporter as _:
            text = _.export_statistics(result)

            assert 'Worst:'          in text
            assert 'test_regression' in text
            assert '+20.0%'          in text

    def test_export_statistics__no_changes(self):                                # Test no changes
        result = Schema__Perf__Statistics(status            = Enum__Comparison__Status.SUCCESS,
                                          session_count     = Safe_UInt(3)                    ,
                                          benchmark_count   = Safe_UInt(5)                    ,
                                          improvement_count = Safe_UInt(0)                    ,
                                          regression_count  = Safe_UInt(0)                    ,
                                          avg_improvement   = Safe_Float(0.0)                 ,
                                          avg_regression    = Safe_Float(0.0)                 )

        with self.exporter as _:
            text = _.export_statistics(result)

            assert 'No significant changes' in text

    def test_export_statistics__error_status(self):                              # Test error status
        result = Schema__Perf__Statistics(status = Enum__Comparison__Status.ERROR_NO_SESSIONS,
                                          error  = 'No sessions loaded'                      )

        with self.exporter as _:
            text = _.export_statistics(result)

            assert text == 'No sessions loaded'
