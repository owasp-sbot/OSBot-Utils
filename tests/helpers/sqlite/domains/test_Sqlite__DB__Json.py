from unittest import TestCase

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Json import Sqlite__DB__Json
from osbot_utils.utils.Dev import pprint

class test_Sqlite__DB__Json(TestCase):

    def setUp(self):
        self.json_db      = Sqlite__DB__Json()
        self.table_create =  self.json_db.table_create
        print()

    def test_load_data(self):
        class Data_Set(Kwargs_To_Self):
            str_field  : str   = 'an_str'
            int_field  : int   = 42
            bytes_field: bytes = b"some bytes"

        json_data = Data_Set().json()

        assert json_data == {'bytes_field': b"some bytes", 'int_field': 42, 'str_field': 'an_str'}

        self.json_db.create_fields_from_json_data(json_data)

        assert self.table_create.fields__by_name_type() == { 'bytes_field': 'BLOB'   ,
                                                        'id'         : 'INTEGER',
                                                        'int_field'  : 'INTEGER',
                                                        'str_field'  : 'TEXT'   }
        assert self.table_create.table.exists() is False

        assert self.json_db.database.tables() == []
        self.table_create.create_table()
        assert self.table_create.table.exists() is True
        assert self.json_db.database.tables_names() == [self.json_db.table_name]
