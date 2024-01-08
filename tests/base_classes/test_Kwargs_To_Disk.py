from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Files import current_temp_folder, file_exists, file_name

from osbot_utils.base_classes.Kwargs_To_Disk import Kwargs_To_Disk


class test_Kwargs_To_Disk(TestCase):

    def setUp(self):
        self.kwargs_to_disk = Kwargs_To_Disk()

    def tearDown(self):
        assert self.kwargs_to_disk._cache_delete() is True

    def test__cache_create(self):
        assert self.kwargs_to_disk._cache_delete() is True
        assert self.kwargs_to_disk._cache_exists() is False
        self.kwargs_to_disk._cache_create()
        assert self.kwargs_to_disk._cache_exists() is True

    def test__cache_delete(self):
        assert self.kwargs_to_disk._cache_delete() is True
        assert self.kwargs_to_disk._cache_exists() is False
        self.kwargs_to_disk._cache_create()

    def test__cache_exists(self):
        assert self.kwargs_to_disk._cache_exists() is True

    def test__cache_path_data_file(self):
        expected_parent_folder = current_temp_folder()
        expected_cache_folder  = '_cache_data'
        expected_file_namev    = 'osbot_utils.base_classes.Kwargs_To_Disk___Kwargs_To_Disk.json'
        path_data_file         = self.kwargs_to_disk._cache_path_data_file()

        assert path_data_file              == f'{expected_parent_folder}/{expected_cache_folder}/{expected_file_namev}'
        assert file_exists(path_data_file) is True

    def test___getattr__(self):
        local_cache = self.kwargs_to_disk._local_cache
        assert local_cache.data() == {}

        assert self.kwargs_to_disk.an_var is None                   # confirm that the value is not set
        local_cache.set('an_var', 42)                               # set the value via the cache
        assert self.kwargs_to_disk.an_var is 42                     # confirm that the value is now set

    def test___setattr__(self):
        local_cache = self.kwargs_to_disk._local_cache
        assert local_cache.data() == {}
        assert self.kwargs_to_disk.an_var is None
        self.kwargs_to_disk.an_var = 42
        assert local_cache.data() == {'an_var': 42}
        assert self.kwargs_to_disk.an_var is 42
        local_cache.set('an_var', 'changed')
        assert local_cache.data() == {'an_var': 'changed'}
        assert self.kwargs_to_disk.an_var is 'changed'

    def test__class_that_uses_Kwargs_To_Disk(self):

        class An_Class(Kwargs_To_Disk):
            name : str

        an_class = An_Class()

        #assert an_class.name is None
        assert an_class._cache_exists                  ()  is True
        assert file_name(an_class._cache_path_data_file()) == 'test_Kwargs_To_Disk___An_Class.json'
        assert an_class._cache_delete                  ()  is True
        assert an_class._cache_create                  ()  == an_class._local_cache

        an_class.name = 'some name'
        assert an_class.name            == 'some name'
        assert an_class._cache_data  () == {'name': 'some name'}
        assert an_class._cache_delete() is True