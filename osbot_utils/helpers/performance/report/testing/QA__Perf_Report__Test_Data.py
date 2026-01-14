# ═══════════════════════════════════════════════════════════════════════════════
# QA__Perf_Report__Test_Data - Test data factory for performance report tests
# Provides sample data for schemas, collections, and integration tests
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Measure_Mode                      import Enum__Measure_Mode
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id               import Safe_Str__Benchmark_Id
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description     import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section         import Safe_Str__Benchmark__Section
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title           import Safe_Str__Benchmark__Title
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report                              import Schema__Perf_Report
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Analysis                    import Schema__Perf_Report__Analysis
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Benchmark                   import Schema__Perf_Report__Benchmark
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Builder__Config             import Schema__Perf_Report__Builder__Config
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Category                    import Schema__Perf_Report__Category
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Metadata                    import Schema__Perf_Report__Metadata
from osbot_utils.helpers.performance.report.schemas.collections.Dict__Perf_Report__Legend            import Dict__Perf_Report__Legend
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Benchmarks        import List__Perf_Report__Benchmarks
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Categories        import List__Perf_Report__Categories
from osbot_utils.type_safe.primitives.core.Safe_Int                                                  import Safe_Int
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                 import Safe_UInt
from osbot_utils.type_safe.Type_Safe                                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.numerical.safe_float.Safe_Float__Percentage_Change     import Safe_Float__Percentage_Change
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                       import type_safe


