import os
from datetime                                                       import datetime, UTC
from typing                                                         import Optional, List, Dict, Tuple
from osbot_utils.decorators.methods.cache_on_self                   import cache_on_self
from osbot_utils.helpers.Obj_Id                                     import Obj_Id, is_obj_id
from osbot_utils.helpers.Safe_Id                                    import Safe_Id
from osbot_utils.helpers.Timestamp_Now import Timestamp_Now
from osbot_utils.helpers.llms.cache.LLM_Cache__Path_Generator       import LLM_Cache__Path_Generator
from osbot_utils.helpers.llms.cache.LLM_Request__Cache              import LLM_Request__Cache
from osbot_utils.helpers.llms.schemas.Schema__LLM_Cache__Index      import Schema__LLM_Cache__Index
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request           import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response          import Schema__LLM_Response
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response__Cache   import Schema__LLM_Response__Cache
from osbot_utils.helpers.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
from osbot_utils.type_safe.decorators.type_safe                     import type_safe
from osbot_utils.utils.Files import current_temp_folder, path_combine_safe, folder_create, file_exists, folder_exists, \
    file_delete, files_names_in_folder, create_folder, parent_folder, files_recursive, files_names, \
    files_names_without_extension, file_name_without_extension
from osbot_utils.utils.Json                                         import json_file_load, json_file_save

FOLDER_NAME__CACHE_IN_TEMP_FOLDER = '_llm_requests_cache'
FILE_NAME__CACHE_INDEX            = "cache_index.json"

