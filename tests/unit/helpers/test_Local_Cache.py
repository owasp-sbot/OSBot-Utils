from unittest import TestCase

from osbot_utils.helpers.Local_Cache import Local_Cache
from osbot_utils.utils.Files import folder_exists, parent_folder, current_temp_folder, file_name, file_exists, \
    folder_name


class test_Local_Cache(TestCase):
    cache       : Local_Cache
    cache_name  : str

    @classmethod
    def setUpClass(cls) -> None:
        cls.cache_name = '_local_cache'
        cls.cache      = Local_Cache(cache_name=cls.cache_name).setup()
        assert cls.cache.cache_exists() is True

    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.cache.cache_delete() is True
        assert cls.cache.cache_exists() is False


    def test__init__(self):
        assert self.cache.cache_name == self.cache_name

    def test_add_data(self):
        assert self.cache.data()                     == {}
        assert self.cache.add_data({'a':1, 'b':2   }) is self.cache
        assert self.cache.data    ()                  == {'a': 1, 'b': 2}
        assert self.cache.add_data({'c': 3, 'd': 4 }) is self.cache
        assert self.cache.data    ()                  == {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        assert self.cache.set_all_data({'e': 5         }) is self.cache
        assert self.cache.data    ()                  == {'e': 5 }

    def test_path_root_folder(self):
        root_folder = self.cache.path_root_folder()
        assert folder_exists(root_folder)
        assert parent_folder(root_folder) == current_temp_folder()
        assert folder_name  (root_folder) == Local_Cache.DEFAULT_CACHES_NAME

    def test_path_cache_file(self):
        path_cache_file = self.cache.path_cache_file()
        assert file_exists  (path_cache_file)
        assert parent_folder(path_cache_file) == self.cache.path_root_folder()
        assert file_name    (path_cache_file) == self.cache.cache_name +  ".json"
