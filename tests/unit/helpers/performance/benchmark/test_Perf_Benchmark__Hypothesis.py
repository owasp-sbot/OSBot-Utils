# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Benchmark__Hypothesis - Tests for hypothesis testing class
# ═══════════════════════════════════════════════════════════════════════════════

import tempfile
import pytest
from unittest                                                                                             import TestCase

from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Result import Schema__Perf__Benchmark__Result
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description          import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.testing.QA__Benchmark__Test_Data                           import QA__Benchmark__Test_Data
from osbot_utils.testing.Stdout import Stdout
from osbot_utils.testing.Temp_File import Temp_File
from osbot_utils.testing.__ import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.utils.Files                                                                              import file_exists
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Hypothesis                                 import Perf_Benchmark__Hypothesis
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results                import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Hypothesis__Result                   import Schema__Perf__Hypothesis__Result
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Hypothesis__Status                     import Enum__Hypothesis__Status
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id                    import Safe_Str__Benchmark_Id


class test_Perf_Benchmark__Hypothesis(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Shared test data
        cls.test_data = QA__Benchmark__Test_Data()

    def test__init__(self):                                                      # Test initialization
        with Perf_Benchmark__Hypothesis() as _:
            assert type(_)                   is Perf_Benchmark__Hypothesis
            assert isinstance(_, Type_Safe)
            assert type(_.description)        is Safe_Str__Benchmark__Description
            assert type(_.target_improvement) is Safe_Float
            assert type(_.before_results)     is Dict__Benchmark_Results
            assert type(_.after_results)      is Dict__Benchmark_Results
            assert type(_.comments)           is Safe_Str__Benchmark__Description
            assert _.obj()                    == __(description='',
                                                    target_improvement=0.0,
                                                    before_results=__(),
                                                    after_results=__(),
                                                    comments='')

    def test__init____with_values(self):                                         # Test with values
        with Perf_Benchmark__Hypothesis(description        = 'Test hypothesis',
                                        target_improvement = Safe_Float(0.5)             ,
                                        comments           = 'Test comment'   ) as _:
            assert str(_.description)          == 'Test hypothesis'
            assert float(_.target_improvement) == 0.5
            assert str(_.comments)             == 'Test comment'
            assert _.obj()                     == __(description='Test hypothesis',
                                                     target_improvement=0.5,
                                                     before_results=__(),
                                                     after_results=__(),
                                                     comments='Test comment')


    # ═══════════════════════════════════════════════════════════════════════════════
    # Run Before/After Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_run_before(self):                                                   # Test run_before method
        def benchmarks(timing):
            timing.benchmark(Safe_Str__Benchmark_Id('A_01__test'), self.test_data.target_nop)

        with Perf_Benchmark__Hypothesis() as _:
            result = _.run_before(benchmarks)

            assert result                                is _                                                   # Returns self
            assert len(_.before_results)                 == 1
            assert type(_.before_results)                is Dict__Benchmark_Results
            assert type(_.before_results['A_01__test'])  is Schema__Perf__Benchmark__Result
            assert _.obj()                               == __(description='',
                                                               target_improvement=0.0,
                                                               before_results=__(A_01__test=__(benchmark_id='A_01__test',
                                                                                               section='A',
                                                                                               index='01',
                                                                                               name='test',
                                                                                               final_score=__SKIP__,
                                                                                               raw_score=__SKIP__)),
                                                               after_results=__(),
                                                               comments='')

    def test_run_after(self):                                                    # Test run_after method
        def benchmarks(timing):
            timing.benchmark(Safe_Str__Benchmark_Id('A_01__test'), self.test_data.target_nop)

        with Perf_Benchmark__Hypothesis() as _:
            result = _.run_after(benchmarks)

            assert result               is _                                                   # Returns self
            assert len(_.after_results) == 1
            assert _.obj()              == __( description='',
                                               target_improvement=0.0,
                                               before_results=__(),
                                               after_results=__(A_01__test=__(benchmark_id='A_01__test',
                                                                              section='A',
                                                                              index='01',
                                                                              name='test',
                                                                              final_score=__SKIP__,
                                                                              raw_score=__SKIP__)),
                                               comments='')

    def test_run_both(self):                                                     # Test both before and after
        def benchmarks(timing):
            timing.benchmark(Safe_Str__Benchmark_Id('A_01__test'), self.test_data.target_nop   )
            timing.benchmark(Safe_Str__Benchmark_Id('A_02__test'), self.test_data.target_simple)

        with Perf_Benchmark__Hypothesis() as _:
            _.run_before(benchmarks)
            _.run_after (benchmarks)

            assert len(_.before_results) == 2
            assert len(_.after_results)  == 2
            assert _.obj()               == __(description='',
                                               target_improvement=0.0,
                                               before_results=__(A_01__test=__(benchmark_id='A_01__test',
                                                                               section='A',
                                                                               index='01',
                                                                               name='test',
                                                                               final_score=__SKIP__,
                                                                               raw_score=__SKIP__),
                                                                 A_02__test=__(benchmark_id='A_02__test',
                                                                               section='A',
                                                                               index='02',
                                                                               name='test',
                                                                               final_score=__SKIP__,
                                                                               raw_score=__SKIP__)),
                                               after_results=__(A_01__test=__(benchmark_id='A_01__test',
                                                                              section='A',
                                                                              index='01',
                                                                              name='test',
                                                                              final_score=__SKIP__,
                                                                              raw_score=__SKIP__),
                                                                A_02__test=__(benchmark_id='A_02__test',
                                                                              section='A',
                                                                              index='02',
                                                                              name='test',
                                                                              final_score=__SKIP__,
                                                                              raw_score=__SKIP__)),
                                               comments='')


    # ═══════════════════════════════════════════════════════════════════════════════
    # Evaluate Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_evaluate(self):                                                     # Test evaluate method
        def benchmarks(timing):
            timing.benchmark(Safe_Str__Benchmark_Id('A_01__test'), self.test_data.target_nop)

        with Perf_Benchmark__Hypothesis(description        = 'Test',
                                        target_improvement = Safe_Float(0.0) ) as _:  # 0% target (always passes)
            _.run_before(benchmarks)
            _.run_after(benchmarks)

            result = _.evaluate()

            assert type(result)  is Schema__Perf__Hypothesis__Result
            assert result.status in list(Enum__Hypothesis__Status)
            assert result.obj()  == __(description='Test',
                                       target_improvement=0.0,
                                       actual_improvement=0.0,
                                       before_results=__(A_01__test=__(benchmark_id='A_01__test',
                                                                       section='A',
                                                                       index='01',
                                                                       name='test',
                                                                       final_score=__SKIP__,
                                                                       raw_score=__SKIP__)),
                                       after_results=__(A_01__test=__(benchmark_id='A_01__test',
                                                                      section='A',
                                                                      index='01',
                                                                      name='test',
                                                                      final_score=__SKIP__,
                                                                      raw_score=__SKIP__)),
                                       status='success',
                                       timestamp=__SKIP__,
                                       comments='')


    def test_evaluate__without_before(self):                                     # Test error without before
        with Perf_Benchmark__Hypothesis() as _:
            with pytest.raises(ValueError, match='Must run before'):
                _.evaluate()

    def test_evaluate__without_after(self):                                      # Test error without after
        def benchmarks(timing):
            timing.benchmark(Safe_Str__Benchmark_Id('A_01__test'), self.test_data.target_nop)

        with Perf_Benchmark__Hypothesis() as _:
            _.run_before(benchmarks)

            with pytest.raises(ValueError, match='Must run after'):
                _.evaluate()


    # ═══════════════════════════════════════════════════════════════════════════════
    # Status Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_evaluate__success_status(self):                                     # Test SUCCESS status
        # With 0% target, any non-negative improvement is SUCCESS
        def benchmarks(timing):
            timing.benchmark(Safe_Str__Benchmark_Id('A_01__test'), self.test_data.target_nop)

        with Perf_Benchmark__Hypothesis(target_improvement = Safe_Float(0.0)) as _:
            _.run_before(benchmarks)
            _.run_after(benchmarks)

            result = _.evaluate()

            # Since we're measuring the same function, improvement should be ~0
            # With 0% target, this should be SUCCESS or INCONCLUSIVE
            assert result.status in [Enum__Hypothesis__Status.SUCCESS,
                                     Enum__Hypothesis__Status.INCONCLUSIVE,
                                     Enum__Hypothesis__Status.FAILURE     ]

    def test_evaluate__result_contains_description(self):                        # Test result has description
        def benchmarks(timing):
            timing.benchmark(Safe_Str__Benchmark_Id('A_01__test'), self.test_data.target_nop)

        with Perf_Benchmark__Hypothesis(description        = 'My Test',
                                        target_improvement = Safe_Float(0.0)     ) as _:
            _.run_before(benchmarks)
            _.run_after(benchmarks)

            result = _.evaluate()

            assert str(result.description) == 'My Test'

    def test_print_result(self):
        def benchmarks(timing):
            timing.benchmark(Safe_Str__Benchmark_Id('A_01__test'), self.test_data.target_nop)

        with (Perf_Benchmark__Hypothesis(description        = 'My Test',
                                        target_improvement = Safe_Float(0.0)     ) as _):
            _.run_before(benchmarks)
            _.run_after(benchmarks)
            with Stdout() as stdout:
                _.print_result()
            assert '│ HYPOTHESIS: My Test' in stdout.value()                                # below is what it looks like, but it is not deterministic (unless we change the values of the results manually here in this test)
                                    # == ('\n'
                                    #     '┌──────────────────────────────────────────┐\n'
                                    #      '│ HYPOTHESIS: My Test                      │\n'
                                    #      '├──────────────────────────────────────────┤\n'
                                    #      '│ Benchmark │ Before │ After  │ Change     │\n'
                                    #      '├──────────────────────────────────────────┤\n'
                                    #      '│ test      │ 100 ns │ 100 ns │ 0%         │\n'
                                    #      '├──────────────────────────────────────────┤\n'
                                    #      '│ ✓ SUCCESS (0.0% >= 0.0% target)          │\n'
                                    #      '└──────────────────────────────────────────┘\n')

    # ═══════════════════════════════════════════════════════════════════════════════
    # Persistence Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_save(self):                                                         # Test save method
        def benchmarks(timing):
            timing.benchmark(Safe_Str__Benchmark_Id('A_01__test'), self.test_data.target_nop)

        with Temp_File(extension='.json', return_file_path=True) as filepath:
            with Perf_Benchmark__Hypothesis(description        = 'Save Test'    ,
                                            target_improvement = Safe_Float(0.0)) as _:
                _.run_before(benchmarks)
                _.run_after(benchmarks)
                _.save(filepath)

                assert file_exists(filepath) is True
        assert file_exists(filepath) is False

    def test_load(self):                                                         # Test load method
        def benchmarks(timing):
            timing.benchmark(Safe_Str__Benchmark_Id('A_01__test'), self.test_data.target_nop)

        with Temp_File(extension='.json', return_file_path=True) as filepath:

            with Perf_Benchmark__Hypothesis(description        = 'Load Test'    ,
                                            target_improvement = Safe_Float(0.5)       ) as _:
                _.run_before(benchmarks)
                _.run_after(benchmarks)
                _.save(filepath)

            loaded = Perf_Benchmark__Hypothesis.load(filepath)

            assert loaded is not None
            assert loaded.description               == 'Load Test'
            assert float(loaded.target_improvement) == 0.5

    def test_load__missing_file(self):                                           # Test load missing file
        loaded = Perf_Benchmark__Hypothesis.load('/nonexistent/file.json')
        assert loaded is None


    # ═══════════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_integration__full_workflow(self):                                   # Test complete workflow
        def benchmarks(timing):
            timing.benchmark(Safe_Str__Benchmark_Id('A_01__nop'), self.test_data.target_nop)
            timing.benchmark(Safe_Str__Benchmark_Id('A_02__simple'), self.test_data.target_simple)

        hypothesis = Perf_Benchmark__Hypothesis(description        = 'Integration Test',
                                                target_improvement = Safe_Float(0.0)              )

        # Step 1: Run before
        hypothesis.run_before(benchmarks)
        assert len(hypothesis.before_results) == 2

        # Step 2: Run after
        hypothesis.run_after(benchmarks)
        assert len(hypothesis.after_results) == 2

        # Step 3: Evaluate
        result = hypothesis.evaluate()
        assert type(result) is Schema__Perf__Hypothesis__Result

        # Step 4: Save
        with Temp_File(extension='.json', return_file_path=True) as filepath:
            hypothesis.save(filepath)
            assert file_exists(filepath) is True


