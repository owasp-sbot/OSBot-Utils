from decimal import Decimal
from types import NoneType
from unittest import TestCase

from osbot_utils.helpers.sqlite.models.Sqlite__Field__Type import Sqlite__Field__Type
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import obj_info


class test_Sqlite__Field__Type(TestCase):

    # def setUp(self):
    #     self.field_type = Sqlite__Field__Type()

    def test__init__(self):
        assert Sqlite__Field__Type.enum_map() == { 'BLOB'   : bytes    ,
                                                   'DECIMAL': Decimal  ,
                                                   'INTEGER': int      ,
                                                   'NUMERIC': 'numeric',                            # todo see if there is a better way to handle this use of 'numeric', (or if it is even needed)
                                                   'REAL'   : float    ,
                                                   'TEXT'   : str      ,
                                                   'UNKNOWN': NoneType }

        assert Sqlite__Field__Type.type_map() ==  { 'numeric': Sqlite__Field__Type.NUMERIC  ,       # todo see if there is a better way to handle this use of 'numeric', (or if it is even needed)
                                                    Decimal  : Sqlite__Field__Type.DECIMAL  ,
                                                    bytes    : Sqlite__Field__Type.BLOB     ,
                                                    int      : Sqlite__Field__Type.INTEGER  ,
                                                    NoneType : Sqlite__Field__Type.UNKNOWN  ,
                                                    float    : Sqlite__Field__Type.REAL     ,
                                                    str      : Sqlite__Field__Type.TEXT     }