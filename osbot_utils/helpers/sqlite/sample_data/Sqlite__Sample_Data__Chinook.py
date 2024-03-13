from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.helpers.sqlite.Sqlite__Table__Create import Sqlite__Table__Create
from osbot_utils.testing.Duration import duration, Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import current_temp_folder, path_combine, folder_create, file_exists, file_not_exists, \
    file_contents
from osbot_utils.utils.Http import GET, GET_to_file
from osbot_utils.utils.Json import json_loads, json_from_file, json_dump
from osbot_utils.utils.Objects import obj_info

URL__CHINOOK_JSON             = 'https://github.com/lerocha/chinook-database/releases/download/v1.4.5/ChinookData.json'
FILE_NAME__CHINOOK_DATA_JSON  = 'ChinookData.json'
FOLDER_NAME__CHINOOK_DATA     = 'chinook_data'
FOLDER_NAME__SQLITE_DATA_SETS = '_sqlite_data_sets'
PATH__DB__CHINOOK             = '/tmp/db-tests/test-chinook.db'
TABLE_NAME__CHINOOK           = 'chinook_data'
class Sqlite__Sample_Data__Chinook():
    url_chinook_database_json : str = URL__CHINOOK_JSON
    path_local_db             : str = PATH__DB__CHINOOK
    table_name                : str = TABLE_NAME__CHINOOK
    def __init__(self):
        pass

    def chinook_data_as_json(self):
        path_chinook_data_as_json = self.path_chinook_data_as_json()
        if file_not_exists(path_chinook_data_as_json):
            GET_to_file(self.url_chinook_database_json, path_chinook_data_as_json)
        return json_from_file(path_chinook_data_as_json)

    def create_table_from_data(self):
        chinook_data = self.chinook_data_as_json()
        table_creator = Sqlite__Table__Create(table_name=self.table_name)
        table_creator.add_field(dict(name="id", type="INTEGER", pk=True))
        table_creator.add_field(dict(name="name", type="TEXT"))
        table_creator.add_field(dict(name="value", type="TEXT"))
        table_creator.create_table()
        table = table_creator.table
        cursor = table.cursor()
        assert len(chinook_data) == 11
        for key, items in chinook_data.items():
            name = key
            value =json_dump(items)
            cursor.execute(f'INSERT INTO {self.table_name} (name, value) VALUES (?, ?)', (name, value))

        cursor.commit()

        pprint(f'created db size :{table.size()}')
        table.database.save_to(PATH__DB__CHINOOK)
        return table

    def load_db_from_disk(self):
        db_chinook = Sqlite__Database(db_path=PATH__DB__CHINOOK)
        db_chinook.connect()
        return db_chinook.table(self.table_name)

    def path_chinook_data_as_json(self):
        return path_combine(self.path_chinook_data(), FILE_NAME__CHINOOK_DATA_JSON)

    def path_chinook_data(self):
        path_chinook_data = path_combine(self.path_sqlite_sample_data_sets(), FOLDER_NAME__CHINOOK_DATA)
        return folder_create(path_chinook_data)

    def path_sqlite_sample_data_sets(self):         # todo: refactor to sqlite_sample_data_sets helper class
        path_data_sets = path_combine(current_temp_folder(), FOLDER_NAME__SQLITE_DATA_SETS)
        return folder_create(path_data_sets)

