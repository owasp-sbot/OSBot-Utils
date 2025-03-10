import os
from typing                                                         import Optional, List, Dict
from osbot_utils.decorators.methods.cache_on_self                   import cache_on_self
from osbot_utils.helpers.Obj_Id                                     import Obj_Id, is_obj_id
from osbot_utils.helpers.llms.actions.LLM_Request__Cache            import LLM_Request__Cache
from osbot_utils.helpers.llms.schemas.Schema__LLM_Cache__Index      import Schema__LLM_Cache__Index
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request           import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response          import Schema__LLM_Response
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response__Cache   import Schema__LLM_Response__Cache
from osbot_utils.type_safe.decorators.type_safe                     import type_safe
from osbot_utils.utils.Files                                        import current_temp_folder, path_combine_safe, folder_create, file_exists, folder_exists, file_delete, files_names_in_folder
from osbot_utils.utils.Json                                         import json_file_load, json_file_save

FOLDER_NAME__CACHE_IN_TEMP_FOLDER = '_llm_requests_cache'
FILE_NAME__CACHE_INDEX            = "cache_index.json"

class LLM_Request__Cache__Local_Folder(LLM_Request__Cache):
    root_folder : str                = FOLDER_NAME__CACHE_IN_TEMP_FOLDER                    # Root folder for cache storage

    def save(self) -> bool:                                                                # Save cache index to disk
        path_file__cache_index  = self.path_file__cache_index()
        json_data               = self.cache_index.json()
        json_file_save(path=path_file__cache_index, python_object=json_data)
        return True

    def setup(self) -> bool:                                                                # Load cache from disk
        path_file__cache_index = self.path_file__cache_index()
        
        if file_exists(path_file__cache_index):
            try:
                json_data        = json_file_load(path=path_file__cache_index)
                self.cache_index = Schema__LLM_Cache__Index.from_json(json_data)

                #self.load_cache_entries()                                                  # Load cache entries from disk
                return True
            except Exception as e:
                print(f"Error loading cache index: {e}")
                return False
        return True

    # def load_cache_entries(self) -> None:                                                 # Load all cache entries from disk
    #     for cache_id in self.get_all_cache_ids():
    #         self.load_cache_entry(cache_id)
    #
    def get_all_cache_ids(self) -> List[Obj_Id]:                                          # Get all cache IDs from disk
        file_names = files_names_in_folder(self.path_folder__root_cache())
        cache_ids  = []
        for file_name in file_names:
            if is_obj_id(file_name):
                cache_ids.append(Obj_Id(file_name))

        return cache_ids

    def load_cache_entry(self, cache_id: Obj_Id) -> Optional[Schema__LLM_Response__Cache]: # Load cache entry from disk
        cache_path = self.path_file__cache_entry(cache_id)

        if file_exists(cache_path):
            cache_data  = json_file_load(cache_path)
            cache_entry = Schema__LLM_Response__Cache.from_json(cache_data)
            self.cache_entries[cache_id] = cache_entry
            return cache_entry
        return None

    def get_cache_entry(self, cache_id: Obj_Id) -> Optional[Schema__LLM_Response__Cache]:   # Get cache entry by ID (overridden)
        if cache_id in self.cache_entries:                                                  # Check memory first
            return self.cache_entries[cache_id]
        return self.load_cache_entry(cache_id)                                              # Load from disk if not in memory

    @type_safe
    def add(self, request     : Schema__LLM_Request ,                                       # Add to cache (overridden)
                  response    : Schema__LLM_Response                                        # Response to store
             ) -> bool:                                                                     # Success status

        result = super().add(request, response)
        
        if result:
            cache_id    = self.cache_index.hash__request[request.request_cache.hash__request]   # Save the cache entry to disk
            cache_entry = self.cache_entries[cache_id]
            cache_path  = self.path_file__cache_entry(cache_id)
            json_file_save(cache_path, cache_entry.json())
        
        return result

    @type_safe
    def delete(self, request: Schema__LLM_Request)-> bool:                                      # Delete from cache (overridden) , returns Success status
        request_hash = self.compute_request_hash(request)
        
        if request_hash not in self.cache_index.hash__request:
            return False
        
        cache_id   = self.cache_index.hash__request[request_hash]
        cache_path = self.path_file__cache_entry(cache_id)

        file_delete(cache_path)                                                                 # Delete the file

        return super().delete(request)                                                          # Remove from memory and index

    def clear(self) -> bool:                                                                    # Clear all cache entries (overridden)
        for cache_id in self.get_all_cache_ids():                                               # Delete all files
            cache_path = self.path_file__cache_entry(cache_id)
            file_delete(cache_path)
        return super().clear()                                                                  # Clear memory cache

    def rebuild_index(self) -> bool:                                                            # Rebuild index from disk files
        self.cache_index   = Schema__LLM_Cache__Index()                                     # Create new empty index
        self.cache_entries = {}

        for cache_id in self.get_all_cache_ids():                                           # Load all cache entries
            cache_entry = self.load_cache_entry(cache_id)

            if cache_entry:
                request       = cache_entry.llm_request
                request_hash  = request.request_cache.hash__request
                messages_hash = request.request_cache.hash__request__messages

                if messages_hash not in self.cache_index.hash__request__messages:
                    self.cache_index.hash__request__messages[messages_hash] = set()

                self.cache_index.hash__request [request_hash ] = cache_entry.cache_id       # Update the index
                self.cache_index.hash__request__messages[messages_hash].add(cache_entry.cache_id)

        return self.save()

    def stats(self) -> Dict:                                                               # Cache statistics (overridden)
        stats = super().stats()
        total_size = 0                                                                      # Add disk-specific stats
        for cache_id in self.get_all_cache_ids():
            cache_path = self.path_file__cache_entry(cache_id)
            if file_exists(cache_path):
                total_size += os.path.getsize(cache_path)
        
        stats["total_size_bytes"] = total_size
        stats["root_folder"     ] = self.path_folder__root_cache()
        
        return stats

    @cache_on_self
    def path_folder__root_cache(self):                                                     # Get root cache folder path
        if folder_exists(self.root_folder):                                                # If cache_folder is a folder that exists
            path_cache_folder = self.root_folder                                           #   Then use it
        else:                                                                              # If not
            path_cache_folder = path_combine_safe(current_temp_folder(), self.root_folder) #   Combine with temp folder
            folder_create(path_cache_folder)                                               #   Make sure it exists
        return path_cache_folder

    def path_file__cache_index(self):                                                      # Get path to cache index file
        return path_combine_safe(self.path_folder__root_cache(), FILE_NAME__CACHE_INDEX)

    def path_file__cache_entry(self, cache_id: Obj_Id) -> str:                             # Get path to cache entry file
        return path_combine_safe(self.path_folder__root_cache(), f"{cache_id}.json")