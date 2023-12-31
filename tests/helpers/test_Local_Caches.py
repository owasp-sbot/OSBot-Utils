from unittest                           import TestCase
from osbot_utils.helpers.Local_Caches   import Local_Caches
from osbot_utils.utils.Files            import folder_exists, parent_folder, current_temp_folder, file_name, folder_name
from osbot_utils.utils.Misc             import random_text


class test_Local_Caches(TestCase):
    caches     : Local_Caches
    caches_name: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.caches_name  = random_text('local_cache')
        cls.caches      = Local_Caches(caches_name=cls.caches_name).setup()
        assert cls.caches.exists() is True

    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.caches.delete() is True
        assert cls.caches.exists() is False


    def test__init__(self):
        assert self.caches.caches_name == self.caches_name #Local_Caches.DEFAULT_NAME
        assert self.caches.exists()    is True
        assert self.caches.empty()     is True


    def test_caches(self):
        temp_cache = self.caches.cache('aaaaa')
        caches     = self.caches.caches()
        assert temp_cache.cache_exists() is True
        assert temp_cache.name()   in self.caches.caches()
        #assert temp_cache          in caches.values()
        assert temp_cache.cache_delete() is True
        assert temp_cache.cache_exists() is False

    def test_path_local_caches(self):
        path_local_caches = self.caches.path_local_caches()
        assert folder_exists(path_local_caches)
        assert parent_folder(path_local_caches) == current_temp_folder()
        assert folder_name  (path_local_caches) == self.caches_name