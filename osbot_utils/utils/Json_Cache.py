from osbot_utils.utils.Files import path_combine, folder_create, file_delete, file_exists
from osbot_utils.utils.Json import json_save_file_gz, json_save_file, json_load_file_gz, json_load_file
from osbot_utils.utils.Str import str_safe

PATH_TEMP_FOLDER = '/tmp/json_cache'

class Json_Cache:

    def __init__(self, cache_type=None, cache_keys=None):
        self.cache_type      = cache_type or '__cache'
        self.cache_keys      = cache_keys or [self.cache_type]
        self.path_tmp_folder = PATH_TEMP_FOLDER
        self.save_as_gz      = True
        if type(self.cache_keys) is not list and type(self.cache_keys) is not tuple:
            self.cache_keys = [self.cache_keys]
        #self.data = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def data(self):
        file_path = self.path_cache_file()
        if self.exists():
            if self.save_as_gz:
                return json_load_file_gz(file_path)
            else:
                return json_load_file(file_path)
        return None

    def delete(self):
        return file_delete(self.path_cache_file())

    def exists(self):
        return file_exists(self.path_cache_file())

    def save(self, data):
        file_path = self.path_cache_file()
        if self.save_as_gz:
            return json_save_file_gz(data, file_path)
        else:
            return json_save_file(data, file_path)

    def path_cache_folder(self):
        path_cache = path_combine(self.path_tmp_folder, self.cache_type)
        folder_create(path_cache)
        return path_cache

    def path_cache_file(self):
        tmp_file_name = ""#str_safe(str(self.cache_type))
        for cache_key in  self.cache_keys:
            tmp_file_name += f"--{str_safe(str(cache_key))}"
        tmp_file_name += ".json"
        if self.save_as_gz:
            tmp_file_name += ".gz"
        file_path = path_combine(self.path_cache_folder(), tmp_file_name)
        return file_path