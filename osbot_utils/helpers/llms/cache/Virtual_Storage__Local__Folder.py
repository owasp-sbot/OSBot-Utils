from typing                                                         import List, Optional, Dict, Any
from osbot_utils.decorators.methods.cache_on_self                   import cache_on_self
from osbot_utils.helpers.safe_str.Safe_Str__File__Path              import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                     import type_safe
from osbot_utils.utils.Files                                        import current_temp_folder, path_combine_safe, folder_create, file_exists, folder_exists, file_delete, file_name_without_extension, parent_folder, create_folder, files_recursive
from osbot_utils.utils.Json                                         import json_save_file, json_load_file, json_file_load

FOLDER_NAME__CACHE_IN_TEMP_FOLDER = '_llm_requests_cache'
FILE_NAME__CACHE_INDEX            = "cache_index.json"

class Virtual_Storage__Local__Folder(Type_Safe):

    root_folder : Safe_Str__File__Path = None                                       # Base directory for file operations

    def folder__create(self, path_folder) -> None:                                  # Make sure root folder exists
        folder_create(path_folder)

    @type_safe
    def json__load(self, path: Safe_Str__File__Path) -> Optional[Dict[str, Any]]:  # Read JSON from file
        full_path = self.get_full_path(path)
        if file_exists(full_path):
            return json_load_file(path=full_path)
        return None

    @type_safe
    def json__save(self, path: Safe_Str__File__Path,
                         data: dict
                    ) -> bool:                                           # Write JSON to file
        full_path = self.get_full_path(path)
        folder = parent_folder(full_path)
        create_folder(folder)                                         # Ensure parent folder exists
        return json_save_file(data, path=full_path)

    @cache_on_self
    def path_folder__root_cache(self) -> str:  # Get root cache folder path
        if folder_exists(self.root_folder):
            path_cache_folder = self.root_folder
        else:
            path_cache_folder = path_combine_safe(current_temp_folder(), self.root_folder)
            folder_create(path_cache_folder)
        return path_cache_folder

    @type_safe
    def get_full_path(self, path: Safe_Str__File__Path) -> Safe_Str__File__Path:    # Convert relative path to absolute
        base_path = self.path_folder__root_cache()
        full_path = path_combine_safe(base_path, path)
        return Safe_Str__File__Path(full_path)

    @type_safe
    def file__delete(self, path: Safe_Str__File__Path) -> bool:        # Delete a file
        full_path = self.get_full_path(path)
        return file_delete(full_path)

    @type_safe
    def file__exists(self, path: Safe_Str__File__Path) -> bool:       # Check if file exists
        full_path = self.get_full_path(path)
        return file_exists(full_path)

    @type_safe
    def files__all(self) -> List[str]:                            # List all files recursively
        base_path = self.path_folder__root_cache()
        return files_recursive(base_path)

