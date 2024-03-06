from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Field import Sqlite__Field
from osbot_utils.utils.Dev import pprint


class test_Sqlite__Field(TestCase):

    def test_from_dict(self):
        data__default  = {'cid': 0, 'name': ''  , 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}
        data__name__id = {'cid': 0, 'name': 'id', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1}

        assert Sqlite__Field().json() == data__default

        sqlite_field = Sqlite__Field.from_json(data__name__id)

        assert sqlite_field.json() == Sqlite__Field().deserialize_from_dict(data__name__id).json()
        assert sqlite_field.json() == data__name__id