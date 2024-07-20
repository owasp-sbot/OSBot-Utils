from pathlib import Path
from typing import Dict, List
from osbot_utils.helpers.Local_Cache import Local_Cache
from osbot_utils.utils.Files import current_temp_folder, path_combine, folder_exists, folder_delete, file_extension
from osbot_utils.utils.Misc          import random_text


class Local_Caches:

    DEFAULT_NAME = "_cache_data"                # todo: see if this is still being used

    def __init__(self, caches_name=None):
        self.caches_name = caches_name or random_text("local_caches")

    def caches(self) -> Dict[str, Local_Cache]:
        cache_names = self.existing_cache_names()
        caches = {}
        for cache_name in cache_names:
            caches[cache_name] = self.cache(cache_name)
        return caches

    def delete(self) -> bool:
        for cache_name, cache in self.caches().items():
            cache.cache_delete()
        return folder_delete(self.path_local_caches())

    #
    #@cache_on_self
    def cache(self, cache_name) -> Local_Cache:
        local_cache = Local_Cache(cache_name=cache_name, caches_name=self.caches_name)
        local_cache.setup()
        return local_cache

    def exists(self) -> bool:
        return folder_exists(self.path_local_caches())

    def empty(self) -> bool:
        return len(self.caches()) == 0

    def existing_cache_names(self) -> List[str]:
        cache_names = []
        for f in self.path_local_caches().iterdir():
            if f.is_file():
                if file_extension(f.name) == '.json':
                    cache_name = f.name.replace('.json', '')
                    cache_names.append(cache_name)
        return cache_names

    #@cache_on_self
    def path_local_caches(self) -> Path:
        return Path(path_combine(current_temp_folder(), self.caches_name))

    def setup(self):
        self.path_local_caches().mkdir(parents=True, exist_ok=True)
        return self