from unittest import TestCase

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Json import Sqlite__DB__Json
from osbot_utils.utils.Dev import pprint

class test_Sqlite__DB__Json(TestCase):

    def setUp(self):
        self.json_db = Sqlite__DB__Json()
        print()

    def test_load_data(self):
        class Data_Set(Kwargs_To_Self):
            str_field : str  = 'an_str'
            int_field : int  = 42
            bool_field: bool = True

        json_data = Data_Set().json()

        assert json_data == {'bool_field': True, 'int_field': 42, 'str_field': 'an_str'}

        result = self.json_db.json_data_convert_to_sqlite_fields(json_data)
        pprint(result)