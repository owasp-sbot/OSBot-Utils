# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf_Report__Builder__Config - Configuration for report builder
# Controls overhead calculation pattern and optional report sections
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section import Safe_Str__Benchmark__Section
from osbot_utils.type_safe.Type_Safe                                                         import Type_Safe


class Schema__Perf_Report__Builder__Config(Type_Safe):              # Builder configuration
    full_category_id              : Safe_Str__Benchmark__Section = 'A'    # Category for full operations
    create_category_id            : Safe_Str__Benchmark__Section = 'B'    # Category for creation only
    convert_category_id           : Safe_Str__Benchmark__Section = 'C'    # Category for conversion only
    include_percentage_analysis   : bool                         = True   # Show % relative to full
    include_stage_breakdown       : bool                         = True   # Show visual bars
    include_auto_insight          : bool                         = True   # Generate key insight text
