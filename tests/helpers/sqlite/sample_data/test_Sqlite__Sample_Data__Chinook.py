from unittest import TestCase

from osbot_utils.helpers.sqlite.sample_data.Sqlite__Sample_Data__Chinook import Sqlite__Sample_Data__Chinook, \
    FOLDER_NAME__SQLITE_DATA_SETS, FOLDER_NAME__CHINOOK_DATA
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, parent_folder, current_temp_folder, folder_name, file_exists
from osbot_utils.utils.Misc import list_set


class test_Sqlite__Sample_Data__Chinook(TestCase):
    def setUp(self):
        self.chinook_sqlite = Sqlite__Sample_Data__Chinook()
        print()

    def test_chinook_data_as_json(self):
        chinook_data_as_json = self.chinook_sqlite.chinook_data_as_json()
        assert list_set(chinook_data_as_json) == ['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice',
                                                  'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']


    def test_download_chinook_data__from_url(self):
        force_download = True
        path_chinook_data_as_json = self.chinook_sqlite.download_chinook_data__from_url(force_download=force_download)
        assert file_exists(path_chinook_data_as_json)

    def test_load_chinook_data__from_disk(self):
        chinook_data = self.chinook_sqlite.load_chinook_data__from_disk()
        assert list_set(chinook_data) == ['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice',
                                          'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']

    def test_path_chinook_data(self):
        path_chinook_data = self.chinook_sqlite.path_chinook_data()
        assert folder_exists(path_chinook_data) is True
        assert parent_folder(path_chinook_data) == self.chinook_sqlite.path_sqlite_sample_data_sets()
        assert folder_name  (path_chinook_data) == FOLDER_NAME__CHINOOK_DATA

    def test_path_sqlite_sample_data_sets(self):
        path_data_sets = self.chinook_sqlite.path_sqlite_sample_data_sets()
        assert folder_exists(path_data_sets) is True
        assert parent_folder(path_data_sets) == current_temp_folder()
        assert folder_name  (path_data_sets) == FOLDER_NAME__SQLITE_DATA_SETS