# ═══════════════════════════════════════════════════════════════════════════════
# List__Perf_Report__Categories - Typed list of category summaries
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Category import Schema__Perf_Report__Category
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List             import Type_Safe__List


class List__Perf_Report__Categories(Type_Safe__List):               # Collection of category summaries
    expected_type = Schema__Perf_Report__Category
