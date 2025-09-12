from typing                                                                       import List, Optional, Dict, Any
from osbot_utils.utils.Files                                                      import path_combine_safe
from osbot_utils.utils.Json                                                       import json_parse, json_dumps
from osbot_utils.decorators.methods.cache_on_self                                 import cache_on_self
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Files                         import Sqlite__DB__Files
from osbot_utils.helpers.llms.cache.Virtual_Storage__Local__Folder                import Virtual_Storage__Local__Folder
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import Safe_Str__File__Path

class Virtual_Storage__Sqlite(Virtual_Storage__Local__Folder):
    db          : Sqlite__DB__Files                                                         # SQLite database for file storage (defaults to an in memory db)
    root_folder : Safe_Str__File__Path = Safe_Str__File__Path("llm-cache/"                )     # Prefix for all stored files

    def folder__create(self, path_folder) -> None:                                          # Folders don't need to be explicitly created in SQLite storage
        pass                                                                                # They're implicitly created when files are added with path prefixes

    def json__load(self, path: Safe_Str__File__Path) -> Optional[Dict[str, Any]]:           # Load JSON data from SQLite
        virtual_path = self.get_virtual_path(path)
        if self.file__exists(path):
            content = self.db.file_contents(virtual_path)
            if content:
                return json_parse(content)
        return None

    def json__save(self, path: Safe_Str__File__Path, data: dict) -> bool:                   # Save JSON data to SQLite
        self.db.delete_file(path)                                                           # todo: figure out a better way to do this, since at the moment we need to delete an existing file, in order to make sure it is updated
        virtual_path = self.get_virtual_path(path)
        content      = json_dumps(data)
        return self.db.add_file(virtual_path, content) is not None

    def get_full_path(self, path: Safe_Str__File__Path) -> Safe_Str__File__Path:    # For SQLite, we don't need physical paths, but we maintain
        return path                                                                 # the same interface for compatibility

    def file__delete(self, path: Safe_Str__File__Path) -> bool:                     # Delete a file from SQLite
        virtual_path = self.get_virtual_path(path)
        return self.db.delete_file(virtual_path)

    def file__exists(self, path: Safe_Str__File__Path) -> bool:                     # Check if file exists in SQLite
        virtual_path = self.get_virtual_path(path)
        return self.db.file_exists(virtual_path)

    # todo: see if need the filter below
    def files__all(self) -> List[str]:                                              # List all files in SQLite
        all_files = self.db.file_names()
        return all_files
        #return [f for f in all_files if f.startswith(self.root_folder)]             # Filter to only include files that start with our root_prefix

    def get_virtual_path(self, path: Safe_Str__File__Path) -> str:                  # Create a virtual path that incorporates the root_folder concept
        if path.startswith(self.root_folder):
            return path
        return path_combine_safe(self.root_folder, path)

    @cache_on_self
    def path_folder__root_cache(self) -> str:                                       # In SQLite storage, this is a virtual concept
        return self.root_folder                                                     # We use the root_folder as the base path for all files

    def clear_all(self) -> bool:                                                    # Clear all stored files in this virtual storage
        for file_path in self.files__all():
            self.db.delete_file(file_path)
        return True

    def stats(self) -> Dict[str, Any]:                                              # Get storage statistics
        total_size = 0
        files = self.files__all()
        for file_path in files:
            file_info = self.db.file(file_path)
            if file_info and 'size' in file_info:
                total_size += file_info['size']

        return { "storage_type"    : "sqlite"       ,
                 "db_path"         : self.db.db_path,
                 "file_count"      : len(files)     ,
                 "total_size_bytes": total_size     }