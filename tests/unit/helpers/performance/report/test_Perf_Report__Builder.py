# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Report__Builder - Tests for report builder
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                                    import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                                            import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Measure_Mode                                  import Enum__Measure_Mode
from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config             import Schema__Perf_Benchmark__Timing__Config
from osbot_utils.helpers.performance.report.Perf_Report__Builder                                                 import Perf_Report__Builder
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report                                          import Schema__Perf_Report
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Builder__Config                         import Schema__Perf_Report__Builder__Config
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Category                                import Schema__Perf_Report__Category
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Metadata                                import Schema__Perf_Report__Metadata
from osbot_utils.helpers.performance.report.schemas.collections.Dict__Perf_Report__Legend                        import Dict__Perf_Report__Legend
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Benchmarks                    import List__Perf_Report__Benchmarks
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Categories                    import List__Perf_Report__Categories
from osbot_utils.helpers.performance.report.testing.QA__Perf_Report__Test_Data                                   import QA__Perf_Report__Test_Data
from osbot_utils.type_safe.Type_Safe                                                                             import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Int import Safe_Int


class test_Perf_Report__Builder(TestCase):

    @classmethod
    def setUpClass(cls):                                            # Shared test data
        cls.test_data = QA__Perf_Report__Test_Data()
        cls.config    = Schema__Perf_Benchmark__Timing__Config(title            = 'Builder Test'    ,
                                                               print_to_console = False             ,
                                                               measure_quick    = True              )

    def test__init__(self):                                         # Test initialization
        with Perf_Report__Builder() as _:
            assert type(_)              is Perf_Report__Builder
            assert isinstance(_, Type_Safe)
            assert type(_.metadata)      is Schema__Perf_Report__Metadata
            assert type(_.legend)        is Dict__Perf_Report__Legend
            assert type(_.config)        is Schema__Perf_Benchmark__Timing__Config
            assert type(_.builder_config) is Schema__Perf_Report__Builder__Config

    def test__init____with_config(self):                            # Test with config
        metadata = self.test_data.create_metadata(title='Configured Test')
        legend   = self.test_data.create_legend()

        with Perf_Report__Builder(metadata = metadata    ,
                                  legend   = legend      ,
                                  config   = self.config ) as _:
            assert str(_.metadata.title) == 'Configured Test'
            assert len(_.legend)         == 3

    # ═══════════════════════════════════════════════════════════════════════════
    # Extract Methods Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_extract_category_id(self):                             # Test category extraction
        with Perf_Report__Builder() as _:
            cat_id = _.extract_category_id('A_01__test')
            assert str(cat_id) == 'A'

    def test_extract_category_id__complex(self):                    # Test complex ID
        with Perf_Report__Builder() as _:
            cat_id = _.extract_category_id('B_02__type_safe__convert')
            assert str(cat_id) == 'B'

    def test_extract_category_id__no_underscore(self):              # Test ID without underscore
        with Perf_Report__Builder() as _:
            cat_id = _.extract_category_id('simple')
            assert str(cat_id) == 's'

    def test_extract_category_name(self):                           # Test name extraction from legend
        legend = self.test_data.create_legend()

        with Perf_Report__Builder(legend=legend) as _:
            name, desc = _.extract_category_name('A')
            assert 'Full Operation' in name

    def test_extract_category_name__missing(self):                  # Test missing category
        with Perf_Report__Builder() as _:
            name, desc = _.extract_category_name('X')
            assert name == 'Category X'

    # ═══════════════════════════════════════════════════════════════════════════
    # Build Methods Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_build_benchmarks(self):                                # Test build_benchmarks
        def sample_benchmarks(timing: Perf_Benchmark__Timing):
            timing.benchmark('A_01__test', self.test_data.target_nop)
            timing.benchmark('B_01__test', self.test_data.target_simple)

        with Perf_Report__Builder(config=self.config) as _:
            timing = Perf_Benchmark__Timing(config=self.config)
            sample_benchmarks(timing)

            benchmarks = _.build_benchmarks(timing)

            assert type(benchmarks) is List__Perf_Report__Benchmarks
            assert len(benchmarks)  == 2
            assert str(benchmarks[0].category_id) == 'A'
            assert str(benchmarks[1].category_id) == 'B'

    def test_build_categories(self):                                # Test build_categories
        with self.test_data as td:
            benchmarks = td.create_benchmarks_list(count=4)

            with Perf_Report__Builder(legend=td.create_legend()) as _:
                categories = _.build_categories(benchmarks)

                assert type(categories) is List__Perf_Report__Categories
                assert len(categories)  == 2                        # A and B categories

    def test_find_bottleneck(self):                                 # Test bottleneck detection
        with self.test_data as td:
            benchmarks = td.create_benchmarks_list()

            with Perf_Report__Builder() as _:
                bottleneck = _.find_bottleneck(benchmarks)

                assert bottleneck is not None
                assert int(bottleneck.time_ns) > 0

    def test_calculate_overhead(self):                              # Test overhead calculation
        with self.test_data as td:
            categories = td.create_categories_list()

            with Perf_Report__Builder(builder_config=td.create_builder_config()) as _:
                overhead = _.calculate_overhead(categories)

                assert type(overhead) is Safe_Int

    # ═══════════════════════════════════════════════════════════════════════════
    # Run Method Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_run(self):                                             # Test run method
        def sample_benchmarks(timing: Perf_Benchmark__Timing):
            timing.benchmark('A_01__full', self.test_data.target_nop)
            timing.benchmark('B_01__create', self.test_data.target_simple)
            timing.benchmark('C_01__convert', self.test_data.target_list)

        metadata = self.test_data.create_metadata(title='Run Test')
        legend   = self.test_data.create_legend()

        with Perf_Report__Builder(metadata = metadata    ,
                                  legend   = legend      ,
                                  config   = self.config ) as _:
            report = _.run(sample_benchmarks)

            assert type(report)                   is Schema__Perf_Report
            assert len(report.benchmarks)         == 3
            assert len(report.categories)         == 3
            assert int(report.metadata.benchmark_count) == 3

    def test_run__multiple_benchmarks_per_category(self):           # Test multiple per category
        def sample_benchmarks(timing: Perf_Benchmark__Timing):
            timing.benchmark('A_01__test1', self.test_data.target_nop)
            timing.benchmark('A_02__test2', self.test_data.target_simple)
            timing.benchmark('A_03__test3', self.test_data.target_list)

        with Perf_Report__Builder(config=self.config) as _:
            report = _.run(sample_benchmarks)

            assert len(report.benchmarks) == 3
            assert len(report.categories) == 1                      # All in category A

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_integration__full_workflow(self):                      # Test complete workflow
        def benchmarks(timing: Perf_Benchmark__Timing):
            timing.benchmark('A_01__full_op', self.test_data.target_list)
            timing.benchmark('B_01__create' , self.test_data.target_nop)
            timing.benchmark('C_01__convert', self.test_data.target_simple)

        metadata = Schema__Perf_Report__Metadata(title        = 'Integration Test'          ,
                                                 version      = '1.0.0'                     ,
                                                 description  = 'Full workflow test'        ,
                                                 test_input   = 'test'                      ,
                                                 measure_mode = Enum__Measure_Mode.FAST     )
        legend = Dict__Perf_Report__Legend({'A': 'Full = Create + Convert'                  ,
                                            'B': 'Create = Setup only'                      ,
                                            'C': 'Convert = Execute only'                   })

        builder = Perf_Report__Builder(metadata = metadata                                  ,
                                       legend   = legend                                    ,
                                       config   = self.config                               )
        report  = builder.run(benchmarks)

        assert type(report)                       is Schema__Perf_Report
        assert str(report.metadata.title)         == 'Integration Test'
        assert int(report.metadata.benchmark_count) == 3
        assert len(report.benchmarks)             == 3
        assert len(report.categories)             == 3
        assert report.analysis is not None
        assert str(report.analysis.bottleneck_id) != ''

    def test_integration__json_round_trip(self):                    # Test JSON round-trip
        def benchmarks(timing: Perf_Benchmark__Timing):
            timing.benchmark('A_01__test', self.test_data.target_nop)

        with Perf_Report__Builder(config=self.config) as builder:
            report    = builder.run(benchmarks)
            json_data = report.json()
            restored  = Schema__Perf_Report.from_json(json_data)

            assert len(restored.benchmarks) == len(report.benchmarks)
            assert str(restored.analysis.bottleneck_id) == str(report.analysis.bottleneck_id)

    # ═══════════════════════════════════════════════════════════════════════════
    # extract_category_name Coverage Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_extract_category_name__no_equals_sign(self):           # Test legend value without ' = '
        legend = Dict__Perf_Report__Legend({'A': 'Full Operations'})

        with Perf_Report__Builder(legend=legend) as _:
            name, desc = _.extract_category_name('A')

            assert name == 'Full Operations'
            assert desc == ''

    def test_extract_category_name__not_in_legend(self):            # Test category not in legend
        with Perf_Report__Builder() as _:
            name, desc = _.extract_category_name('Z')

            assert name == 'Category Z'
            assert desc == ''

    # ═══════════════════════════════════════════════════════════════════════════
    # find_bottleneck Coverage Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_find_bottleneck__empty_list(self):                     # Test empty benchmarks list
        with Perf_Report__Builder() as _:
            benchmarks = List__Perf_Report__Benchmarks()
            result     = _.find_bottleneck(benchmarks)

            assert result is None

    def test_find_bottleneck__finds_slowest(self):                  # Test finds benchmark with highest time
        with self.test_data as td:
            benchmarks = List__Perf_Report__Benchmarks()
            benchmarks.append(td.create_benchmark('A_01__fast', time_ns=1_000))
            benchmarks.append(td.create_benchmark('A_02__slow', time_ns=10_000))
            benchmarks.append(td.create_benchmark('A_03__medium', time_ns=5_000))

            with Perf_Report__Builder() as _:
                result = _.find_bottleneck(benchmarks)

                assert str(result.benchmark_id) == 'A_02__slow'
                assert int(result.time_ns)      == 10_000

    # ═══════════════════════════════════════════════════════════════════════════
    # generate_insight Coverage Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_generate_insight__disabled_in_config(self):            # Test when auto_insight disabled
        with self.test_data as td:
            config = td.create_builder_config()
            config.include_auto_insight = False
            categories = td.create_categories_list()

            with Perf_Report__Builder(builder_config=config) as _:
                result = _.generate_insight(categories)

                assert result == ''

    def test_generate_insight__empty_full_category_id(self):        # Test when full_category_id is empty
        with self.test_data as td:
            config = Schema__Perf_Report__Builder__Config(full_category_id   = '',
                                                          create_category_id = 'B')
            categories = td.create_categories_list()

            with Perf_Report__Builder(builder_config=config) as _:
                result = _.generate_insight(categories)

                assert result == ''

    def test_generate_insight__empty_create_category_id(self):      # Test when create_category_id is empty
        with self.test_data as td:
            config = Schema__Perf_Report__Builder__Config(full_category_id   = 'A',
                                                          create_category_id = '')
            categories = td.create_categories_list()

            with Perf_Report__Builder(builder_config=config) as _:
                result = _.generate_insight(categories)

                assert result == ''

    def test_generate_insight__full_total_zero(self):               # Test when full category total is zero
        with self.test_data as td:
            config     = td.create_builder_config()
            categories = td.create_categories_list()

            # Set category A's total_ns to 0
            for category in categories:
                if str(category.category_id) == 'A':
                    category.total_ns = 0

            with Perf_Report__Builder(builder_config=config) as _:
                result = _.generate_insight(categories)

                assert result == ''

    def test_generate_insight__negligible(self):                    # Test NEGLIGIBLE insight (< 1%)
        with self.test_data as td:
            config     = td.create_builder_config()
            categories = List__Perf_Report__Categories()
            categories.append(Schema__Perf_Report__Category(
                category_id     = 'A'           ,
                name            = 'Full'        ,
                description     = ''            ,
                total_ns        = 100_000_000   ,   # 100ms
                pct_of_total    = 80.0          ,
                benchmark_count = 2             ))
            categories.append(Schema__Perf_Report__Category(
                category_id     = 'B'           ,
                name            = 'Create'      ,
                description     = ''            ,
                total_ns        = 100_000       ,   # 0.1ms = 0.1%
                pct_of_total    = 0.1           ,
                benchmark_count = 2             ))

            with Perf_Report__Builder(builder_config=config) as _:
                result = _.generate_insight(categories)
                assert 'NEGLIGIBLE' in result

    def test_generate_insight__minor_impact(self):                  # Test Minor impact insight (1-10%)
        with self.test_data as td:
            config     = td.create_builder_config()
            categories = List__Perf_Report__Categories()
            categories.append(Schema__Perf_Report__Category(
                category_id     = 'A'           ,
                name            = 'Full'        ,
                description     = ''            ,
                total_ns        = 100_000_000   ,   # 100ms
                pct_of_total    = 80.0          ,
                benchmark_count = 2             ))
            categories.append(Schema__Perf_Report__Category(
                category_id     = 'B'           ,
                name            = 'Create'      ,
                description     = ''            ,
                total_ns        = 5_000_000     ,   # 5ms = 5%
                pct_of_total    = 5.0           ,
                benchmark_count = 2             ))

            with Perf_Report__Builder(builder_config=config) as _:
                result = _.generate_insight(categories)

                assert 'Minor impact' in result

    def test_generate_insight__significant(self):                   # Test Significant insight (> 10%)
        with self.test_data as td:
            config     = td.create_builder_config()
            categories = List__Perf_Report__Categories()
            categories.append(Schema__Perf_Report__Category(
                category_id     = 'A'           ,
                name            = 'Full'        ,
                description     = ''            ,
                total_ns        = 100_000_000   ,   # 100ms
                pct_of_total    = 80.0          ,
                benchmark_count = 2             ))
            categories.append(Schema__Perf_Report__Category(
                category_id     = 'B'           ,
                name            = 'Create'      ,
                description     = ''            ,
                total_ns        = 20_000_000    ,   # 20ms = 20%
                pct_of_total    = 20.0          ,
                benchmark_count = 2             ))

            with Perf_Report__Builder(builder_config=config) as _:
                result = _.generate_insight(categories)

                assert 'Significant' in result

    def test_generate_insight__missing_category_ids(self):          # Test when category IDs are None
        with self.test_data as td:
            config = Schema__Perf_Report__Builder__Config(full_category_id    = None,
                                                          create_category_id  = None,
                                                          convert_category_id = None)
            categories = td.create_categories_list()

            with Perf_Report__Builder(builder_config=config) as _:
                result = _.generate_insight(categories)
                assert result != ''
                #assert result == 'Category B is 0.01% of A → NEGLIGIBLE'

