from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Field import Sqlite__Field
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import obj_info, obj_data


class test_Sqlite__Field(TestCase):

    def test_from_dict(self):
        data__default     = {'cid': 0, 'name': ''  , 'type': 'INTEGER', 'notnull': 0, 'dflt_value': 'an dflt value'  , 'pk': 0}
        data__name__id    = {'cid': 0, 'name': 'id', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': 'different value', 'pk': 1}
        data__bad__values = {'cid': 0, 'name': 'id', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': True             , 'pk': 1}


        assert Sqlite__Field().json() == data__default

        sqlite_field = Sqlite__Field.from_json(data__name__id)
        assert sqlite_field.json() == Sqlite__Field().deserialize_from_dict(data__name__id).json()
        assert sqlite_field.json() == data__name__id

        # todo: BUGs of type safety on assigment
        should_had_not_worked =  Sqlite__Field.from_json(data__bad__values)
        should_had_not_worked.dflt_value = False
        should_had_not_worked.cid = False
        assert obj_data(should_had_not_worked) == {'cid'        : False ,       # BUG: should not be allowed to be an bool
                                                   'dflt_value' : False ,        # BUG: should not be allowed to be an bool
                                                   'name'       : 'id'  ,
                                                   'notnull'    : 0     ,
                                                   'pk'         : 1     ,
                                                   'type'       : 'Sqlite__Field__Type.INTEGER'}
        Sqlite__Field()
#        pprint(sqlite_field.json())