# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Report__Storage__Base - Abstract base for report storage backends
# Defines interface for save, load, list, exists operations
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                       import List
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report           import Schema__Perf_Report
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                    import type_safe
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe


class Perf_Report__Storage__Base(Type_Safe):                        # Abstract base for storage backends

    @type_safe
    def save(self                                 ,                 # Save report to storage
             report : Schema__Perf_Report         ,                 # Report to save
             key    : str                         ,                 # Storage key/name
             formats: List[str] = None            ) -> bool:        # Formats to save (txt, md, json)
        raise NotImplementedError()

    @type_safe
    def save_content(self                         ,                 # Save rendered content
                     key        : str             ,                 # Storage key/name
                     content    : str             ,                 # Rendered content
                     format_type: str             ) -> bool:        # Format type (txt, md, json)
        raise NotImplementedError()

    @type_safe
    def load(self, key: str) -> Schema__Perf_Report:                # Load report from storage
        raise NotImplementedError()

    @type_safe
    def list_reports(self) -> List[str]:                            # List available report keys
        raise NotImplementedError()

    @type_safe
    def exists(self, key: str) -> bool:                             # Check if report exists
        raise NotImplementedError()

    @type_safe
    def delete(self, key: str) -> bool:                             # Delete report from storage
        raise NotImplementedError()
