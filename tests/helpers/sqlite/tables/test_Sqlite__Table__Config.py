from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.tables.Sqlite__Table__Config import Sqlite__Table__Config, SQLITE__TABLE_NAME__CONFIG
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import pickle_load_from_bytes


class test_Sqlite__Table__Config(TestCase):
    table_config: Sqlite__Table__Config
    database    : Sqlite__Database

    @classmethod
    def setUpClass(cls):
        cls.table_config = Sqlite__Table__Config()
        cls.database     = cls.table_config.database
        cls.table_config.create()


    def test___init__(self):
        with self.database as _:
            assert _.exists()  is True
            assert _.db_path   is None
            assert _.in_memory is True

        with self.table_config as _:
            assert _.exists()                   is True
            assert _.table_name                 == SQLITE__TABLE_NAME__CONFIG
            assert _.schema__by_name_type()     == {'id'   : 'INTEGER',
                                                    'key'  : 'TEXT'   ,
                                                    'value': 'BLOB'   }
            assert _.new_row_obj().__locals__() == {'key': '', 'value': b''}



    def test_set_config_data(self):
        config_data = dict(an_str   = '42' ,
                           an_int   = 42   ,
                           an_bytes = b'42',
                           an_bool  = True ,
                           an_list  =  ['A1', 'B2', 'C3'],
                           an_dict  = {'an': 'str', 'another': 'int'})
        expected_rows = [{'id': 1, 'key': 'an_str'  , 'value': b'\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00\x8c\x0242\x94.'                                                     },
                         {'id': 2, 'key': 'an_int'  , 'value': b'\x80\x04K*.'                                                                                                     },
                         {'id': 3, 'key': 'an_bytes', 'value': b'\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00C\x0242\x94.'                                                        },
                         {'id': 4, 'key': 'an_bool' , 'value': b'\x80\x04\x88.'                                                                                                   },
                         {'id': 5, 'key': 'an_list' , 'value': b'\x80\x04\x95\x14\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c\x02A1\x94\x8c\x02B2\x94\x8c\x02C3\x94e.'                  },
                         {'id': 6, 'key': 'an_dict' , 'value': b'\x80\x04\x95 \x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x02an\x94\x8c\x03str\x94\x8c\x07another\x94\x8c\x03int\x94u.'}]
        for item in expected_rows:
            key           = item.get('key')
            pickled_value = item.get('value')
            value         = pickle_load_from_bytes(pickled_value)
            assert config_data[key] == value

        with self.table_config as _:
            assert _.rows() == []
            _.set_config_data(config_data)
        assert _.rows() == expected_rows

