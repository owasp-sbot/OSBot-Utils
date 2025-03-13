from datetime                                                                   import datetime, UTC
from typing                                                                     import Optional, List
from osbot_utils.decorators.methods.cache_on_self                               import cache_on_self
from osbot_utils.helpers.Obj_Id                                                 import Obj_Id
from osbot_utils.helpers.Safe_Id                                                import Safe_Id
from osbot_utils.helpers.llms.cache.LLM_Cache__Path_Generator                   import LLM_Cache__Path_Generator
from osbot_utils.helpers.llms.cache.LLM_Request__Cache                          import LLM_Request__Cache
from osbot_utils.helpers.llms.cache.LLM_Request__Cache__Storage                 import LLM_Request__Cache__Storage
from osbot_utils.helpers.llms.cache.Virtual_Storage__Local__Folder              import Virtual_Storage__Local__Folder
from osbot_utils.helpers.llms.schemas.Schema__LLM_Cache__Index                  import Schema__LLM_Cache__Index
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request                       import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                      import Schema__LLM_Response
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response__Cache               import Schema__LLM_Response__Cache
from osbot_utils.helpers.safe_str.Safe_Str__File__Path                          import Safe_Str__File__Path
from osbot_utils.type_safe.decorators.type_safe                                 import type_safe

