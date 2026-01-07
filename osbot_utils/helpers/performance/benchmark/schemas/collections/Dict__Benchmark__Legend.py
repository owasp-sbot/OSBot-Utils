# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Benchmark__Legend - Type-safe mapping of sections to descriptions
# Maps section identifiers to human-readable descriptions
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title      import Safe_Str__Benchmark__Title
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section    import Safe_Str__Benchmark__Section
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                           import Type_Safe__Dict


class Dict__Benchmark__Legend(Type_Safe__Dict):                                  # {section → description}
    expected_key_type   = Safe_Str__Benchmark__Section
    expected_value_type = Safe_Str__Benchmark__Title
