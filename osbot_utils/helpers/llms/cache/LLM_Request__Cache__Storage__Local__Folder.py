from typing                                                         import List, Optional
from osbot_utils.decorators.methods.cache_on_self                   import cache_on_self
from osbot_utils.helpers.llms.schemas.Schema__LLM_Cache__Index      import Schema__LLM_Cache__Index
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response__Cache   import Schema__LLM_Response__Cache
from osbot_utils.helpers.safe_str.Safe_Str__File__Path              import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                     import type_safe
from osbot_utils.helpers.Obj_Id                                     import Obj_Id, is_obj_id
from osbot_utils.utils.Files                                        import current_temp_folder, path_combine_safe, folder_create, file_exists, folder_exists, file_delete, file_name_without_extension, parent_folder, create_folder, files_recursive
from osbot_utils.utils.Json                                         import json_save_file, json_load_file, json_file_load

FOLDER_NAME__CACHE_IN_TEMP_FOLDER = '_llm_requests_cache'
FILE_NAME__CACHE_INDEX            = "cache_index.json"

class LLM_Request__Cache__Storage__Local__Folder(Type_Safe):

    root_folder     : Safe_Str__File__Path  = Safe_Str__File__Path(FOLDER_NAME__CACHE_IN_TEMP_FOLDER)
    index_file_name : str                   = FILE_NAME__CACHE_INDEX

    @type_safe
    def delete__cache_entry(self, file_path : Safe_Str__File__Path) -> bool: # Delete cache entry from storage
        return file_delete(self.path_file__cache_entry(file_path))

    def delete__cache_index(self):
        index_path = self.path_file__cache_index()
        return file_delete(index_path)

    @type_safe
    def exists__cache_entry(self,file_path : Safe_Str__File__Path) -> bool: # Check if cache entry exists
        return file_exists(self.path_file__cache_entry(file_path))

    def exists__cache_index(self):
        path_cache_index = self.path_file__cache_index()
        return file_exists(path_cache_index)

    @type_safe
    def load__cache_entry(self, file_path : Safe_Str__File__Path) -> Optional[Schema__LLM_Response__Cache]:                 # Load cache entry from storage
        path_entry = self.path_file__cache_entry(file_path)
        if file_exists(path=path_entry):
            json_data   = json_load_file(path=path_entry)
            cache_entry = Schema__LLM_Response__Cache.from_json(json_data)
            return cache_entry
        return None

    def load__cache_index(self) -> Optional[Schema__LLM_Cache__Index]:                                                         # Load cache index data
        path_cache_index = self.path_file__cache_index()
        if file_exists(path_cache_index):
            json_data = json_file_load(path=path_cache_index)       # get the data
            return Schema__LLM_Cache__Index.from_json(json_data)    # and load it as cache_index
        return None

    @cache_on_self
    def path_folder__root_cache(self) -> str:                                                       # Get root cache folder path
        if folder_exists(self.root_folder):
            path_cache_folder = self.root_folder
        else:
            path_cache_folder = path_combine_safe(current_temp_folder(), self.root_folder)
            folder_create(path_cache_folder)
        return path_cache_folder

    @cache_on_self
    def path_file__cache_index(self) -> Safe_Str__File__Path:                                       # Get path to cache index file
        path = path_combine_safe(self.path_folder__root_cache(), self.index_file_name)
        return Safe_Str__File__Path(path)

    @type_safe
    def path_file__cache_entry(self, file_path : Safe_Str__File__Path) -> Safe_Str__File__Path:     # Get full path to cache entry file
        path = path_combine_safe(self.path_folder__root_cache(), file_path)
        return Safe_Str__File__Path(path)

    def reload__cache_id_to_file_path(self) -> List[Obj_Id]:                # todo: check the performance impact of this (and if we really need this method)                                    # Get all cache IDs from disk
        all_files_paths         = files_recursive(self.path_folder__root_cache())
        path_root               = self.path_folder__root_cache()
        cache_id__to__file_path = {}
        for full_file_path in all_files_paths:
            file_path = full_file_path.replace(path_root, '')[1:]
            cache_id = file_name_without_extension(full_file_path)
            if is_obj_id(cache_id):
                cache_id__to__file_path[cache_id] = file_path
        return cache_id__to__file_path
    
    @type_safe
    def save__cache_index(self, cache_index : Schema__LLM_Cache__Index) -> bool:                           # Save cache index data
        json_data =  cache_index.json()
        return json_save_file(json_data, path=self.path_file__cache_index())

    @type_safe
    def save__cache_entry(self,file_path   : Safe_Str__File__Path,
                               cache_entry : Schema__LLM_Response__Cache
                          ) -> bool:                                                        # Save cache entry to storage
        full_file_path        = path_combine_safe(self.path_folder__root_cache(), file_path)
        folder_full_file_path = parent_folder(full_file_path)
        json_data             = cache_entry.json()
        create_folder(folder_full_file_path)                                               # Ensure parent folder exists
        return json_save_file(json_data, path=full_file_path)