class LLM_Request__Cache__Local_Folder(LLM_Request__Cache):
    root_folder   : str                       = FOLDER_NAME__CACHE_IN_TEMP_FOLDER                    # Root folder for cache storage
    path_generator: LLM_Cache__Path_Generator

    def save(self) -> bool:                                                                 # Save cache index to disk
        path_file__cache_index  = self.path_file__cache_index()
        json_data               = self.cache_index.json()
        json_file_save(path=path_file__cache_index, python_object=json_data)
        return True

    def setup(self) -> 'LLM_Request__Cache__Local_Folder':                                  # Load cache from disk
        self.load_or_create()
        return self

    def get_all_cache_ids(self) -> List[Obj_Id]:                                          # Get all cache IDs from disk
        return sorted(self.cache_index.cache_id__to__file_path.keys())

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
    def delete(self, request: Schema__LLM_Request)-> bool:                                      # Delete from cache (overridden) , returns Success status
        request_hash = self.compute_request_hash(request)

        if request_hash not in self.cache_index.cache_id__from__hash__request:
            return False

        cache_id   = self.cache_index.cache_id__from__hash__request[request_hash]
        cache_path = self.path_file__cache_entry(cache_id)

        if file_exists(cache_path):
            file_delete(cache_path)                                                                 # Delete the file

        return super().delete(request)                                                          # Remove from memory and index

    def clear(self) -> bool:                                                                    # Clear all cache entries (overridden)
        for cache_id in self.get_all_cache_ids():                                               # Delete all files
            cache_path = self.path_file__cache_entry(cache_id)
            if file_exists(cache_path):
                file_delete(cache_path)

        index_path = self.path_file__cache_index()                                              # Delete the index file
        if file_exists(index_path):
            file_delete(index_path)

        return super().clear()                                                                  # Clear memory cache

    def load_or_create(self):
        folder_create(self.path_folder__root_cache())                                           # Ensure the root_folder exists
        path_file__cache_index = self.path_file__cache_index()
        if file_exists(path_file__cache_index):                                                 # if cache file exists
            json_data        = json_file_load(path=path_file__cache_index)                      # get the data
            self.cache_index = Schema__LLM_Cache__Index.from_json(json_data)                    # and load it as cache_index
        else:
            self.save()                                                                         # if not save the current cache_index (which should be empty)

    def rebuild_cache_id_to_file_path(self) -> List[Obj_Id]:                # todo: check the performance impact of this (and if we really need this method)                                    # Get all cache IDs from disk
        all_files_paths = files_recursive              (self.path_folder__root_cache())
        path_root = self.path_folder__root_cache()
        cache_id__to__file_path = {}
        for full_file_path in all_files_paths:
            file_path = full_file_path.replace(path_root, '')[1:]
            cache_id = file_name_without_extension(full_file_path)
            if is_obj_id(cache_id):
                cache_id__to__file_path[cache_id] = file_path

        self.cache_index.cache_id__to__file_path = cache_id__to__file_path  # assign the new cache_id__to__file_path
        return cache_id__to__file_path


    def rebuild_index(self) -> bool:                                                            # Rebuild index from disk files
        self.cache_index   = Schema__LLM_Cache__Index()                                         # Create new empty index
        self.cache_entries = {}
        self.rebuild_cache_id_to_file_path()                                                    # rebuild the cache_id_to_file_path (needed so that we can find the files from its cache_ids)
        for cache_id in self.get_all_cache_ids():                                               # Load all cache entries
            cache_entry = self.load_cache_entry(cache_id)

            if cache_entry:
                request = cache_entry.llm_request

                hash_request   = self.compute_request_hash(request)                             # Recompute hashes since in case they are not be stored in the cache entry
                messages_hash  = self.compute_messages_hash(request)                            # todo: see if we really need to recompute these hashes

                if messages_hash not in self.cache_index.cache_ids__from__hash__request__messages:
                    self.cache_index.cache_ids__from__hash__request__messages[messages_hash] = set()

                self.cache_index.cache_id__from__hash__request[hash_request] = cache_id       # Update the index
                self.cache_index.cache_ids__from__hash__request__messages[messages_hash].add(cache_id)

        return self.save()

    def stats(self) -> Dict:                                                               # Cache statistics (overridden)
        stats = super().stats()
        total_size = 0                                                                      # Add disk-specific stats

        # Add index file size
        index_path = self.path_file__cache_index()
        if file_exists(index_path):
            total_size += os.path.getsize(index_path)

        # Add cache entry files size
        for cache_id in self.get_all_cache_ids():
            cache_path = self.path_file__cache_entry(cache_id)
            if file_exists(cache_path):
                total_size += os.path.getsize(cache_path)

        stats["total_size_bytes"] = total_size
        stats["root_folder"     ] = self.path_folder__root_cache()
        stats["cache_files"     ] = len(self.get_all_cache_ids())
        
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
        file_path      = self.cache_id__to__file_path(cache_id)
        if file_path:
            full_file_path = path_combine_safe(self.path_folder__root_cache(), file_path)
            return full_file_path

    @type_safe
    def cache_id__to__file_path(self, cache_id: Obj_Id) -> str:
        return self.cache_index.cache_id__to__file_path.get(cache_id)

    # todo: refactor this to not use a tuple return value (which is never a good thing)
    @type_safe
    def extract_request_domains_areas(self, request: Schema__LLM_Request) -> Tuple[List[Safe_Id], List[Safe_Id]]: # Extract organizational information from a request.
        domains = []
        areas   = []

        if request and request.request_data:                                                                        # Provider as domain
            if request.request_data.provider:
                domains.append(Safe_Id(request.request_data.provider))

            if request.request_data.platform:                                                                       # Platform as domain
                domains.append(Safe_Id(request.request_data.platform))

            # Model as area
            if request.request_data.model:
                areas.append(Safe_Id(request.request_data.model))

        return domains, areas

    @type_safe
    def path_for_temporal_entry(self, cache_id  : Obj_Id              ,
                                      date_time : datetime      = None,
                                      domains   : List[Safe_Id] = None,
                                      areas     : List[Safe_Id] = None
                                 ) -> Safe_Str__File__Path:                                          # Generate a time-based path for a cache entry
        date_time = date_time or datetime.now()
        path      = self.path_generator.from_date_time(date_time = date_time,
                                                       domains   = domains,
                                                       areas     = areas,
                                                       file_id   = Safe_Id(cache_id),
                                                       extension = "json")
        return path

    @type_safe
    def add(self, request  : Schema__LLM_Request,
                  response : Schema__LLM_Response,
                  now      : datetime = None
             ) -> Obj_Id:                                                                   # Save an LLM request/response pair using temporal organization.

        cache_id       = super().add(request, response)                                     # First use standard add() to handle in-memory caching
        cache_entry    = self.cache_entries[cache_id]                                       # get the cache entry (which will exist since it was added on super().add(request, response)  )
        domains, areas = self.extract_request_domains_areas(request)                        # Extract domains and areas for organization
        date_time      = now or datetime.now(UTC)

        file_path = self.path_for_temporal_entry(cache_id   = cache_id ,                    # Generate file path and save
                                                     date_time  = date_time,
                                                     domains    = domains  ,
                                                     areas      = areas    )
        self.cache_index.cache_id__to__file_path[cache_id] = file_path

        # todo: move this to a separate method
        full_file_path        = path_combine_safe(self.path_folder__root_cache(), file_path)
        folder_full_file_path = parent_folder   (full_file_path)
        create_folder (folder_full_file_path)                                                   # Ensure parent folder exists
        json_file_save(cache_entry.json(), path=full_file_path)                                 # Save file to temporal path

        self.save()     # save the cache to disk
        return cache_id

    # todo: see if we need this, since we should create an MGraph with this data (also self.cache_index.cache_id__to__file_path kinda have this data)
    @type_safe
    def get_from__date_time(self,date_time: datetime,
                                domains   : List[Safe_Id] = None,
                                areas     : List[Safe_Id] = None) -> List[Schema__LLM_Response__Cache]:     # Get all cache entries from a specific date/time.

        folder_path      = self.path_generator.from_date_time(date_time = date_time,                        # Generate the folder path pattern for the date/time
                                                              domains   = domains  ,
                                                              areas     = areas    )
        full_folder_path = path_combine_safe(self.path_folder__root_cache(), folder_path)


        if not folder_exists(full_folder_path):                                                             # Check if folder exists
            return []


        results = []                                                                                        # Find all cache files in this folder and subfolders
        # todo: refactor using osbot_utils files methods
        def collect_entries(directory):                                                                     # Function to collect entries recursively
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    collect_entries(item_path)
                elif item.endswith('.json') and item != FILE_NAME__CACHE_INDEX:
                    cache_id_str = os.path.splitext(os.path.basename(item_path))[0]
                    if is_obj_id(cache_id_str):
                        cache_id = Obj_Id(cache_id_str)
                        cache_entry = self.get_cache_entry(cache_id)
                        if cache_entry:
                            results.append(cache_entry)

        collect_entries(full_folder_path)
        return results

    @type_safe
    def get_from__now(self,domains: List[Safe_Id] = None,
                           areas   : List[Safe_Id] = None,
                           now     : datetime      = None
                      ) -> List[Schema__LLM_Response__Cache]:    # Get all cache entries from current time or specified time.
        timestamp = now or datetime.now()
        return self.get_from__date_time(date_time = timestamp,
                                        domains   = domains  ,
                                        areas     = areas    )