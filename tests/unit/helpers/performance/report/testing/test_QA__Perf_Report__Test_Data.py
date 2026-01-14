# ═══════════════════════════════════════════════════════════════════════════════
# test_QA__Perf_Report__Test_Data - Tests for test data factory
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                  import TestCase
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report                        import Schema__Perf_Report
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Analysis              import Schema__Perf_Report__Analysis
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Benchmark             import Schema__Perf_Report__Benchmark
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Builder__Config       import Schema__Perf_Report__Builder__Config
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Category              import Schema__Perf_Report__Category
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Metadata              import Schema__Perf_Report__Metadata
from osbot_utils.helpers.performance.report.schemas.collections.Dict__Perf_Report__Legend      import Dict__Perf_Report__Legend
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Benchmarks  import List__Perf_Report__Benchmarks
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Categories  import List__Perf_Report__Categories
from osbot_utils.helpers.performance.report.testing.QA__Perf_Report__Test_Data                 import QA__Perf_Report__Test_Data
from osbot_utils.type_safe.Type_Safe                                                           import Type_Safe


class test_QA__Perf_Report__Test_Data(TestCase):

    @classmethod
    def setUpClass(cls):                                            # Shared instance
        cls.test_data = QA__Perf_Report__Test_Data()

    def test__init__(self):                                         # Test initialization
        with QA__Perf_Report__Test_Data() as _:
            assert type(_)         is QA__Perf_Report__Test_Data
            assert isinstance(_, Type_Safe)

    # ═══════════════════════════════════════════════════════════════════════════
    # Sample Data Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_benchmark_ids(self):                                   # Test benchmark ID constants
        with self.test_data as _:
            assert _.benchmark_id_1 == 'A_01__full_operation'
            assert _.benchmark_id_3 == 'B_01__create_only'
            assert _.benchmark_id_5 == 'C_01__convert_only'

    def test_sections(self):                                        # Test section constants
        with self.test_data as _:
            assert _.section_a == 'A'
            assert _.section_b == 'B'
            assert _.section_c == 'C'

    def test_times(self):                                           # Test time constants
        with self.test_data as _:
            assert _.time_1_ms   == 1_000_000
            assert _.time_10_ms  == 10_000_000
            assert _.time_100_us == 100_000
            assert _.time_1_us   == 1_000

    # ═══════════════════════════════════════════════════════════════════════════
    # Target Function Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_target_nop(self):                                      # Test nop function
        with self.test_data as _:
            result = _.target_nop()
            assert result is None

    def test_target_simple(self):                                   # Test simple function
        with self.test_data as _:
            result = _.target_simple()
            assert result == 2

    def test_target_list(self):                                     # Test list function
        with self.test_data as _:
            result = _.target_list()
            assert result == list(range(10))

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Method Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_create_metadata(self):                                 # Test metadata factory
        with self.test_data as _:
            metadata = _.create_metadata()

            assert type(metadata)         is Schema__Perf_Report__Metadata
            assert str(metadata.title)    == 'Test Report'
            assert str(metadata.version)  == '1.0.0'

    def test_create_metadata__custom(self):                         # Test with custom values
        with self.test_data as _:
            metadata = _.create_metadata(title='Custom', version='2.0.0')

            assert str(metadata.title)   == 'Custom'
            assert str(metadata.version) == '2.0.0'

    def test_create_benchmark(self):                                # Test benchmark factory
        with self.test_data as _:
            benchmark = _.create_benchmark()

            assert type(benchmark)            is Schema__Perf_Report__Benchmark
            assert str(benchmark.benchmark_id) == 'A_01__test'
            assert int(benchmark.time_ns)      == 1_000_000

    def test_create_category(self):                                 # Test category factory
        with self.test_data as _:
            category = _.create_category()

            assert type(category)            is Schema__Perf_Report__Category
            assert str(category.category_id) == 'A'
            assert str(category.name)        == 'Full Operations'

    def test_create_analysis(self):                                 # Test analysis factory
        with self.test_data as _:
            analysis = _.create_analysis()

            assert type(analysis)            is Schema__Perf_Report__Analysis
            assert str(analysis.bottleneck_id) == 'A_01__test'
            assert int(analysis.total_ns)    == 2_000_000

    def test_create_legend(self):                                   # Test legend factory
        with self.test_data as _:
            legend = _.create_legend()

            assert type(legend) is Dict__Perf_Report__Legend
            assert len(legend)  == 3
            assert 'A' in legend
            assert 'B' in legend
            assert 'C' in legend

    def test_create_benchmarks_list(self):                          # Test benchmarks list factory
        with self.test_data as _:
            benchmarks = _.create_benchmarks_list()

            assert type(benchmarks) is List__Perf_Report__Benchmarks
            assert len(benchmarks)  == 6

    def test_create_benchmarks_list__custom_count(self):            # Test with custom count
        with self.test_data as _:
            benchmarks = _.create_benchmarks_list(count=3)

            assert len(benchmarks) == 3

    def test_create_categories_list(self):                          # Test categories list factory
        with self.test_data as _:
            categories = _.create_categories_list()

            assert type(categories) is List__Perf_Report__Categories
            assert len(categories)  == 3

    def test_create_report(self):                                   # Test full report factory
        with self.test_data as _:
            report = _.create_report()

            assert type(report)           is Schema__Perf_Report
            assert len(report.benchmarks) == 6
            assert len(report.categories) == 3
            assert len(report.legend)     == 3

    def test_create_report__custom_title(self):                     # Test with custom title
        with self.test_data as _:
            report = _.create_report(title='My Custom Report')

            assert str(report.metadata.title) == 'My Custom Report'

    def test_create_builder_config(self):                           # Test builder config factory
        with self.test_data as _:
            config = _.create_builder_config()

            assert type(config)              is Schema__Perf_Report__Builder__Config
            assert str(config.full_category_id)    == 'A'
            assert str(config.create_category_id)  == 'B'
            assert str(config.convert_category_id) == 'C'

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_integration__multiple_instances(self):                 # Test multiple instances
        data_1 = QA__Perf_Report__Test_Data()
        data_2 = QA__Perf_Report__Test_Data()

        assert data_1.benchmark_id_1 == data_2.benchmark_id_1
        assert data_1.time_1_ms      == data_2.time_1_ms

    def test_integration__independence(self):                       # Test data independence
        with self.test_data as _:
            report_1 = _.create_report(title='Report 1')
            report_2 = _.create_report(title='Report 2')

            assert str(report_1.metadata.title) == 'Report 1'
            assert str(report_2.metadata.title) == 'Report 2'
            assert report_1 is not report_2