class QA__Perf_Report__Test_Data(Type_Safe):                        # Test data factory for report tests

    # ═══════════════════════════════════════════════════════════════════════════
    # Sample Benchmark IDs
    # ═══════════════════════════════════════════════════════════════════════════

    benchmark_id_1: str = 'A_01__full_operation'
    benchmark_id_2: str = 'A_02__full_convert'
    benchmark_id_3: str = 'B_01__create_only'
    benchmark_id_4: str = 'B_02__setup_only'
    benchmark_id_5: str = 'C_01__convert_only'
    benchmark_id_6: str = 'C_02__execute_only'

    # ═══════════════════════════════════════════════════════════════════════════
    # Sample Values
    # ═══════════════════════════════════════════════════════════════════════════

    section_a    : str = 'A'
    section_b    : str = 'B'
    section_c    : str = 'C'
    time_1_ms    : int = 1_000_000                                  # 1ms in ns
    time_10_ms   : int = 10_000_000                                 # 10ms in ns
    time_100_us  : int = 100_000                                    # 100µs in ns
    time_1_us    : int = 1_000                                      # 1µs in ns

    # ═══════════════════════════════════════════════════════════════════════════
    # Target Functions for Benchmarking
    # ═══════════════════════════════════════════════════════════════════════════

    def target_nop(self):                                           # No-op function
        pass

    def target_simple(self):                                        # Simple computation
        return 1 + 1

    def target_list(self):                                          # List creation
        return list(range(10))

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods: Metadata
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_metadata(self                                        ,
                        title          : str = 'Test Report'        ,
                        version        : str = '1.0.0'              ,
                        description    : str = 'Test description'   ,
                        test_input     : str = '<html></html>'      ,
                        benchmark_count: int = 6                    ) -> Schema__Perf_Report__Metadata:
        return Schema__Perf_Report__Metadata(version         = version                  ,
                                             title           = title                    ,
                                             description     = description              ,
                                             test_input      = test_input               ,
                                             measure_mode    = Enum__Measure_Mode.FAST  ,
                                             benchmark_count = benchmark_count          )

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods: Benchmark
    # ═══════════════════════════════════════════════════════════════════════════

    def create_benchmark(self                                       ,
                         benchmark_id: str = 'A_01__test'           ,
                         time_ns     : int = 1_000_000              ,
                         category_id : str = 'A'                    ,
                         pct_of_total: float = 50.0                 ) -> Schema__Perf_Report__Benchmark:
        return Schema__Perf_Report__Benchmark(benchmark_id = Safe_Str__Benchmark_Id(benchmark_id)               ,
                                              time_ns      = Safe_UInt(time_ns)                                 ,
                                              category_id  = Safe_Str__Benchmark__Section(category_id)          ,
                                              pct_of_total = Safe_Float__Percentage_Change(pct_of_total)        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods: Category
    # ═══════════════════════════════════════════════════════════════════════════

    def create_category(self                                        ,
                        category_id    : str   = 'A'                ,
                        name           : str   = 'Full Operations'  ,
                        description    : str   = 'Full test'        ,
                        total_ns       : int   = 2_000_000          ,
                        pct_of_total   : float = 50.0               ,
                        benchmark_count: int   = 2                  ) -> Schema__Perf_Report__Category:
        return Schema__Perf_Report__Category(category_id     = Safe_Str__Benchmark__Section(category_id)        ,
                                             name            = Safe_Str__Benchmark__Title(name)                 ,
                                             description     = Safe_Str__Benchmark__Description(description)    ,
                                             total_ns        = Safe_UInt(total_ns)                              ,
                                             pct_of_total    = Safe_Float__Percentage_Change(pct_of_total)      ,
                                             benchmark_count = Safe_UInt(benchmark_count)                       )

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods: Analysis
    # ═══════════════════════════════════════════════════════════════════════════

    def create_analysis(self                                        ,
                        bottleneck_id : str   = 'A_01__test'        ,
                        bottleneck_ns : int   = 1_000_000           ,
                        bottleneck_pct: float = 50.0                ,
                        total_ns      : int   = 2_000_000           ,
                        overhead_ns   : int   = 1000                ,
                        overhead_pct  : float = 0.05                ,
                        key_insight   : str   = 'Test insight'      ) -> Schema__Perf_Report__Analysis:
        return Schema__Perf_Report__Analysis(bottleneck_id  = Safe_Str__Benchmark_Id(bottleneck_id)             ,
                                             bottleneck_ns  = Safe_UInt(bottleneck_ns)                          ,
                                             bottleneck_pct = Safe_Float__Percentage_Change(bottleneck_pct)     ,
                                             total_ns       = Safe_UInt(total_ns)                               ,
                                             overhead_ns    = Safe_Int(overhead_ns)                             ,
                                             overhead_pct   = Safe_Float__Percentage_Change(overhead_pct)       ,
                                             key_insight    = Safe_Str__Benchmark__Description(key_insight)     )

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods: Legend
    # ═══════════════════════════════════════════════════════════════════════════

    def create_legend(self) -> Dict__Perf_Report__Legend:           # Standard A/B/C legend
        return Dict__Perf_Report__Legend({'A': 'Full Operation = Create + Convert'      ,
                                          'B': 'Creation Only = Just instantiate'       ,
                                          'C': 'Convert Only = Call method'             })

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods: Benchmarks List
    # ═══════════════════════════════════════════════════════════════════════════

    def create_benchmarks_list(self, count: int = 6) -> List__Perf_Report__Benchmarks:
        benchmarks = List__Perf_Report__Benchmarks()
        samples    = [(self.benchmark_id_1, self.time_10_ms, 'A', 40.0)  ,
                      (self.benchmark_id_2, self.time_10_ms, 'A', 40.0)  ,
                      (self.benchmark_id_3, self.time_1_us , 'B', 0.01)  ,
                      (self.benchmark_id_4, self.time_1_us , 'B', 0.01)  ,
                      (self.benchmark_id_5, self.time_10_ms, 'C', 9.99)  ,
                      (self.benchmark_id_6, self.time_10_ms, 'C', 9.99)  ]

        for i in range(min(count, len(samples))):
            bench_id, time_ns, cat_id, pct = samples[i]
            benchmarks.append(self.create_benchmark(bench_id, time_ns, cat_id, pct))

        return benchmarks

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods: Categories List
    # ═══════════════════════════════════════════════════════════════════════════

    def create_categories_list(self) -> List__Perf_Report__Categories:
        categories = List__Perf_Report__Categories()
        categories.append(self.create_category('A', 'Full Operations', 'Full test', 20_000_000, 80.0, 2))
        categories.append(self.create_category('B', 'Creation Only'  , 'Setup'    , 2_000     , 0.02, 2))
        categories.append(self.create_category('C', 'Convert Only'   , 'Execute'  , 20_000_000, 19.98, 2))
        return categories

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods: Full Report
    # ═══════════════════════════════════════════════════════════════════════════

    def create_report(self                                          ,
                      title: str = 'Test Report'                    ) -> Schema__Perf_Report:
        return Schema__Perf_Report(metadata   = self.create_metadata(title=title)   ,
                                   benchmarks = self.create_benchmarks_list()       ,
                                   categories = self.create_categories_list()       ,
                                   analysis   = self.create_analysis()              ,
                                   legend     = self.create_legend()                )

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods: Builder Config
    # ═══════════════════════════════════════════════════════════════════════════

    def create_builder_config(self                                  ,
                              full_id   : str  = 'A'                ,
                              create_id : str  = 'B'                ,
                              convert_id: str  = 'C'                ) -> Schema__Perf_Report__Builder__Config:
        return Schema__Perf_Report__Builder__Config(full_category_id            = full_id   ,
                                                    create_category_id          = create_id ,
                                                    convert_category_id         = convert_id,
                                                    include_percentage_analysis = True      ,
                                                    include_stage_breakdown     = True      ,
                                                    include_auto_insight        = True      )
