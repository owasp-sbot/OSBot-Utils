from unittest import TestCase

import pytest

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Json import Sqlite__DB__Json
from osbot_utils.helpers.sqlite.models.Sqlite__Field__Type import Sqlite__Field__Type
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json import json_dumps, json_round_trip
from osbot_utils.utils.Misc import random_string, lower


class test_Sqlite__DB__Json(TestCase):

    def setUp(self):
        self.json_db      = Sqlite__DB__Json()
        self.database     = self.json_db.database
        self.table_create =  self.json_db.table_create

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

    def test_create_table_from_schema(self):
        dict__table_name                = 'table_from__dict__json_data__schema'
        dict__table__expected_schema    = { 'bytes_field' : 'BLOB'    ,
                                            'id'          : 'INTEGER' ,
                                            'int_field'   : 'INTEGER' ,
                                            'str_field'   : 'TEXT'    }
        dict__json_data                 = self.json_data__dict()
        dict__json_data__schema         = self.json_db.get_schema_from_json_data(dict__json_data)
        dict__table = self.json_db.create_table_from_schema(dict__table_name, dict__json_data__schema)

        list_of_dict__table_name        = 'table_from_list_of_dict__json_data__schema'
        list_of_dict__expected_schema   = { 'an_int'     : 'INTEGER' ,
                                            'an_str'     : 'TEXT'    ,
                                            'id'         : 'INTEGER' }
        list_of_dict__json_data         = self.json_data__list_of_dict()
        list_of_dict__json_data__schema = self.json_db.get_schema_from_json_data(list_of_dict__json_data)
        list_of_dict__table             = self.json_db.create_table_from_schema(list_of_dict__table_name, list_of_dict__json_data__schema)

        assert dict__table.table_name                     == dict__table_name
        assert dict__table.schema__by_name_type()         == dict__table__expected_schema
        assert list_of_dict__table.table_name             == list_of_dict__table_name
        assert list_of_dict__table.schema__by_name_type() == list_of_dict__expected_schema

        round_trip__table_name              = 'round_trip__dict_schema'
        round_trip__json_data__dict__schema = json_round_trip(dict__json_data__schema)
        round_trip__table__table            = self.json_db.create_table_from_schema(round_trip__table_name, round_trip__json_data__dict__schema)

        assert round_trip__table__table.table_name              == round_trip__table_name
        assert round_trip__table__table.schema__by_name_type()  == dict__table__expected_schema






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


    def test__regression__extract_schema_from_json_data__when_value_has_none(self):
        json_data__list_of_dict = self.json_data__list_of_dict()
        json_data__list_of_dict[1]['an_str'] = None
        json_data__list_of_dict__schema = self.json_db.get_schema_from_json_data(json_data__list_of_dict)
        assert json_data__list_of_dict__schema == {'an_int': Sqlite__Field__Type.INTEGER, 'an_str': Sqlite__Field__Type.TEXT}