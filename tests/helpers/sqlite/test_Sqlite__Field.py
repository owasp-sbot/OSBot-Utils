from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Field import Sqlite__Field
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import obj_info, obj_data


class test_Sqlite__Field(TestCase):

    def test_regression__type_safety_on__union_vars_assigment(self):
        data__default     = {'cid': 0, 'name': ''  , 'type': 'INTEGER', 'notnull': 0, 'dflt_value': 'an dflt value'  , 'pk': 0}
        data__name__id    = {'cid': 0, 'name': 'id', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': 'different value', 'pk': 1}
        data__bad__values = {'cid': 0, 'name': 'id', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': True             , 'pk': 1}

        sqlite_field      = Sqlite__Field.from_json(data__name__id)

        assert Sqlite__Field().json() == data__default
        assert sqlite_field.json()    == Sqlite__Field().deserialize_from_dict(data__name__id).json()
        assert sqlite_field.json()    == data__name__id

        with self.assertRaises(Exception) as context:
            Sqlite__Field.from_json(data__bad__values)           # FIXED: was BUG: should have raised exception
        assert context.exception.args[0] == ("Invalid type for attribute 'dflt_value'. Expected 'typing.Union[int, str, "
                                              "float, bytes, NoneType]' but got '<class 'bool'>'")

        with self.assertRaises(Exception) as context:
            sqlite_field.dflt_value = False                     # FIXED: was BUG: assigment should have not worked
        assert context.exception.args[0] == ("Invalid type for attribute 'dflt_value'. Expected 'typing.Union[int, str, "
                                              "float, bytes, NoneType]' but got '<class 'bool'>'")
