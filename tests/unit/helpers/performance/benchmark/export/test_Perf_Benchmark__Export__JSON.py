# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Benchmark__Export__JSON - Tests for JSON exporter
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Comparison      import Schema__Perf__Benchmark__Comparison
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Evolution       import Schema__Perf__Benchmark__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Comparison__Two            import Schema__Perf__Comparison__Two
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.utils.Json                                                                               import json_loads
from osbot_utils.helpers.performance.benchmark.export.Perf_Benchmark__Export                              import Perf_Benchmark__Export
from osbot_utils.helpers.performance.benchmark.export.Perf_Benchmark__Export__JSON                        import Perf_Benchmark__Export__JSON
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Evolution                            import Schema__Perf__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Statistics                           import Schema__Perf__Statistics
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Benchmark_Comparisons            import List__Benchmark_Comparisons
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Benchmark_Evolutions             import List__Benchmark_Evolutions
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Titles                           import List__Titles
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Scores                           import List__Scores
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Comparison__Status                     import Enum__Comparison__Status
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Benchmark__Trend                       import Enum__Benchmark__Trend


class test_Perf_Benchmark__Export__JSON(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Shared test data
        cls.exporter = Perf_Benchmark__Export__JSON()

        # Create sample comparison
        cls.comparison = Schema__Perf__Benchmark__Comparison(benchmark_id   = 'A_01__test'                          ,
                                                             name           = 'test_benchmark'                      ,
                                                             score_a        = Safe_UInt(1000)                       ,
                                                             score_b        = Safe_UInt(800)                        ,
                                                             change_percent = Safe_Float(20.0)                      ,
                                                             trend          = Enum__Benchmark__Trend.IMPROVEMENT    )

        # Create comparisons list
        cls.comparisons = List__Benchmark_Comparisons()
        cls.comparisons.append(cls.comparison)

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
        with Perf_Benchmark__Export__JSON() as _:
            assert type(_)         is Perf_Benchmark__Export__JSON
            assert isinstance(_, Type_Safe)

    def test_inheritance(self):                                                  # Test inheritance
        assert issubclass(Perf_Benchmark__Export__JSON, Perf_Benchmark__Export)
        assert issubclass(Perf_Benchmark__Export__JSON, Type_Safe)


    # ═══════════════════════════════════════════════════════════════════════════════
    # export_comparison Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_export_comparison(self):                                            # Test comparison export
        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Before'                        ,
                                               title_b     = 'After'                         ,
                                               comparisons = self.comparisons                )

        with self.exporter as _:
            json_str = _.export_comparison(result)

            assert type(json_str) is str

    def test_export_comparison__valid_json(self):                                # Test valid JSON
        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Before'                        ,
                                               title_b     = 'After'                         ,
                                               comparisons = self.comparisons                )

        with self.exporter as _:
            json_str = _.export_comparison(result)
            data     = json_loads(json_str)                                      # Should not raise

            assert type(data) is dict

    def test_export_comparison__contains_fields(self):                           # Test required fields
        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Before'                        ,
                                               title_b     = 'After'                         ,
                                               comparisons = self.comparisons                )

        with self.exporter as _:
            json_str = _.export_comparison(result)
            data     = json_loads(json_str)

            assert 'status'       in data
            assert 'title_a'      in data
            assert 'title_b'      in data
            assert 'comparisons'  in data
            assert 'timestamp'    in data

    def test_export_comparison__status_value(self):                              # Test status serialization
        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Before'                        ,
                                               title_b     = 'After'                         ,
                                               comparisons = self.comparisons                )

        with self.exporter as _:
            json_str = _.export_comparison(result)
            data     = json_loads(json_str)

            assert data['status'] == 'success'

    def test_export_comparison__comparisons_list(self):                          # Test comparisons array
        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Before'                        ,
                                               title_b     = 'After'                         ,
                                               comparisons = self.comparisons                )

        with self.exporter as _:
            json_str = _.export_comparison(result)
            data     = json_loads(json_str)

            assert type(data['comparisons']) is list
            assert len(data['comparisons'])  == 1

            comparison = data['comparisons'][0]
            assert comparison['benchmark_id']   == 'A_01__test'
            assert comparison['name']           == 'test_benchmark'
            assert comparison['score_a']        == 1000
            assert comparison['score_b']        == 800
            assert comparison['change_percent'] == 20.0
            assert comparison['trend']          == 'improvement'

    def test_export_comparison__error_status(self):                              # Test error status
        result = Schema__Perf__Comparison__Two(status = Enum__Comparison__Status.ERROR_NO_SESSIONS,
                                               error  = 'No sessions loaded'                      )

        with self.exporter as _:
            json_str = _.export_comparison(result)
            data     = json_loads(json_str)

            assert data['status'] == 'no_sessions'
            assert data['error']  == 'No sessions loaded'


    # ═══════════════════════════════════════════════════════════════════════════════
    # export_evolution Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_export_evolution(self):                                             # Test evolution export
        result = Schema__Perf__Evolution(status        = Enum__Comparison__Status.SUCCESS,
                                         session_count = Safe_UInt(3)                    ,
                                         titles        = self.titles                     ,
                                         evolutions    = self.evolutions                 )

        with self.exporter as _:
            json_str = _.export_evolution(result)

            assert type(json_str) is str

    def test_export_evolution__valid_json(self):                                 # Test valid JSON
        result = Schema__Perf__Evolution(status        = Enum__Comparison__Status.SUCCESS,
                                         session_count = Safe_UInt(3)                    ,
                                         titles        = self.titles                     ,
                                         evolutions    = self.evolutions                 )

        with self.exporter as _:
            json_str = _.export_evolution(result)
            data     = json_loads(json_str)

            assert type(data) is dict

    def test_export_evolution__contains_fields(self):                            # Test required fields
        result = Schema__Perf__Evolution(status        = Enum__Comparison__Status.SUCCESS,
                                         session_count = Safe_UInt(3)                    ,
                                         titles        = self.titles                     ,
                                         evolutions    = self.evolutions                 )

        with self.exporter as _:
            json_str = _.export_evolution(result)
            data     = json_loads(json_str)

            assert 'status'         in data
            assert 'session_count'  in data
            assert 'titles'         in data
            assert 'evolutions'     in data
            assert 'timestamp'      in data

    def test_export_evolution__titles_list(self):                                # Test titles array
        result = Schema__Perf__Evolution(status        = Enum__Comparison__Status.SUCCESS,
                                         session_count = Safe_UInt(3)                    ,
                                         titles        = self.titles                     ,
                                         evolutions    = self.evolutions                 )

        with self.exporter as _:
            json_str = _.export_evolution(result)
            data     = json_loads(json_str)

            assert type(data['titles']) is list
            assert len(data['titles'])  == 3
            assert data['titles'][0]    == 'Session 1'
            assert data['titles'][1]    == 'Session 2'
            assert data['titles'][2]    == 'Session 3'

    def test_export_evolution__evolutions_list(self):                            # Test evolutions array
        result = Schema__Perf__Evolution(status        = Enum__Comparison__Status.SUCCESS,
                                         session_count = Safe_UInt(3)                    ,
                                         titles        = self.titles                     ,
                                         evolutions    = self.evolutions                 )

        with self.exporter as _:
            json_str = _.export_evolution(result)
            data     = json_loads(json_str)

            assert type(data['evolutions']) is list
            assert len(data['evolutions'])  == 1

            evolution = data['evolutions'][0]
            assert evolution['benchmark_id']   == 'A_01__test'
            assert evolution['name']           == 'test_benchmark'
            assert evolution['scores']         == [1000, 900, 800]
            assert evolution['first_score']    == 1000
            assert evolution['last_score']     == 800
            assert evolution['change_percent'] == 20.0
            assert evolution['trend']          == 'improvement'

    def test_export_evolution__error_status(self):                               # Test error status
        result = Schema__Perf__Evolution(status = Enum__Comparison__Status.ERROR_INSUFFICIENT_SESSIONS,
                                         error  = 'Need at least 2 sessions'                          )

        with self.exporter as _:
            json_str = _.export_evolution(result)
            data     = json_loads(json_str)

            assert data['status'] == 'insufficient_sessions'
            assert data['error']  == 'Need at least 2 sessions'


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
            json_str = _.export_statistics(result)

            assert type(json_str) is str

    def test_export_statistics__valid_json(self):                                # Test valid JSON
        result = Schema__Perf__Statistics(status            = Enum__Comparison__Status.SUCCESS,
                                          session_count     = Safe_UInt(3)                    ,
                                          benchmark_count   = Safe_UInt(10)                   ,
                                          improvement_count = Safe_UInt(5)                    ,
                                          regression_count  = Safe_UInt(2)                    ,
                                          avg_improvement   = Safe_Float(15.5)                ,
                                          avg_regression    = Safe_Float(8.2)                 )

        with self.exporter as _:
            json_str = _.export_statistics(result)
            data     = json_loads(json_str)

            assert type(data) is dict

    def test_export_statistics__contains_fields(self):                           # Test required fields
        result = Schema__Perf__Statistics(status            = Enum__Comparison__Status.SUCCESS,
                                          session_count     = Safe_UInt(3)                    ,
                                          benchmark_count   = Safe_UInt(10)                   ,
                                          improvement_count = Safe_UInt(5)                    ,
                                          regression_count  = Safe_UInt(2)                    ,
                                          avg_improvement   = Safe_Float(15.5)                ,
                                          avg_regression    = Safe_Float(8.2)                 )

        with self.exporter as _:
            json_str = _.export_statistics(result)
            data     = json_loads(json_str)

            assert 'status'             in data
            assert 'session_count'      in data
            assert 'benchmark_count'    in data
            assert 'improvement_count'  in data
            assert 'regression_count'   in data
            assert 'avg_improvement'    in data
            assert 'avg_regression'     in data
            assert 'timestamp'          in data

    def test_export_statistics__values(self):                                    # Test field values
        result = Schema__Perf__Statistics(status            = Enum__Comparison__Status.SUCCESS,
                                          session_count     = Safe_UInt(3)                    ,
                                          benchmark_count   = Safe_UInt(10)                   ,
                                          improvement_count = Safe_UInt(5)                    ,
                                          regression_count  = Safe_UInt(2)                    ,
                                          avg_improvement   = Safe_Float(15.5)                ,
                                          avg_regression    = Safe_Float(8.2)                 )

        with self.exporter as _:
            json_str = _.export_statistics(result)
            data     = json_loads(json_str)

            assert data['status']             == 'success'
            assert data['session_count']      == 3
            assert data['benchmark_count']    == 10
            assert data['improvement_count']  == 5
            assert data['regression_count']   == 2
            assert data['avg_improvement']    == 15.5
            assert data['avg_regression']     == 8.2

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
            json_str = _.export_statistics(result)
            data     = json_loads(json_str)

            assert 'best_improvement' in data
            assert data['best_improvement']['benchmark_id'] == 'A_01__test'
            assert data['best_improvement']['name']         == 'test_benchmark'

    def test_export_statistics__null_best_improvement(self):                     # Test null best
        result = Schema__Perf__Statistics(status            = Enum__Comparison__Status.SUCCESS,
                                          session_count     = Safe_UInt(3)                    ,
                                          benchmark_count   = Safe_UInt(5)                    ,
                                          improvement_count = Safe_UInt(0)                    ,
                                          regression_count  = Safe_UInt(0)                    ,
                                          avg_improvement   = Safe_Float(0.0)                 ,
                                          avg_regression    = Safe_Float(0.0)                 )

        with self.exporter as _:
            json_str = _.export_statistics(result)
            data     = json_loads(json_str)

            assert data['best_improvement'] is None
            assert data['worst_regression'] is None

    def test_export_statistics__error_status(self):                              # Test error status
        result = Schema__Perf__Statistics(status = Enum__Comparison__Status.ERROR_NO_SESSIONS,
                                          error  = 'No sessions loaded'                      )

        with self.exporter as _:
            json_str = _.export_statistics(result)
            data     = json_loads(json_str)

            assert data['status'] == 'no_sessions'
            assert data['error']  == 'No sessions loaded'


    # ═══════════════════════════════════════════════════════════════════════════════
    # Format Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_export__indented_format(self):                                      # Test pretty-print
        result = Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                               title_a     = 'Before'                        ,
                                               title_b     = 'After'                         ,
                                               comparisons = self.comparisons                )

        with self.exporter as _:
            json_str = _.export_comparison(result)

            assert '\n' in json_str                                              # Multi-line
            assert '  ' in json_str                                              # Indented
