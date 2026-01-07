# ═══════════════════════════════════════════════════════════════════════════════
# test_Schema__Perf__Benchmark__Result - Tests for benchmark result schema
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.testing.QA__Benchmark__Test_Data                           import QA__Benchmark__Test_Data
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Str                                                       import Safe_Str
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Result          import Schema__Perf__Benchmark__Result
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id                    import Safe_Str__Benchmark_Id
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section              import Safe_Str__Benchmark__Section
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Index                import Safe_Str__Benchmark__Index


class test_Schema__Perf__Benchmark__Result(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Shared test data
        cls.test_data = QA__Benchmark__Test_Data()

    def test__init__(self):                                                      # Test initialization
        with Schema__Perf__Benchmark__Result() as _:
            assert type(_)         is Schema__Perf__Benchmark__Result
            assert isinstance(_, Type_Safe)
            assert type(_.benchmark_id) is Safe_Str__Benchmark_Id
            assert type(_.section)      is Safe_Str__Benchmark__Section
            assert type(_.index)        is Safe_Str__Benchmark__Index
            assert type(_.name)         is Safe_Str
            assert type(_.final_score)  is Safe_UInt
            assert type(_.raw_score)    is Safe_UInt

    def test__init____with_values(self):                                         # Test with explicit values
        with Schema__Perf__Benchmark__Result(benchmark_id = Safe_Str__Benchmark_Id('A_01__test')      ,
                                             section      = Safe_Str__Benchmark__Section('A')         ,
                                             index        = Safe_Str__Benchmark__Index('01')          ,
                                             name         = Safe_Str('test')                          ,
                                             final_score  = Safe_UInt(100)                            ,
                                             raw_score    = Safe_UInt(87)                             ) as _:
            assert str(_.benchmark_id) == 'A_01__test'
            assert str(_.section)      == 'A'
            assert str(_.index)        == '01'
            assert str(_.name)         == 'test'
            assert int(_.final_score)  == 100
            assert int(_.raw_score)    == 87

    def test_factory_method(self):                                               # Test using factory method
        result = self.test_data.create_benchmark_result()

        assert type(result)            is Schema__Perf__Benchmark__Result
        assert str(result.benchmark_id) == self.test_data.benchmark_id_1
        assert str(result.section)      == self.test_data.section_a
        assert str(result.index)        == self.test_data.index_01
        assert int(result.final_score)  == 100
        assert int(result.raw_score)    == 87

    def test_factory_method__custom_values(self):                                # Test factory with custom values
        result = self.test_data.create_benchmark_result(benchmark_id = 'B_01__custom'                ,
                                                        section      = 'B'                           ,
                                                        index        = '01'                          ,
                                                        name         = 'custom'                      ,
                                                        final_score  = 500                           ,
                                                        raw_score    = 456                           )

        assert str(result.benchmark_id) == 'B_01__custom'
        assert str(result.section)      == 'B'
        assert str(result.index)        == '01'
        assert str(result.name)         == 'custom'
        assert int(result.final_score)  == 500
        assert int(result.raw_score)    == 456

    def test_json_serialization(self):                                           # Test JSON round-trip
        original = self.test_data.create_benchmark_result()
        json_data = original.json()

        assert type(json_data) is dict
        assert 'benchmark_id' in json_data
        assert 'final_score'  in json_data
        assert 'raw_score'    in json_data

    def test_from_json(self):                                                    # Test deserialization
        original  = self.test_data.create_benchmark_result()
        json_data = original.json()
        restored  = Schema__Perf__Benchmark__Result.from_json(json_data)

        assert type(restored)             is Schema__Perf__Benchmark__Result
        assert str(restored.benchmark_id) == str(original.benchmark_id)
        assert int(restored.final_score)  == int(original.final_score)
        assert int(restored.raw_score)    == int(original.raw_score)
