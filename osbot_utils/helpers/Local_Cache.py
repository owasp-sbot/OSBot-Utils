from osbot_utils.utils.Misc                         import list_set
from osbot_utils.utils.Dev                          import pprint
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.utils.Files                        import current_temp_folder, path_combine, create_folder, safe_file_name, file_exists, file_delete, file_size
from osbot_utils.utils.Json                         import json_save_file, json_load_file

class Local_Cache:

    DEFAULT_CACHES_NAME = "_cache_data"

    def __init__(self, cache_name, caches_name=None):
        self.caches_name = caches_name or Local_Cache.DEFAULT_CACHES_NAME
        self.cache_name = safe_file_name(cache_name)
        self._data      = None

    def add(self, key, value):
        self.data()[key] = value
        self.save()
        return self

    def add_data(self, items):
        data = self.data()
        for key, value in items.items():
            data[key] = value
        self.save()
        return self

    def cache_delete(self):
        return file_delete(self.path_cache_file())

    def cache_exists(self):
        return file_exists(self.path_cache_file())

    def cache_file_size(self):
        return file_size(self.path_cache_file())

    def create(self):
        if not self.cache_exists():
            self.save()
        return self

    def has_key(self, key):
        return key in self.keys()

    def save(self):
        data = self.data() or {}
        json_save_file(data, self.path_cache_file())
        return self

    def data(self):
        if self._data is None:
            self._data = json_load_file(self.path_cache_file())
        return self._data

    def get(self, key, default_value=None):
        return self.data().get(key, default_value)

    def info(self):
        return { 'caches_name'    : self.caches_name       ,
                 'cache_name'     : self.cache_name        ,
                 'path_cache_file': self.path_cache_file() ,
                 'data_keys'      : list_set(self.data())  }

    def name(self):
        return self.cache_name

    def print_info(self):
        pprint(self.info())

    def keys(self):
        return self.data().keys()

    @cache_on_self
    def path_root_folder(self):
        path_root_folder = path_combine(current_temp_folder(), self.caches_name)
        create_folder(path_root_folder)                          # create if it doesn't exist
        return path_root_folder

    @cache_on_self
    def path_cache_file(self):
        return path_combine(self.path_root_folder(), f"{self.cache_name}.json")

    def set(self, key, value):
        return self.add(key, value)

    def set_data(self,items):
        return self.add_data(items)

    def set_all_data(self, data):
        self._data = data
        self.save()
        return self

    def setup(self):
        self.create()
        return self

    def remove(self, key):
        if key in self.keys():
            del self.data()[key]
            self.save()
            return True
        return False

    def values(self):
        return self.data().values()

    def __repr__(self):
        return f"Local_Cache: {self.cache_name}"

    # extra methods alias

    #add = set