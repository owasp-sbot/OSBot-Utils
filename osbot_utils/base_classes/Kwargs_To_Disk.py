from osbot_utils.helpers.Local_Cache import Local_Cache

class Kwargs_To_Disk:

    def __enter__(self): return self
    def __exit__ (self, exc_type, exc_val, exc_tb): pass

    def __init__(self):
        self._cache_name  = f'{self.__class__.__module__}___{self.__class__.__name__}'
        self._local_cache = Local_Cache(cache_name=self._cache_name).setup()

    def __getattr__(self, key):
        if key.startswith('_'):
            return super().__getattribute__(key)
        return self._local_cache.get(key)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super().__setattr__(key, value)
        else:
            self._local_cache.set(key, value)

    def _cache_create        (self): return self._local_cache.create()
    def _cache_delete        (self): return self._local_cache.cache_delete   ()
    def _cache_data          (self): return self._local_cache.data           ()
    def _cache_exists        (self): return self._local_cache.cache_exists   ()
    def _cache_path_data_file(self): return self._local_cache.path_cache_file()
