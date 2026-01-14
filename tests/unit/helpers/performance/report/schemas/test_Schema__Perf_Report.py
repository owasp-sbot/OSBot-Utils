# ═══════════════════════════════════════════════════════════════════════════════
# test_Schema__Perf_Report - Tests for main report schema
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                 import TestCase
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report                       import Schema__Perf_Report
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Analysis             import Schema__Perf_Report__Analysis
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Metadata             import Schema__Perf_Report__Metadata
from osbot_utils.helpers.performance.report.schemas.collections.Dict__Perf_Report__Legend     import Dict__Perf_Report__Legend
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Benchmarks import List__Perf_Report__Benchmarks
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Categories import List__Perf_Report__Categories
from osbot_utils.helpers.performance.testing.QA__Perf_Report__Test_Data                       import QA__Perf_Report__Test_Data
from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe


class test_Schema__Perf_Report(TestCase):

    @classmethod
    def setUpClass(cls):                                            # Shared test data
        cls.test_data = QA__Perf_Report__Test_Data()

    def test__init__(self):                                         # Test initialization
        with Schema__Perf_Report() as _:
            assert type(_)           is Schema__Perf_Report
            assert isinstance(_, Type_Safe)
            assert type(_.metadata)   is Schema__Perf_Report__Metadata
            assert type(_.benchmarks) is List__Perf_Report__Benchmarks
            assert type(_.categories) is List__Perf_Report__Categories
            assert type(_.analysis)   is Schema__Perf_Report__Analysis
            assert type(_.legend)     is Dict__Perf_Report__Legend

    def test__init____empty_collections(self):                      # Test empty collections
        with Schema__Perf_Report() as _:
            assert len(_.benchmarks) == 0
            assert len(_.categories) == 0
            assert len(_.legend)     == 0

    def test_factory_method(self):                                  # Test using factory
        with self.test_data as _:
            report = _.create_report(title='Integration Test')

            assert str(report.metadata.title) == 'Integration Test'
            assert len(report.benchmarks)     == 6
            assert len(report.categories)     == 3
            assert len(report.legend)         == 3

    def test_json_round_trip(self):                                 # Test JSON serialization
        with self.test_data as _:
            report    = _.create_report()
            json_data = report.json()
            restored  = Schema__Perf_Report.from_json(json_data)

            assert str(restored.metadata.title)       == str(report.metadata.title)
            assert len(restored.benchmarks)           == len(report.benchmarks)
            assert len(restored.categories)           == len(report.categories)
            assert str(restored.analysis.bottleneck_id) == str(report.analysis.bottleneck_id)

    def test_json_round_trip__benchmarks(self):                     # Test benchmarks preserved
        with self.test_data as _:
            report    = _.create_report()
            json_data = report.json()
            restored  = Schema__Perf_Report.from_json(json_data)

            for i, benchmark in enumerate(restored.benchmarks):
                original = report.benchmarks[i]
                assert str(benchmark.benchmark_id) == str(original.benchmark_id)
                assert int(benchmark.time_ns)      == int(original.time_ns)

    def test_json_round_trip__categories(self):                     # Test categories preserved
        with self.test_data as _:
            report    = _.create_report()
            json_data = report.json()
            restored  = Schema__Perf_Report.from_json(json_data)

            for i, category in enumerate(restored.categories):
                original = report.categories[i]
                assert str(category.category_id) == str(original.category_id)
                assert str(category.name)        == str(original.name)
