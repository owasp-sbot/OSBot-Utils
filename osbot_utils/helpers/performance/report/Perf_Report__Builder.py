# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Report__Builder - Main entry point for performance report generation
# Runs benchmarks, calculates categories/percentages, identifies bottlenecks
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                          import Callable, Optional
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                                import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section         import Safe_Str__Benchmark__Section
from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config import Schema__Perf_Benchmark__Timing__Config
from osbot_utils.helpers.performance.report.schemas.collections.Dict__Perf_Report__Legend            import Dict__Perf_Report__Legend
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Benchmarks        import List__Perf_Report__Benchmarks
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Categories        import List__Perf_Report__Categories
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report                              import Schema__Perf_Report
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Analysis                    import Schema__Perf_Report__Analysis
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Benchmark                   import Schema__Perf_Report__Benchmark
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Builder__Config             import Schema__Perf_Report__Builder__Config
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Category                    import Schema__Perf_Report__Category
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Metadata                    import Schema__Perf_Report__Metadata
from osbot_utils.type_safe.primitives.core.Safe_Int import Safe_Int
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                       import type_safe
from osbot_utils.type_safe.Type_Safe                                                                 import Type_Safe


class Perf_Report__Builder(Type_Safe):                              # Main builder for performance reports
    metadata      : Schema__Perf_Report__Metadata                   # Report metadata
    legend        : Dict__Perf_Report__Legend                       # Category descriptions
    config        : Schema__Perf_Benchmark__Timing__Config          # Timing configuration
    builder_config: Schema__Perf_Report__Builder__Config            # Builder configuration

    # ═══════════════════════════════════════════════════════════════════════════
    # Main Entry Point
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def run(self, benchmarks_fn: Callable) -> Schema__Perf_Report:  # Run benchmarks and build report
        timing = Perf_Benchmark__Timing(config=self.config)
        benchmarks_fn(timing)

        benchmarks = self.build_benchmarks(timing)
        categories = self.build_categories(benchmarks)
        analysis   = self.build_analysis(benchmarks, categories)

        self.metadata.benchmark_count = len(benchmarks)

        return Schema__Perf_Report(metadata   = self.metadata   ,
                                   benchmarks = benchmarks      ,
                                   categories = categories      ,
                                   analysis   = analysis        ,
                                   legend     = self.legend     )

    # ═══════════════════════════════════════════════════════════════════════════
    # Build Benchmarks
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def build_benchmarks(self                                       ,
                         timing: Perf_Benchmark__Timing             ) -> List__Perf_Report__Benchmarks:
        benchmarks = List__Perf_Report__Benchmarks()
        total_ns   = self.calculate_total_ns(timing)

        for bench_id, result in timing.results.items():
            time_ns     = result.final_score
            category_id = self.extract_category_id(bench_id)
            pct         = (time_ns / total_ns * 100) if total_ns > 0 else 0

            benchmark = Schema__Perf_Report__Benchmark(benchmark_id = bench_id      ,
                                                       time_ns      = time_ns       ,
                                                       category_id  = category_id   ,
                                                       pct_of_total = pct           )
            benchmarks.append(benchmark)

        return benchmarks

    @type_safe
    def calculate_total_ns(self, timing: Perf_Benchmark__Timing) -> Safe_Int:
        total = 0
        for _, result in timing.results.items():
            total += result.final_score
        return total

    @type_safe
    def extract_category_id(self                                    ,
                            benchmark_id: str                       ) -> Safe_Str__Benchmark__Section:
        if '_' in benchmark_id:
            return Safe_Str__Benchmark__Section(benchmark_id.split('_')[0])
        return Safe_Str__Benchmark__Section(benchmark_id[0] if benchmark_id else 'X')

    # ═══════════════════════════════════════════════════════════════════════════
    # Build Categories
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def build_categories(self                                       ,
                         benchmarks: List__Perf_Report__Benchmarks  ) -> List__Perf_Report__Categories:
        cat_totals = {}                                             # {cat_id: total_ns}
        cat_counts = {}                                             # {cat_id: count}

        for benchmark in benchmarks:
            cat_id  = benchmark.category_id
            time_ns = benchmark.time_ns

            if cat_id not in cat_totals:
                cat_totals[cat_id] = 0
                cat_counts[cat_id] = 0

            cat_totals[cat_id] += time_ns
            cat_counts[cat_id] += 1

        total_ns   = sum(cat_totals.values())
        categories = List__Perf_Report__Categories()

        for cat_id in sorted(cat_totals.keys()):
            cat_ns      = cat_totals[cat_id]
            cat_count   = cat_counts[cat_id]
            pct         = (cat_ns / total_ns * 100) if total_ns > 0 else 0
            name, desc  = self.extract_category_name(cat_id)

            category = Schema__Perf_Report__Category(category_id     = cat_id    ,
                                                     name            = name      ,
                                                     description     = desc      ,
                                                     total_ns        = cat_ns    ,
                                                     pct_of_total    = pct       ,
                                                     benchmark_count = cat_count )
            categories.append(category)

        return categories

    @type_safe
    def extract_category_name(self, category_id: str) -> tuple:     # Returns (name, description)
        if self.legend and category_id in self.legend:
            legend_value = self.legend[category_id]

            if ' = ' in legend_value:                               # Format: "Name = Description"
                parts = legend_value.split(' = ', 1)
                return parts[0].strip(), parts[1].strip() if len(parts) > 1 else ''

            return legend_value, ''

        return f'Category {category_id}', ''

    # ═══════════════════════════════════════════════════════════════════════════
    # Build Analysis
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def build_analysis(self                                         ,
                       benchmarks: List__Perf_Report__Benchmarks    ,
                       categories: List__Perf_Report__Categories    ) -> Schema__Perf_Report__Analysis:
        bottleneck = self.find_bottleneck           (benchmarks)
        total_ns   = self.calculate_benchmarks_total(benchmarks)
        overhead   = self.calculate_overhead        (categories)
        insight    = self.generate_insight          (categories)

        return Schema__Perf_Report__Analysis(bottleneck_id  = bottleneck.benchmark_id if bottleneck else ''    ,
                                             bottleneck_ns  = bottleneck.time_ns      if bottleneck else 0     ,
                                             bottleneck_pct = bottleneck.pct_of_total if bottleneck else 0     ,
                                             total_ns       = total_ns                                         ,
                                             overhead_ns    = overhead                                         ,
                                             overhead_pct   = overhead / total_ns * 100 if total_ns > 0 else 0 ,
                                             key_insight    = insight                                          )

    @type_safe
    def find_bottleneck(self                                        ,
                        benchmarks: List__Perf_Report__Benchmarks   ) -> Optional[Schema__Perf_Report__Benchmark]:
        if not benchmarks:
            return None

        slowest = benchmarks[0]
        for benchmark in benchmarks:
            if benchmark.time_ns > slowest.time_ns:
                slowest = benchmark

        return slowest

    @type_safe
    def calculate_benchmarks_total(self                             ,
                                   benchmarks: List__Perf_Report__Benchmarks) -> Safe_Int:
        total = 0
        for benchmark in benchmarks:
            total += benchmark.time_ns
        return total

    @type_safe
    def calculate_overhead(self                                     ,
                           categories: List__Perf_Report__Categories) -> Safe_Int:
        config = self.builder_config if self.builder_config else Schema__Perf_Report__Builder__Config()

        full_id    = config.full_category_id if config.full_category_id else None
        create_id  = config.create_category_id if config.create_category_id else None
        convert_id = config.convert_category_id if config.convert_category_id else None

        cat_totals = {}
        for category in categories:
            cat_totals[category.category_id] = category.total_ns

        full_total    = cat_totals.get(full_id, 0) if full_id else 0
        create_total  = cat_totals.get(create_id, 0) if create_id else 0
        convert_total = cat_totals.get(convert_id, 0) if convert_id else 0

        if full_total > 0 and (create_total > 0 or convert_total > 0):
            return Safe_Int(int(full_total) - int(create_total) - int(convert_total))

        return 0

    @type_safe
    def generate_insight(self                                       ,
                         categories: List__Perf_Report__Categories  ) -> str:
        config = self.builder_config if self.builder_config else Schema__Perf_Report__Builder__Config()

        if config.include_auto_insight is False:
            return ''

        full_id   = config.full_category_id if config.full_category_id else None
        create_id = config.create_category_id if config.create_category_id else None

        if not full_id or not create_id:
            return ''

        cat_totals = {}
        cat_pcts   = {}
        for category in categories:
            cat_id             = category.category_id
            cat_totals[cat_id] = category.total_ns
            cat_pcts[cat_id]   = category.pct_of_total

        full_total   = cat_totals.get(full_id, 0)
        create_total = cat_totals.get(create_id, 0)

        if full_total == 0:
            return ''

        create_pct = (create_total / full_total) * 100 if full_total > 0 else 0

        if create_pct < 1.0:
            return f'Category {create_id} is {create_pct:.2f}% of {full_id} → NEGLIGIBLE'
        elif create_pct < 10.0:
            return f'Category {create_id} is {create_pct:.1f}% of {full_id} → Minor impact'
        else:
            return f'Category {create_id} is {create_pct:.1f}% of {full_id} → Significant'
