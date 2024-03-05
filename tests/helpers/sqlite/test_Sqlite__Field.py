from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Field import Sqlite__Field
from osbot_utils.utils.Dev import pprint


class test_Sqlite__Field(TestCase):

    def test_from_dict(self):

        data = { 'cid'       : 0        ,
                 'name'      : ''     ,         # was id
                 'type'      : 'INTEGER',
                 'notnull'   : 0        ,
                 'dflt_value': None     ,
                 'pk'        : 0        }       # was 1

        sqlite_field = Sqlite__Field()
        #sqlite_field.deserialize_from_dict(data)
        #pprint(sqlite_field.__locals__())
        #pprint(sqlite_field.json())
        assert sqlite_field.json() == data