class LLM_Request__Cache__File_System(LLM_Request__Cache):
    virtual_storage: Virtual_Storage__Local__Folder    
    path_generator : LLM_Cache__Path_Generator
    shared_domains : List[Safe_Id]
    shared_areas   : List[Safe_Id]
    
    @cache_on_self
    def storage(self):
        return LLM_Request__Cache__Storage(virtual_storage=self.virtual_storage)
    
    def save(self) -> bool:                                                                 # Save cache index to disk
        self.storage().save__cache_index(cache_index=self.cache_index)
        return True

    def setup(self) -> 'LLM_Request__Cache__File_System':                                  # Load cache from disk
        self.load_or_create()
        return self

    def get_all_cache_ids(self) -> List[Obj_Id]:                                          # Get all cache IDs from disk
        return sorted(self.cache_index.cache_id__to__file_path.keys())

    def load_cache_entry(self, cache_id: Obj_Id) -> Optional[Schema__LLM_Response__Cache]: # Load cache entry from disk
        cache_path  = self.path_file__cache_entry(cache_id)
        cache_entry = self.storage().load__cache_entry(cache_path)
        if cache_entry:
            self.cache_entries[cache_id] = cache_entry
            return cache_entry
        return None

    def get__cache_entry__from__cache_id(self, cache_id: Obj_Id) -> Optional[Schema__LLM_Response__Cache]:   # Get cache entry by ID (overridden)
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

        self.storage().delete__cache_entry(cache_path)                                             # Delete the file

        return super().delete(request)                                                          # Remove from memory and index

    def clear(self) -> bool:                                                                    # Clear all cache entries (overridden)
        for cache_id in self.get_all_cache_ids():                                               # Delete all files
            cache_path = self.path_file__cache_entry(cache_id)
            self.storage().delete__cache_entry(cache_path)

        self.storage().delete__cache_index()

        return super().clear()                                                                  # Clear memory cache

    def load_or_create(self):
        if self.storage().exists__cache_index():                                                  # if cache file exists
            self.cache_index = self.storage().load__cache_index()                                 # load it
        else:
            self.save()                                                                         # if not save the current cache_index (which should be empty)

    def rebuild_cache_id_to_file_path(self) -> List[Obj_Id]:                # todo: check the performance impact of this (and if we really need this method)                                    # Get all cache IDs from disk
        self.cache_index.cache_id__to__file_path = self.storage().reload__cache_id_to_file_path()  # assign the new cache_id__to__file_path
        return self


    def rebuild_index(self) -> bool:                                                            # Rebuild index from disk files
        self.cache_index   = Schema__LLM_Cache__Index()                                         # Create new empty index
        self.cache_entries = {}
        self.rebuild_cache_id_to_file_path()                                                    # rebuild the cache_id_to_file_path (needed so that we can find the files from its cache_ids)
        for cache_id in self.get_all_cache_ids():                                               # Load all cache entries
            cache_entry = self.load_cache_entry(cache_id)
            if cache_entry:
                request       = cache_entry.llm__request
                hash_request  = cache_entry.request__hash
                if hash_request is None:                                                        # if hash_request doesn't exist     # todo: see if this a valid scenario
                    hash_request  = self.compute_request_hash(request)                          #   recompute hash_request
                self.cache_index.cache_id__from__hash__request[hash_request] = cache_id         # Update the index

        return self.save()

    # def stats(self) -> Dict:                                                               # Cache statistics (overridden)
    #     stats = super().stats()
    #     total_size = 0                                                                      # Add disk-specific stats
    #
    #     # Add index file size
    #     index_path = self.path_file__cache_index()
    #     if file_exists(index_path):
    #         total_size += os.path.getsize(index_path)
    #
    #     # Add cache entry files size
    #     for cache_id in self.get_all_cache_ids():
    #         cache_path = self.path_file__cache_entry(cache_id)
    #         if file_exists(cache_path):
    #             total_size += os.path.getsize(cache_path)
    #
    #     stats["total_size_bytes"] = total_size
    #     #stats["root_folder"     ] = self.path_folder__root_cache()
    #     stats["cache_files"     ] = len(self.get_all_cache_ids())
    #
    #     return stats

    # @cache_on_self
    # def path_folder__root_cache(self):                                                     # Get root cache folder path
    #     if folder_exists(self.root_folder):                                                # If cache_folder is a folder that exists
    #         path_cache_folder = self.root_folder                                           #   Then use it
    #     else:                                                                              # If not
    #         path_cache_folder = path_combine_safe(current_temp_folder(), self.root_folder) #   Combine with temp folder
    #         folder_create(path_cache_folder)                                               #   Make sure it exists
    #     return path_cache_folder
    #
    # def path_file__cache_index(self):                                                      # Get path to cache index file
    #     return path_combine_safe(self.path_folder__root_cache(), FILE_NAME__CACHE_INDEX)
    #
    def path_file__cache_entry(self, cache_id: Obj_Id) -> str:                             # Get path to cache entry file
        file_path      = self.cache_id__to__file_path(cache_id)
        return file_path
    #     if file_path:
    #         full_file_path = path_combine_safe(self.path_folder__root_cache(), file_path)
    #         return full_file_path

    @type_safe
    def cache_id__to__file_path(self, cache_id: Obj_Id) -> str:
        return self.cache_index.cache_id__to__file_path.get(cache_id)

    @type_safe
    def extract_domains_from_request(self, request: Schema__LLM_Request) -> List[Safe_Id]:                          # Extract organizational information from a request.
        domains = []
        if request and request.request_data:
            if request.request_data.model:                                                                          # first add the model (if exists)
                domains.append(Safe_Id(request.request_data.model))
            if request.request_data.provider:                                                                       # then add the provider (if exists)
                domains.append(Safe_Id(request.request_data.provider))
            if request.request_data.platform:                                                                       # finally add the platform (if exists)
                domains.append(Safe_Id(request.request_data.platform))

        return domains

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
    def add(self, request  : Schema__LLM_Request ,
                  response : Schema__LLM_Response,
                  duration : float    = None     ,
                  payload  : dict     = None     ,
                  now      : datetime = None

             ) -> Obj_Id:                                                                           # Save an LLM request/response pair using temporal organization.

        cache_id        = super().add(request=request, response=response, payload=payload, duration=duration)                                            # First use standard add() to handle in-memory caching
        cache_entry     = self.cache_entries[cache_id]                                              # get the cache entry (which will exist since it was added on super().add(request, response)  )
        request_domains = self.extract_domains_from_request(request)                                # Extract domains and areas for organization
        domains         = self.shared_domains + request_domains
        areas           = self.shared_areas
        date_time       = now or datetime.now(UTC)

        file_path       = self.path_for_temporal_entry(cache_id   = cache_id ,                      # Generate file path and save
                                                           date_time  = date_time,
                                                           domains    = domains  ,
                                                           areas      = areas    )
        self.cache_index.cache_id__to__file_path[cache_id] = file_path

        self.storage().save__cache_entry(file_path, cache_entry)

        self.save()                                                                         # save the cache to disk
        return cache_id

    # todo: see if we need this, since we should create an MGraph with this data (also self.cache_index.cache_id__to__file_path kinda have this data)
    # @type_safe
    # def get_from__date_time(self,date_time: datetime,
    #                             domains   : List[Safe_Id] = None,
    #                             areas     : List[Safe_Id] = None) -> List[Schema__LLM_Response__Cache]:     # Get all cache entries from a specific date/time.
    #
    #     folder_path      = self.path_generator.from_date_time(date_time = date_time,                        # Generate the folder path pattern for the date/time
    #                                                           domains   = domains  ,
    #                                                           areas     = areas    )
    #     full_folder_path = path_combine_safe(self.path_folder__root_cache(), folder_path)
    #
    #
    #     if not folder_exists(full_folder_path):                                                             # Check if folder exists
    #         return []
    #
    #
    #     results = []                                                                                        # Find all cache files in this folder and subfolders
    #     # todo: refactor using osbot_utils files methods
    #     def collect_entries(directory):                                                                     # Function to collect entries recursively
    #         for item in os.listdir(directory):
    #             item_path = os.path.join(directory, item)
    #             if os.path.isdir(item_path):
    #                 collect_entries(item_path)
    #             elif item.endswith('.json') and item != FILE_NAME__CACHE_INDEX:
    #                 cache_id_str = os.path.splitext(os.path.basename(item_path))[0]
    #                 if is_obj_id(cache_id_str):
    #                     cache_id = Obj_Id(cache_id_str)
    #                     cache_entry = self.get_cache_entry__from__cache_id(cache_id)
    #                     if cache_entry:
    #                         results.append(cache_entry)
    #
    #     collect_entries(full_folder_path)
    #     return results

    # @type_safe
    # def get_from__now(self,domains: List[Safe_Id] = None,
    #                        areas   : List[Safe_Id] = None,
    #                        now     : datetime      = None
    #                   ) -> List[Schema__LLM_Response__Cache]:    # Get all cache entries from current time or specified time.
    #     timestamp = now or datetime.now()
    #     return self.get_from__date_time(date_time = timestamp,
    #                                     domains   = domains  ,
    #                                     areas     = areas    )