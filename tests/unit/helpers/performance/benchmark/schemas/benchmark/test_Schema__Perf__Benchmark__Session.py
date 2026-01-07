# ═══════════════════════════════════════════════════════════════════════════════
# test_Schema__Perf__Benchmark__Session - Tests for benchmark session schema
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description          import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title                import Safe_Str__Benchmark__Title
from osbot_utils.helpers.performance.benchmark.testing.QA__Benchmark__Test_Data                           import QA__Benchmark__Test_Data
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Session         import Schema__Perf__Benchmark__Session
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results                import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark__Legend                import Dict__Benchmark__Legend


class test_Schema__Perf__Benchmark__Session(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Shared test data
        cls.test_data = QA__Benchmark__Test_Data()

    def test__init__(self):                                                      # Test initialization
        with Schema__Perf__Benchmark__Session() as _:
            assert type(_)           is Schema__Perf__Benchmark__Session
            assert isinstance(_, Type_Safe)
            assert type(_.title)       is Safe_Str__Benchmark__Title
            assert type(_.description) is Safe_Str__Benchmark__Description
            assert type(_.results)     is Dict__Benchmark_Results
            assert type(_.legend)      is Dict__Benchmark__Legend

    def test__init____with_values(self):                                         # Test with explicit values
        results = self.test_data.create_results_dict(count=2)
        legend  = self.test_data.create_legend()

        with Schema__Perf__Benchmark__Session(title       = 'Test Session'              ,
                                              description = 'Test description'          ,
                                              results     = results                     ,
                                              legend      = legend                      ) as _:
            assert str(_.title)       == 'Test Session'
            assert str(_.description) == 'Test description'
            assert len(_.results)     == 2
            assert len(_.legend)      == 2

    def test_factory_method(self):                                               # Test using factory method
        session = self.test_data.create_session()

        assert type(session)           is Schema__Perf__Benchmark__Session
        assert str(session.title)      == 'Test Session'
        assert str(session.description) == 'Test description'
        assert len(session.results)    == 3
        assert len(session.legend)     == 2

    def test_factory_method__custom_count(self):                                 # Test factory with custom count
        session = self.test_data.create_session(title='Custom', result_count=1)

        assert str(session.title)   == 'Custom'
        assert len(session.results) == 1

    def test_results_access(self):                                               # Test accessing results
        session = self.test_data.create_session()

        from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id import Safe_Str__Benchmark_Id

        result = session.results.get(Safe_Str__Benchmark_Id(self.test_data.benchmark_id_1))
        assert result is not None
        assert int(result.final_score) == self.test_data.score_100_ns

    def test_legend_access(self):                                                # Test accessing legend
        session = self.test_data.create_session()

        from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section import Safe_Str__Benchmark__Section

        desc = session.legend.get(Safe_Str__Benchmark__Section(self.test_data.section_a))
        assert str(desc) == 'Python Baselines'

    def test_json_serialization(self):                                           # Test JSON round-trip
        session   = self.test_data.create_session()
        json_data = session.json()

        assert type(json_data) is dict
        assert 'title'       in json_data
        assert 'description' in json_data
        assert 'results'     in json_data
        assert 'legend'      in json_data
