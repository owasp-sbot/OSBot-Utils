from unittest import TestCase

from osbot_utils.helpers.sqlite.sample_data.Sqlite__Sample_Data__Chinook import Sqlite__Sample_Data__Chinook, \
    FOLDER_NAME__SQLITE_DATA_SETS, FOLDER_NAME__CHINOOK_DATA
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, parent_folder, current_temp_folder, folder_name, file_exists
from osbot_utils.utils.Json import json_loads, json_from_file
from osbot_utils.utils.Misc import list_set


class test_Sqlite__Sample_Data__Chinook(TestCase):

    def setUp(self):
        self.chinook_sqlite = Sqlite__Sample_Data__Chinook()

    def test_chinook_data_as_json(self):
        chinook_data_as_json = self.chinook_sqlite.chinook_data_as_json()
        assert list_set(chinook_data_as_json) == ['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice',
                                                  'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']

    def test_create_table_from_data(self):
        table = self.chinook_sqlite.create_table_from_data()
        assert table.fields() == {'id'   : {'cid': 0, 'name': 'id'   , 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1},
                                  'name' : {'cid': 1, 'name': 'name' , 'type': 'TEXT'   , 'notnull': 0, 'dflt_value': None, 'pk': 0},
                                  'value': {'cid': 2, 'name': 'value', 'type': 'TEXT'   , 'notnull': 0, 'dflt_value': None, 'pk': 0}}

        for row in table.rows():
            name = row.get('name')
            value = row.get('value')
            data = json_loads(value)
            print(f'{name:15} {len(value):10} {len(data):10}')


    def test_load_db_from_disk(self):
        table = self.chinook_sqlite.load_db_from_disk()
        for row in table.rows():
            name = row.get('name')
            value = row.get('value')
            data = json_loads(value)
            print(f'{name:15} {len(value):10} {len(data):10}' )

    def test_json_loads_file_from_disk(self):
        path_to_file = self.chinook_sqlite.path_chinook_data_as_json()
        all_data = json_from_file(path_to_file)
        for name, data in all_data.items():
            print(f'{name:15} {len(data):10}')



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