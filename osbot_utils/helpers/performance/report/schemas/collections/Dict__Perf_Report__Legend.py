# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Perf_Report__Legend - Typed dict mapping category ID to description
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description    import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section        import Safe_Str__Benchmark__Section
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                               import Type_Safe__Dict


class Dict__Perf_Report__Legend(Type_Safe__Dict):                   # Maps category ID to description
    expected_key_type   = Safe_Str__Benchmark__Section              # Category letter (A, B, C, ...)
    expected_value_type = Safe_Str__Benchmark__Description          # Description text
