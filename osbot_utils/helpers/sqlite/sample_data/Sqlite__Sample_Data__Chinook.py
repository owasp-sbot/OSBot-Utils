from osbot_utils.testing.Duration import duration, Duration
from osbot_utils.utils.Files import current_temp_folder, path_combine, folder_create, file_exists, file_not_exists, \
    file_contents
from osbot_utils.utils.Http import GET, GET_to_file
from osbot_utils.utils.Json import json_loads, json_from_file

URL__CHINOOK_JSON             = 'https://github.com/lerocha/chinook-database/releases/download/v1.4.5/ChinookData.json'
FILE_NAME__CHINOOK_DATA_JSON  = 'ChinookData.json'
FOLDER_NAME__CHINOOK_DATA     = 'chinook_data'
FOLDER_NAME__SQLITE_DATA_SETS = '_sqlite_data_sets'

class Sqlite__Sample_Data__Chinook():
    url_chinook_database_json : str = URL__CHINOOK_JSON
    def __init__(self):
        pass

    @duration
    def chinook_data_as_json(self):
        self.download_chinook_data__from_url()
        return self.load_chinook_data__from_disk()

    @duration
    def download_chinook_data__from_url(self, force_download=False):
        path_chinook_data_as_json = self.path_chinook_data_as_json()
        if force_download or file_not_exists(path_chinook_data_as_json):
            GET_to_file(self.url_chinook_database_json, path_chinook_data_as_json)
        return path_chinook_data_as_json

    @duration
    def load_chinook_data__from_disk(self):
        path_chinook_data_as_json = self.path_chinook_data_as_json()
        #return json_from_file(path_chinook_data_as_json)
        with Duration(prefix='load from disk'):
            json_data = file_contents(path_chinook_data_as_json)
        with Duration(prefix='parse json'):
            data = json_loads(json_data)
        return data
    def path_chinook_data_as_json(self):
        return path_combine(self.path_chinook_data(), FILE_NAME__CHINOOK_DATA_JSON)

    def path_chinook_data(self):
        path_chinook_data = path_combine(self.path_sqlite_sample_data_sets(), FOLDER_NAME__CHINOOK_DATA)
        return folder_create(path_chinook_data)

    def path_sqlite_sample_data_sets(self):         # todo: refactor to sqlite_sample_data_sets helper class
        path_data_sets = path_combine(current_temp_folder(), FOLDER_NAME__SQLITE_DATA_SETS)
        return folder_create(path_data_sets)