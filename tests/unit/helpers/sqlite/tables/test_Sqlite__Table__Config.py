import sys
import pytest
from unittest                                                   import TestCase
from osbot_utils.helpers.sqlite.Sqlite__Database                import Sqlite__Database
from osbot_utils.helpers.sqlite.tables.Sqlite__Table__Config    import Sqlite__Table__Config, SQLITE__TABLE_NAME__CONFIG
from osbot_utils.utils.Misc                                     import random_value
from osbot_utils.utils.Objects                                  import pickle_load_from_bytes, pickle_save_to_bytes


class test_Sqlite__Table__Config(TestCase):
    table_config: Sqlite__Table__Config
    database    : Sqlite__Database
    config_data = dict(an_str   = '42'                          ,
                       an_int   = 42                            ,
                       an_bytes = b'42'                         ,
                       an_bool  = True                          ,
                       an_list  =  ['A1', 'B2', 'C3']           ,
                       an_dict  = {'an': 'str', 'another': 'int'})

    @classmethod
    def setUpClass(cls):
        if sys.version_info < (3, 8):
            pytest.skip("Skipping tests that don't work on 3.7 or lower")

        cls.table_config = Sqlite__Table__Config()
        cls.database     = cls.table_config.database
        cls.table_config.setup()


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
            assert _.indexes()                  == ['idx__config__key']

    def test_set_config_data(self):

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
            assert self.config_data[key] == value

        with self.table_config as _:
            assert _.rows() == []
            _.set_config_data(self.config_data)
        assert _.rows()        == expected_rows
        assert _.config_data() == self.config_data

    def test_set_value(self):
        with self.table_config as _:
            _.clear()
            key            = random_value(prefix='an_key'       )
            original_value = random_value(prefix='an_value'     )
            changed_value  = random_value(prefix='another_value')
            assert _.config_data() == {}

            _.set_value(key, original_value)

            assert _.rows()        == [{'id': 1, 'key': key,   'value': pickle_save_to_bytes(original_value)}]
            assert _.config_data() == {key: original_value}

            _.set_value(key, changed_value)

            assert _.config_data() == {key: changed_value}
            assert _.rows() == [{'id': 1, 'key': key, 'value': pickle_save_to_bytes(changed_value)}]


    def test_value(self):
        with self.table_config as _:
            _.set_config_data(self.config_data)
            for key,value in self.config_data.items():
                assert _.value(key) == value
            assert _.value('aaaa') is None
            assert _.value(None  ) is None
            assert _.value(123   ) is None
