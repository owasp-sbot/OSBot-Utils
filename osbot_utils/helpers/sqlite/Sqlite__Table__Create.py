from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Field import Sqlite__Field
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table

class Sqlite__Table__Create(Kwargs_To_Self):
    fields : list[Sqlite__Field]
    table  : Sqlite__Table

    def add_field(self, field_data: dict):
        sqlite_field = Sqlite__Field.from_json(field_data)
        self.fields.append(sqlite_field)