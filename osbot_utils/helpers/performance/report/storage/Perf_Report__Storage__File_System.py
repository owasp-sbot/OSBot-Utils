# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Report__Storage__File_System - File system storage backend
# Saves reports to files at {storage_path}/{key}.{format}
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import List
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Json             import Perf_Report__Renderer__Json
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Markdown         import Perf_Report__Renderer__Markdown
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Text             import Perf_Report__Renderer__Text
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report                       import Schema__Perf_Report
from osbot_utils.helpers.performance.report.storage.Perf_Report__Storage__Base                import Perf_Report__Storage__Base
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                import type_safe
from osbot_utils.utils.Files                                                                  import file_create, file_exists, file_contents, folder_create, folder_exists, path_combine
from osbot_utils.utils.Json                                                                   import json_loads


class Perf_Report__Storage__File_System(Perf_Report__Storage__Base): # File system storage backend
    storage_path: str                                               # Root path for report storage

    @type_safe
    def save(self                                 ,                 # Save report to files
             report : Schema__Perf_Report         ,                 # Report to save
             key    : str                         ,                 # Storage key/name
             formats: List[str] = None            ) -> bool:        # Formats to save (txt, md, json)
        if formats is None:
            formats = ['txt', 'md', 'json']

        self.ensure_storage_path()

        renderers = {'txt' : Perf_Report__Renderer__Text()     ,
                     'md'  : Perf_Report__Renderer__Markdown() ,
                     'json': Perf_Report__Renderer__Json()     }

        success = True
        for fmt in formats:
            renderer = renderers.get(fmt)
            if renderer:
                content = renderer.render(report)
                success = self.save_content(key, content, fmt)
            else:
                success = False

        return success

    @type_safe
    def save_content(self                         ,                 # Save rendered content to file
                     key        : str             ,                 # Storage key/name
                     content    : str             ,                 # Rendered content
                     format_type: str             ) -> bool:        # Format type (txt, md, json)
        self.ensure_storage_path()
        file_path = self.get_file_path(key, format_type)
        file_create(file_path, content)
        return file_exists(file_path)

    @type_safe
    def load(self, key: str) -> Schema__Perf_Report:                # Load report from JSON file
        file_path = self.get_file_path(key, 'json')

        if file_exists(file_path) is False:
            return None

        content = file_contents(file_path)
        data    = json_loads(content)

        return Schema__Perf_Report.from_json(data)

    @type_safe
    def list_reports(self) -> List[str]:                            # List available report keys
        import os
        if folder_exists(self.storage_path) is False:
            return []

        keys = set()
        for filename in os.listdir(self.storage_path):
            if '.' in filename:
                key = filename.rsplit('.', 1)[0]
                keys.add(key)

        return sorted(list(keys))

    @type_safe
    def exists(self, key: str) -> bool:                             # Check if report exists
        json_path = self.get_file_path(key, 'json')
        return file_exists(json_path)

    @type_safe
    def delete(self, key: str) -> bool:                             # Delete all report files
        import os
        if folder_exists(self.storage_path) is False:
            return False

        deleted = False
        for ext in ['txt', 'md', 'json']:
            file_path = self.get_file_path(key, ext)
            if file_exists(file_path):
                os.remove(file_path)
                deleted = True

        return deleted

    # ═══════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_file_path(self, key: str, format_type: str) -> str:     # Build full file path
        return path_combine(self.storage_path, f'{key}.{format_type}')

    @type_safe
    def ensure_storage_path(self) -> None:                          # Create storage directory if needed
        if self.storage_path and folder_exists(self.storage_path) is False:
            folder_create(self.storage_path)
