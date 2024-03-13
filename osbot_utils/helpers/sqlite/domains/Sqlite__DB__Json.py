from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.helpers.sqlite.Sqlite__Table__Create import Sqlite__Table__Create


class Sqlite__DB__Json(Kwargs_To_Self):
    database: Sqlite__Database

    def json_data_convert_to_sqlite_fields(self, json_data):
        if type(json_data) is dict:
            return self.json_data_convert_to_sqlite_fields__dict(json_data)

    def json_data_convert_to_sqlite_fields__dict(self, json_data):
        create_table = Sqlite__Table__Create('new_table')
        sqlite_fields = []
        for key,value in json_data.items():
            if type(value) is str:
                create_table.add_field__text(key)
                #print(key,type(value))
        return create_table.locked()