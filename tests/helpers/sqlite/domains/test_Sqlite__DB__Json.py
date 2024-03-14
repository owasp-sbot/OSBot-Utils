from unittest import TestCase

import pytest

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Json import Sqlite__DB__Json
from osbot_utils.helpers.sqlite.models.Sqlite__Field__Type import Sqlite__Field__Type
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import random_string, lower


class test_Sqlite__DB__Json(TestCase):

    def setUp(self):
        self.json_db      = Sqlite__DB__Json()
        self.database     = self.json_db.database
        self.table_create =  self.json_db.table_create
        print()

    def json_data__dict(self):
        class Data_Set(Kwargs_To_Self):
            str_field  : str   = 'an_str'
            int_field  : int   = 42
            bytes_field: bytes = b"some bytes"
        json_data = Data_Set().json()
        assert json_data == {'bytes_field': b"some bytes", 'int_field': 42, 'str_field': 'an_str'}
        return json_data

    def json_data__list_of_dict(self):
        json_data = []
        for i in range(0, 3):
            row = {'an_int': 42, 'an_str': lower(random_string())}
            json_data.append(row)
        return json_data

    def test_create_fields_from_json_data(self):
        json_data = self.json_data__dict()
        self.json_db.create_fields_from_json_data(json_data)

        assert self.table_create.fields__by_name_type() == { 'bytes_field': 'BLOB'   ,
                                                             'id'         : 'INTEGER',
                                                             'int_field'  : 'INTEGER',
                                                             'str_field'  : 'TEXT'   }

    def test_create_table_from_json_data(self):
        self.table_create.fields_reset()
        self.table_create.id_field = False
        assert self.database.tables() == []
        json_data = self.json_data__dict()
        table     = self.json_db.create_table_from_json_data(json_data)
        assert table.exists()               is True
        assert table.rows()                 == [json_data]
        assert self.database.tables_names() == [self.json_db.table_name]

    def test_extract_schema_from_json_data(self):
        json_data__dict                 = self.json_data__dict()
        json_data__list_of_dict         = self.json_data__list_of_dict()
        json_data__dict__schema         = self.json_db.get_schema_from_json_data(json_data__dict        )
        json_data__list_of_dict__schema = self.json_db.get_schema_from_json_data(json_data__list_of_dict)
        assert json_data__dict__schema         == { 'bytes_field': Sqlite__Field__Type.BLOB     ,
                                                    'int_field'  : Sqlite__Field__Type.INTEGER  ,
                                                    'str_field'  : Sqlite__Field__Type.TEXT     }
        assert json_data__list_of_dict__schema == { 'an_int'     : Sqlite__Field__Type.INTEGER  ,
                                                    'an_str'     : Sqlite__Field__Type.TEXT     }

    @pytest.mark.skip
    def test__bug__extract_schema_from_json_data__when_value_has_none(self):
        json_data__list_of_dict = self.json_data__list_of_dict()
        json_data__list_of_dict[1]['an_str'] = None
        pprint(json_data__list_of_dict)
        # this will raise an exception on none
        json_data__list_of_dict__schema = self.json_db.get_schema_from_json_data(json_data__list_of_dict)