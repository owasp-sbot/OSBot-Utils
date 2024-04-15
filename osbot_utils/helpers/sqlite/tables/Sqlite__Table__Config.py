from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.sqlite.Sqlite__Table   import Sqlite__Table
from osbot_utils.utils.Objects                  import pickle_save_to_bytes, pickle_load_from_bytes

SQLITE__TABLE_NAME__CONFIG = 'config'

class Schema__Table__Config(Kwargs_To_Self):
    key  : str
    value: bytes

class Sqlite__Table__Config(Sqlite__Table):
    def __init__(self, **kwargs):
        self.table_name = SQLITE__TABLE_NAME__CONFIG
        self.row_schema  = Schema__Table__Config
        super().__init__(**kwargs)

    def config_data(self):
        config_data = {}
        for row in self.rows():
            key, value = self.deserialize_row(row)
            config_data[key] = value
        return config_data

    @cache_on_self
    def data(self):
        return self.config_data()

    def deserialize_row(self, row):
        if row:
            key           = row.get('key')
            pickled_value = row.get('value')
            value         = pickle_load_from_bytes(pickled_value)
            return key, value
        return None, None

    def set_config_data(self, config_data: dict):
        self.clear()
        for key,value in config_data.items():
            self.set_value(key=key, value=value)
        self.commit()

    def set_value(self, key, value):
        if self.not_contains(key=key):
            pickled_value = pickle_save_to_bytes(value)
            return self.add_row_and_commit(key=key, value=pickled_value)
        return self.update_value(key,value)

    def update_value(self, key, value):
        pickled_value = pickle_save_to_bytes(value)
        self.row_update(dict(key=key, value=pickled_value), dict(key=key))

    def setup(self):
        if self.exists() is False:
            self.create()
            self.index_create('key')
        return self

    def value(self, key):
        row = self.where_one(key=key)
        key, value = self.deserialize_row(row)
        return value

