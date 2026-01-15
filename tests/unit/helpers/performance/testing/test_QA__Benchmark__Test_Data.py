# ═══════════════════════════════════════════════════════════════════════════════
# test_QA__Benchmark__Test_Data - Tests for shared test data class
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                                     import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Result          import Schema__Perf__Benchmark__Result
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Session         import Schema__Perf__Benchmark__Session
from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config      import Schema__Perf_Benchmark__Timing__Config
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title                import Safe_Str__Benchmark__Title
from osbot_utils.helpers.performance.benchmark.testing.QA__Benchmark__Test_Data                           import QA__Benchmark__Test_Data
from osbot_utils.testing.__                                                                               import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results                import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark__Legend                import Dict__Benchmark__Legend
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id                    import Safe_Str__Benchmark_Id
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section              import Safe_Str__Benchmark__Section


class test_QA__Benchmark__Test_Data(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Create shared instance
        cls.test_data = QA__Benchmark__Test_Data()

    def test__init__(self):                                                      # Test initialization
        with QA__Benchmark__Test_Data() as _:
            assert type(_)         is QA__Benchmark__Test_Data
            assert isinstance(_, Type_Safe)


    # ═══════════════════════════════════════════════════════════════════════════════
    # Sample Data Attributes Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_benchmark_ids(self):                                                # Test benchmark ID constants
        with self.test_data as _:
            assert _.benchmark_id_1       == 'A_01__python__nop'
            assert _.benchmark_id_2       == 'A_02__python__class_empty'
            assert _.benchmark_id_3       == 'B_01__type_safe__empty'
            assert _.benchmark_id_4       == 'B_02__type_safe__primitives'
            assert _.benchmark_id_5       == 'C_01__complex__nested'
            assert _.benchmark_id_invalid == 'invalid'

    def test_sections(self):                                                     # Test section constants
        with self.test_data as _:
            assert _.section_a == 'A'
            assert _.section_b == 'B'
            assert _.section_c == 'C'

    def test_indices(self):                                                      # Test index constants
        with self.test_data as _:
            assert _.index_01 == '01'
            assert _.index_02 == '02'

    def test_scores(self):                                                       # Test score constants
        with self.test_data as _:
            assert _.score_100_ns  == 100
            assert _.score_500_ns  == 500
            assert _.score_1_kns   == 1_000
            assert _.score_5_kns   == 5_000
            assert _.score_10_kns  == 10_000
            assert _.score_100_kns == 100_000


    # ═══════════════════════════════════════════════════════════════════════════════
    # Target Function Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_target_nop(self):                                                   # Test nop function
        with self.test_data as _:
            result = _.target_nop()
            assert result is None

    def test_target_simple(self):                                                # Test simple function
        with self.test_data as _:
            result = _.target_simple()
            assert result == 2

    def test_target_list(self):                                                  # Test list function
        with self.test_data as _:
            result = _.target_list()
            assert result == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            assert len(result) == 10


    # ═══════════════════════════════════════════════════════════════════════════════
    # Nested Class Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_TS__Empty(self):                                                    # Test empty Type_Safe class
        TS__Empty = QA__Benchmark__Test_Data.TS__Empty

        with TS__Empty() as _:
            assert type(_) is TS__Empty
            assert isinstance(_, Type_Safe)

    def test_TS__With_Primitives(self):                                          # Test Type_Safe with primitives
        TS__With_Primitives = QA__Benchmark__Test_Data.TS__With_Primitives

        with TS__With_Primitives() as _:
            assert type(_) is TS__With_Primitives
            assert isinstance(_, Type_Safe)
            assert type(_.name)  is str
            assert type(_.value) is int

    def test_TS__With_Primitives__with_values(self):                             # Test with explicit values
        TS__With_Primitives = QA__Benchmark__Test_Data.TS__With_Primitives

        with TS__With_Primitives(name='test', value=42) as _:
            assert _.name  == 'test'
            assert _.value == 42


    # ═══════════════════════════════════════════════════════════════════════════════
    # Factory Method Tests: create_benchmark_result
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_create_benchmark_result(self):                                      # Test with defaults
        with self.test_data as _:
            result = _.create_benchmark_result()

            assert type(result)        is Schema__Perf__Benchmark__Result
            assert result.benchmark_id == _.benchmark_id_1
            assert result.section      == _.section_a
            assert result.index        == _.index_01
            assert result.name         == 'python__nop'
            assert result.final_score  == 100
            assert result.raw_score    == 87
            assert result.obj()        == __(benchmark_id='A_01__python__nop',
                                             section='A',
                                             index='01',
                                             name='python__nop',
                                             final_score=100,
                                             raw_score=87)

    def test_create_benchmark_result__custom_values(self):                       # Test with custom values
        with self.test_data as _:
            result = _.create_benchmark_result(benchmark_id = 'X_99__custom'    ,
                                               section      = 'X'               ,
                                               index        = '99'              ,
                                               name         = 'custom'          ,
                                               final_score  = 999               ,
                                               raw_score    = 888               )

            assert str(result.benchmark_id) == 'X_99__custom'
            assert str(result.section)      == 'X'
            assert str(result.index)        == '99'
            assert str(result.name)         == 'custom'
            assert int(result.final_score)  == 999
            assert int(result.raw_score)    == 888

    def test_create_benchmark_result__partial_custom(self):                      # Test with partial custom
        with self.test_data as _:
            result = _.create_benchmark_result(final_score = 500)

            assert str(result.benchmark_id) == _.benchmark_id_1                  # Default
            assert int(result.final_score)  == 500                               # Custom

    def test_create_benchmark_result__zero_scores(self):                         # Test zero scores
        with self.test_data as _:
            result = _.create_benchmark_result(final_score = 0,
                                               raw_score   = 0)

            assert int(result.final_score) == 0
            assert int(result.raw_score)   == 0


    # ═══════════════════════════════════════════════════════════════════════════════
    # Factory Method Tests: create_results_dict
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_create_results_dict(self):                                          # Test with default count
        with self.test_data as _:
            results = _.create_results_dict()

            assert type(results) is Dict__Benchmark_Results
            assert len(results)  == 3

    def test_create_results_dict__count_1(self):                                 # Test count=1
        with self.test_data as _:
            results = _.create_results_dict(count=1)

            assert len(results) == 1
            assert Safe_Str__Benchmark_Id(_.benchmark_id_1) in results

    def test_create_results_dict__count_2(self):                                 # Test count=2
        with self.test_data as _:
            results = _.create_results_dict(count=2)

            assert len(results) == 2
            assert Safe_Str__Benchmark_Id(_.benchmark_id_1) in results
            assert Safe_Str__Benchmark_Id(_.benchmark_id_2) in results

    def test_create_results_dict__count_3(self):                                 # Test count=3
        with self.test_data as _:
            results = _.create_results_dict(count=3)

            assert len(results) == 3
            assert Safe_Str__Benchmark_Id(_.benchmark_id_1) in results
            assert Safe_Str__Benchmark_Id(_.benchmark_id_2) in results
            assert Safe_Str__Benchmark_Id(_.benchmark_id_3) in results

    def test_create_results_dict__count_0(self):                                 # Test count=0 (empty)
        with self.test_data as _:
            results = _.create_results_dict(count=0)

            assert len(results) == 0

    def test_create_results_dict__result_values(self):                           # Test result values
        with self.test_data as _:
            results  = _.create_results_dict(count = 3)

            result_1 = results[Safe_Str__Benchmark_Id(_.benchmark_id_1)]
            result_2 = results[Safe_Str__Benchmark_Id(_.benchmark_id_2)]
            result_3 = results[Safe_Str__Benchmark_Id(_.benchmark_id_3)]

            assert int(result_1.final_score) == _.score_100_ns
            assert int(result_2.final_score) == _.score_500_ns
            assert int(result_3.final_score) == _.score_1_kns
            assert results.obj()             == __(A_01__python__nop         = __(benchmark_id = 'A_01__python__nop'        ,
                                                                                 section      = 'A'                        ,
                                                                                 index        = '01'                       ,
                                                                                 name         = 'python__nop'              ,
                                                                                 final_score  = 100                        ,
                                                                                 raw_score    = 87)                        ,
                                                   A_02__python__class_empty = __(benchmark_id = 'A_02__python__class_empty',
                                                                                 section       = 'A'                          ,
                                                                                 index         = '02'                         ,
                                                                                 name          = 'python__class_empty'       ,
                                                                                 final_score   = 500                          ,
                                                                                 raw_score     = 456)                        ,
                                                   B_01__type_safe__empty    = __(benchmark_id = 'B_01__type_safe__empty' ,
                                                                                 section       = 'B'                          ,
                                                                                 index         = '01'                         ,
                                                                                 name          = 'type_safe__empty'          ,
                                                                                 final_score   = 1000                         ,
                                                                                 raw_score     = 876))

    def test_create_results_dict__sections(self):                                # Test sections in results
        with self.test_data as _:
            results = _.create_results_dict(count=3)

            result_1 = results[Safe_Str__Benchmark_Id(_.benchmark_id_1)]
            result_3 = results[Safe_Str__Benchmark_Id(_.benchmark_id_3)]

            assert str(result_1.section) == _.section_a                          # Section A
            assert str(result_3.section) == _.section_b                          # Section B


    # ═══════════════════════════════════════════════════════════════════════════════
    # Factory Method Tests: create_legend
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_create_legend(self):                                                # Test legend creation
        with self.test_data as _:
            legend = _.create_legend()

            assert type(legend) is Dict__Benchmark__Legend
            assert len(legend)  == 2

    def test_create_legend__section_a(self):                                     # Test section A description
        with self.test_data as _:
            legend  = _.create_legend()
            key_a   = Safe_Str__Benchmark__Section(_.section_a)
            assert type(key_a        ) is Safe_Str__Benchmark__Section
            assert type(legend[key_a]) is Safe_Str__Benchmark__Title                               # BUG
            assert legend[key_a] == 'Python Baselines'

    def test_create_legend__section_b(self):                                     # Test section B description
        with self.test_data as _:
            legend  = _.create_legend()
            key_b   = Safe_Str__Benchmark__Section(_.section_b)

            assert str(legend[key_b]) == 'Type_Safe Creation'


    # ═══════════════════════════════════════════════════════════════════════════════
    # Factory Method Tests: create_session
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_create_session(self):                                               # Test with defaults
        with self.test_data as _:
            session = _.create_session()

            assert type(session)            is Schema__Perf__Benchmark__Session
            assert str(session.title)       == 'Test Session'
            assert str(session.description) == 'Test description'
            assert len(session.results)     == 3
            assert len(session.legend)      == 2

    def test_create_session__custom_title(self):                                 # Test custom title
        with self.test_data as _:
            session = _.create_session(title='Custom Title')

            assert str(session.title) == 'Custom Title'

    def test_create_session__custom_count(self):                                 # Test custom result count
        with self.test_data as _:
            session = _.create_session(result_count=1)

            assert len(session.results) == 1

    def test_create_session__full_custom(self):                                  # Test full custom
        with self.test_data as _:
            session = _.create_session(title='My Session', result_count=2)

            assert str(session.title)   == 'My Session'
            assert len(session.results) == 2


    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Method Tests: run_sample_benchmarks
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_run_sample_benchmarks(self):                                        # Test benchmark runner

        config = Schema__Perf_Benchmark__Timing__Config(title            ='Run Test',
                                                        print_to_console = False)

        with self.test_data as _:
            with Perf_Benchmark__Timing(config=config) as timing:
                _.run_sample_benchmarks(timing)

                assert len(timing.results) == 2


    # ═══════════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_integration__multiple_instances(self):                              # Test multiple instances
        data_1 = QA__Benchmark__Test_Data()
        data_2 = QA__Benchmark__Test_Data()

        assert data_1.benchmark_id_1 == data_2.benchmark_id_1
        assert data_1.score_100_ns   == data_2.score_100_ns

    def test_integration__results_independence(self):                            # Test results are independent
        with self.test_data as _:
            results_1 = _.create_results_dict(count=2)
            results_2 = _.create_results_dict(count=3)

            assert len(results_1) == 2
            assert len(results_2) == 3
            assert results_1 is not results_2

    def test_integration__session_with_results(self):                               # Test session contains results
        with self.test_data as _:
            session = _.create_session(result_count=3)

            result_1 = session.results[Safe_Str__Benchmark_Id(_.benchmark_id_1)]    # Verify results are accessible through session
            assert int(result_1.final_score) == _.score_100_ns

            key_a = Safe_Str__Benchmark__Section(_.section_a)                       # Verify legend matches sections
            assert str(session.legend[key_a]) == 'Python Baselines'
            assert session.obj()              == __(title       = 'Test Session'           ,
                                                    description = 'Test description'       ,
                                                    timestamp   = __SKIP__                 ,
                                                    results     = __(A_01__python__nop         = __(benchmark_id = 'A_01__python__nop'        ,
                                                                                                   section     = 'A'                          ,
                                                                                                   index       = '01'                         ,
                                                                                                   name        = 'python__nop'                ,
                                                                                                   final_score = 100                          ,
                                                                                                   raw_score   = 87)                          ,
                                                                     A_02__python__class_empty = __(benchmark_id = 'A_02__python__class_empty',
                                                                                                   section     = 'A'                          ,
                                                                                                   index       = '02'                         ,
                                                                                                   name        = 'python__class_empty'        ,
                                                                                                   final_score = 500                          ,
                                                                                                   raw_score   = 456)                         ,
                                                                     B_01__type_safe__empty    = __(benchmark_id = 'B_01__type_safe__empty'   ,
                                                                                                   section     = 'B'                          ,
                                                                                                   index       = '01'                         ,
                                                                                                   name        = 'type_safe__empty'           ,
                                                                                                   final_score = 1000                         ,
                                                                                                   raw_score   = 876))                        ,
                                                    legend      = __(A = 'Python Baselines'    ,
                                                                    B = 'Type_Safe Creation') )

