from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.helpers.sqlite.Sqlite__Table__Create import Sqlite__Table__Create


class Sqlite__DB__Json(Kwargs_To_Self):
    database     : Sqlite__Database
    table_create : Sqlite__Table__Create
    table_name   : str                    = 'new_db_table'

    def __init__(self):
        super().__init__()
        self.table_create = Sqlite__Table__Create(self.table_name)

    def create_fields_from_json_data(self, json_data):
        self.table_create.table.database = self.database
        for key,value in json_data.items():
            self.table_create.add_field_with_type(key, type(value))


