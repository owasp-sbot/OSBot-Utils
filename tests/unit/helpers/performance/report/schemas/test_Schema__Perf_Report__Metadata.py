# ═══════════════════════════════════════════════════════════════════════════════
# test_Schema__Perf_Report__Metadata - Tests for report metadata schema
# ═══════════════════════════════════════════════════════════════════════════════
from types import NoneType
from unittest                                                                                        import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Measure_Mode                      import Enum__Measure_Mode
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description     import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title           import Safe_Str__Benchmark__Title
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Metadata                    import Schema__Perf_Report__Metadata
from osbot_utils.helpers.performance.testing.QA__Perf_Report__Test_Data                              import QA__Perf_Report__Test_Data
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                 import Safe_UInt
from osbot_utils.type_safe.Type_Safe                                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now                     import Timestamp_Now


class test_Schema__Perf_Report__Metadata(TestCase):

    @classmethod
    def setUpClass(cls):                                            # Shared test data
        cls.test_data = QA__Perf_Report__Test_Data()

    def test__init__(self):                                         # Test initialization
        with Schema__Perf_Report__Metadata() as _:
            assert type(_)                is Schema__Perf_Report__Metadata
            assert isinstance(_, Type_Safe)
            assert type(_.timestamp)      is Timestamp_Now
            assert type(_.version)        is Safe_Str__Benchmark__Title
            assert type(_.title)          is Safe_Str__Benchmark__Title
            assert type(_.description)    is Safe_Str__Benchmark__Description
            assert type(_.test_input)     is Safe_Str__Benchmark__Description
            assert type(_.measure_mode)   is NoneType
            assert type(_.benchmark_count) is Safe_UInt

    def test__init____with_values(self):                            # Test with explicit values
        with Schema__Perf_Report__Metadata(title           = 'Test Title'                       ,
                                           version         = '1.0.0'                            ,
                                           description     = 'Test description'                 ,
                                           test_input      = '<html></html>'                    ,
                                           measure_mode    = Enum__Measure_Mode.FAST            ,
                                           benchmark_count = 10                                 ) as _:
            assert str(_.title)           == 'Test Title'
            assert str(_.version)         == '1.0.0'
            assert str(_.description)     == 'Test description'
            assert str(_.test_input)      == '<html></html>'
            assert _.measure_mode         == Enum__Measure_Mode.FAST
            assert int(_.benchmark_count) == 10

    def test_factory_method(self):                                  # Test using factory
        with self.test_data as _:
            metadata = _.create_metadata(title='My Report', version='2.0.0')

            assert str(metadata.title)   == 'My Report'
            assert str(metadata.version) == '2.0.0'
            assert type(metadata.timestamp) is Timestamp_Now

    def test_json_round_trip(self):                                 # Test JSON serialization
        with self.test_data as _:
            metadata = _.create_metadata()
            json_data = metadata.json()
            restored = Schema__Perf_Report__Metadata.from_json(json_data)

            assert str(restored.title)       == str(metadata.title)
            assert str(restored.version)     == str(metadata.version)
            assert str(restored.description) == str(metadata.description)
