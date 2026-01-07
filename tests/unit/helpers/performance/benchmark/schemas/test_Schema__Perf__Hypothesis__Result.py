# ═══════════════════════════════════════════════════════════════════════════════
# test_Schema__Perf__Hypothesis__Result - Tests for hypothesis result schema
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description          import Safe_Str__Benchmark__Description
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Hypothesis__Result                   import Schema__Perf__Hypothesis__Result
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results                import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Hypothesis__Status                     import Enum__Hypothesis__Status
from osbot_utils.helpers.performance.benchmark.testing.QA__Benchmark__Test_Data                           import QA__Benchmark__Test_Data


class test_Schema__Perf__Hypothesis__Result(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Shared test data
        cls.test_data = QA__Benchmark__Test_Data()

    def test__init__(self):                                                      # Test initialization
        with Schema__Perf__Hypothesis__Result() as _:
            assert type(_)                   is Schema__Perf__Hypothesis__Result
            assert isinstance(_, Type_Safe)
            assert type(_.description)        is Safe_Str__Benchmark__Description
            assert type(_.target_improvement) is Safe_Float
            assert type(_.actual_improvement) is Safe_Float
            assert type(_.before_results)     is Dict__Benchmark_Results
            assert type(_.after_results)      is Dict__Benchmark_Results
            assert type(_.comments)           is Safe_Str__Benchmark__Description

    def test__init____with_values(self):                                         # Test with explicit values
        before_results = self.test_data.create_results_dict(count=2)
        after_results  = self.test_data.create_results_dict(count=2)

        with Schema__Perf__Hypothesis__Result(description        = Safe_Str__Benchmark__Description('Test hypothesis')              ,
                                              target_improvement = Safe_Float(0.5)                          ,
                                              actual_improvement = Safe_Float(0.75)                         ,
                                              before_results     = before_results                           ,
                                              after_results      = after_results                            ,
                                              status             = Enum__Hypothesis__Status.SUCCESS         ,
                                              comments           = Safe_Str__Benchmark__Description('Test passed')                  ) as _:
            assert str(_.description)            == 'Test hypothesis'
            assert float(_.target_improvement)   == 0.5
            assert float(_.actual_improvement)   == 0.75
            assert len(_.before_results)         == 2
            assert len(_.after_results)          == 2
            assert _.status                      == Enum__Hypothesis__Status.SUCCESS
            assert str(_.comments)               == 'Test passed'

    def test_status_values(self):                                                # Test all status values
        for status in Enum__Hypothesis__Status:
            with Schema__Perf__Hypothesis__Result(status = status) as _:
                assert _.status == status

    def test_improvement_percentages(self):                                      # Test improvement values
        with Schema__Perf__Hypothesis__Result(target_improvement = Safe_Float(0.50),
                                              actual_improvement = Safe_Float(0.75)) as _:
            assert float(_.target_improvement) == 0.50                           # 50%
            assert float(_.actual_improvement) == 0.75                           # 75%

    def test_json_serialization(self):                                           # Test JSON round-trip
        with Schema__Perf__Hypothesis__Result(description        = Safe_Str__Benchmark__Description('Test')                         ,
                                              target_improvement = Safe_Float(0.5)                          ,
                                              actual_improvement = Safe_Float(0.6)                          ,
                                              status             = Enum__Hypothesis__Status.SUCCESS         ) as _:
            json_data = _.json()

            assert type(json_data)       is dict
            assert 'description'         in json_data
            assert 'target_improvement'  in json_data
            assert 'actual_improvement'  in json_data
            assert 'status'              in json_data

    def test_negative_improvement(self):                                         # Test regression case
        with Schema__Perf__Hypothesis__Result(target_improvement = Safe_Float(0.5)  ,
                                              actual_improvement = Safe_Float(-0.2) ,
                                              status             = Enum__Hypothesis__Status.REGRESSION) as _:
            assert float(_.actual_improvement) == -0.2                           # Performance got worse
            assert _.status == Enum__Hypothesis__Status.REGRESSION
