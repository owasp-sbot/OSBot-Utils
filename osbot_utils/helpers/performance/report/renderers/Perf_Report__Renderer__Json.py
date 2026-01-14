# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Report__Renderer__Json - JSON format renderer
# Serializes Schema__Perf_Report to JSON string
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Base import Perf_Report__Renderer__Base
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report           import Schema__Perf_Report
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                    import type_safe
from osbot_utils.utils.Json                                                       import json_dumps


class Perf_Report__Renderer__Json(Perf_Report__Renderer__Base):     # JSON format renderer

    @type_safe
    def render(self, report: Schema__Perf_Report) -> str:           # Render report to JSON
        return json_dumps(report.json(), indent=2)
