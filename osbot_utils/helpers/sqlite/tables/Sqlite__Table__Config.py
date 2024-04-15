from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import pickle_save_to_bytes

SQLITE__TABLE_NAME__CONFIG = 'config'

class Schema__Table__Config(Kwargs_To_Self):
    key  : str
    value: bytes

class Sqlite__Table__Config(Sqlite__Table):
    def __init__(self):
        self.table_name = SQLITE__TABLE_NAME__CONFIG
        self.row_schema  = Schema__Table__Config
        super().__init__()


    def add_value(self, key, value):
        pickled_value = pickle_save_to_bytes(value)
        return self.add_row(key=key, value=pickled_value)

    def config_data(self):
        return {}

    def set_config_data(self, config_data: dict):
        self.clear()
        for key,value in config_data.items():
            self.add_value(key=key, value=value)
        self.commit()
