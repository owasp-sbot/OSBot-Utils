# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf_Report - Main performance report container
# Single source of truth for report data, used by renderers and storage
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.performance.report.schemas.collections.Dict__Perf_Report__Legend      import Dict__Perf_Report__Legend
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Benchmarks  import List__Perf_Report__Benchmarks
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Categories  import List__Perf_Report__Categories
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Analysis              import Schema__Perf_Report__Analysis
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Metadata              import Schema__Perf_Report__Metadata
from osbot_utils.type_safe.Type_Safe                                                           import Type_Safe


class Schema__Perf_Report(Type_Safe):                               # Main report container
    metadata   : Schema__Perf_Report__Metadata                      # Report metadata
    benchmarks : List__Perf_Report__Benchmarks                      # Individual benchmark results
    categories : List__Perf_Report__Categories                      # Category summaries
    analysis   : Schema__Perf_Report__Analysis                      # Bottleneck analysis
    legend     : Dict__Perf_Report__Legend                          # Category descriptions
