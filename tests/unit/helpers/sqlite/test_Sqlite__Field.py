from typing                                                     import Union, Optional
from unittest                                                   import TestCase
from osbot_utils.helpers.sqlite.Sqlite__Field                   import Sqlite__Field, Sqlite__Field__Type
from osbot_utils.type_safe.steps.Type_Safe__Step__From_Json     import type_safe_step_from_json
from osbot_utils.utils.Misc                                     import random_string


class test_Sqlite__Field(TestCase):

    def setUp(self):
        self.sqlite_field = Sqlite__Field()

    def test__init__(self):
        expected_vars =  {'cid': 0, 'name': '', 'type': None, 'notnull': False, 'dflt_value': None, 'pk': False,
                          'autoincrement': False, 'unique': False, 'is_foreign_key': False, 'references_table': None,
                          'references_column': None, 'on_delete_action': None, 'precision': None, 'scale': None,
                          'check_constraint': None}
        expected_types = {'autoincrement'    : bool                                 ,
                          'check_constraint' : Optional[str]                        ,
                          'cid'              : int                                  ,
                          'dflt_value'       : Union[int, str, float, bytes, None]  , # same as Optional[Union[int, str, float, bytes]]
                          'is_foreign_key'   : bool                                 ,
                          'name'             : str                                  ,
                          'notnull'          : bool                                 ,
                          'on_delete_action' : Optional[str]                        ,
                          'pk'               : bool                                 ,
                          'precision'        : Optional[int]                        ,
                          'references_column': Optional[str]                        ,
                          'references_table' : Optional[str]                        ,
                          'scale'            : Optional[int]                        ,
                          'type'             : Sqlite__Field__Type                  ,
                          'unique'           : bool                                 }

        assert self.sqlite_field.__locals__() == expected_vars
        assert self.sqlite_field.__annotations__ == expected_types


    def test_text_for_create_table(self):
        sqlite_field__use_case_1 = dict(name="id", type=Sqlite__Field__Type.INTEGER, pk=True, autoincrement=True)
        sqlite_field__sql_text_1 = "id INTEGER PRIMARY KEY AUTOINCREMENT"
        assert Sqlite__Field(**sqlite_field__use_case_1).text_for_create_table() ==  sqlite_field__sql_text_1

        sqlite_field__use_case_2 = dict(name="name", type=Sqlite__Field__Type.TEXT, notnull=True, autoincrement=False)
        sqlite_field__sql_text_2 = "name TEXT NOT NULL"
        assert Sqlite__Field(**sqlite_field__use_case_2).text_for_create_table() ==  sqlite_field__sql_text_2

        sqlite_field__use_case_3 = dict(name="email", type=Sqlite__Field__Type.TEXT, unique= True, notnull=True)
        sqlite_field__sql_text_3 = "email TEXT UNIQUE NOT NULL"
        assert Sqlite__Field(**sqlite_field__use_case_3).text_for_create_table() ==  sqlite_field__sql_text_3

        sqlite_field__use_case_4 = dict(name="id", type=Sqlite__Field__Type.INTEGER, pk= True, autoincrement=True)
        sqlite_field__sql_text_4 = "id INTEGER PRIMARY KEY AUTOINCREMENT"
        assert Sqlite__Field(**sqlite_field__use_case_4).text_for_create_table() ==  sqlite_field__sql_text_4

        sqlite_field__use_case_5 = dict(name="title", type=Sqlite__Field__Type.TEXT, notnull=True)
        sqlite_field__sql_text_5 = "title TEXT NOT NULL"
        assert Sqlite__Field(**sqlite_field__use_case_5).text_for_create_table() == sqlite_field__sql_text_5

        sqlite_field__use_case_6 = dict(name="user_id", type=Sqlite__Field__Type.INTEGER)
        sqlite_field__sql_text_6 = "user_id INTEGER"
        assert Sqlite__Field(**sqlite_field__use_case_6).text_for_create_table() == sqlite_field__sql_text_6

        sqlite_field__use_case_7 = dict(name="user_id"        , type=Sqlite__Field__Type.INTEGER  ,
                                        is_foreign_key=True   , references_table="users"          ,
                                        references_column="id", on_delete_action="CASCADE"        )
        sqlite_field__sql_text_7 = "FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE"
        assert Sqlite__Field(**sqlite_field__use_case_7).text_for_create_table() == sqlite_field__sql_text_7

        sqlite_field__use_case_8 = dict(name="id", type=Sqlite__Field__Type.INTEGER, pk=True, autoincrement=True)
        sqlite_field__sql_text_8 = "id INTEGER PRIMARY KEY AUTOINCREMENT"
        assert Sqlite__Field(**sqlite_field__use_case_8).text_for_create_table() == sqlite_field__sql_text_8

        sqlite_field__use_case_9 = dict(name="price", type=Sqlite__Field__Type.DECIMAL,
                                        precision=10, scale=2, check_constraint="price >= 0")
        sqlite_field__sql_text_9 = "price DECIMAL(10, 2) CHECK (price >= 0)"
        assert Sqlite__Field(**sqlite_field__use_case_9).text_for_create_table() == sqlite_field__sql_text_9

        sqlite_field__use_case_10 = dict(name="quantity", type=Sqlite__Field__Type.INTEGER, check_constraint="quantity >= 0")
        sqlite_field__sql_text_10 = "quantity INTEGER CHECK (quantity >= 0)"
        assert Sqlite__Field(**sqlite_field__use_case_10).text_for_create_table() == sqlite_field__sql_text_10

    def test_fix_from_json_data(self):
        for type_type, mapped_type in Sqlite__Field__Type.type_map().items():
            json_data = {'type': type_type }
            result = Sqlite__Field.fix_from_json_data(json_data)
            assert result            is  mapped_type
            assert json_data['type'] is mapped_type

        assert Sqlite__Field.fix_from_json_data({'type': None                    }) is None
        assert Sqlite__Field.fix_from_json_data({'type': 'abc'                   }) is None
        assert Sqlite__Field.fix_from_json_data({'type': Sqlite__Field__Type.REAL}) is None

    def test_from_json(self):
        field_name = "id"
        field_type = 'INTEGER'
        expected_data = { 'autoincrement'    : False,
                          'check_constraint' : None ,
                          'cid'              : 0    ,
                          'dflt_value'       : None ,
                          'is_foreign_key'   : False,
                          'name'             : ''   ,
                          'notnull'          : False,
                          'on_delete_action' : None ,
                          'pk'               : False,
                          'precision'        : None ,
                          'references_column': None ,
                          'references_table' : None ,
                          'scale'            : None ,
                          'type'             : None ,
                          'unique'           : False}

        def assert_sqlite_field_type(field_name, field_type, expected_type_local):
            field_data   = dict(name=field_name, type=field_type)
            expected_data['name'         ] = field_name
            expected_data['type'         ] = expected_type_local
            sqlite_field = Sqlite__Field.from_json(field_data)
            assert sqlite_field.__locals__() == expected_data

        assert Sqlite__Field.from_json({}).obj() == Sqlite__Field().obj()

        assert_sqlite_field_type('id'    , int  , Sqlite__Field__Type.INTEGER)
        assert_sqlite_field_type('aaaa' , float, Sqlite__Field__Type.REAL    )
        assert_sqlite_field_type('bytes', bytes, Sqlite__Field__Type.BLOB    )
        assert_sqlite_field_type(random_string()  , str, Sqlite__Field__Type.TEXT      )



            #assert result == mapped_type



    # regression tests
    def test__regression__type_safety_on__union_vars_assigment(self):
        data__default     = {'cid': 0, 'name': '', 'type': None, 'notnull': False, 'dflt_value': None, 'pk': False, 'autoincrement': False, 'unique': False, 'is_foreign_key': False, 'references_table': None, 'references_column': None, 'on_delete_action': None, 'precision': None, 'scale': None, 'check_constraint': None}
        data__name__id    = {'cid': 0, 'name': 'id', 'type': 'INTEGER', 'notnull': False, 'dflt_value': 'different value', 'pk': True, 'autoincrement': False, 'unique': False, 'is_foreign_key': False, 'references_table': None, 'references_column': None, 'on_delete_action': None, 'precision': None, 'scale': None, 'check_constraint': None}
        data__bad__values = {'autoincrement': False, 'cid': 0, 'name': 'id', 'type': 'INTEGER', 'notnull': False, 'dflt_value': True             , 'pk': True}

        sqlite_field      = Sqlite__Field.from_json(data__name__id)

        assert Sqlite__Field().json() == data__default
        assert sqlite_field.json()    == type_safe_step_from_json.deserialize_from_dict(Sqlite__Field(),data__name__id).json()
        assert sqlite_field.json()    == data__name__id

        with self.assertRaises(Exception) as context:
            Sqlite__Field.from_json(data__bad__values)           # FIXED: was BUG: should have raised exception
        assert context.exception.args[0] == ("Invalid type for attribute 'dflt_value'. Expected 'typing.Union[int, str, "
                                              "float, bytes, NoneType]' but got '<class 'bool'>'")

        with self.assertRaises(Exception) as context:
            sqlite_field.dflt_value = False                     # FIXED: was BUG: assigment should have not worked
        assert context.exception.args[0] == ("Invalid type for attribute 'dflt_value'. Expected 'typing.Union[int, str, "
                                              "float, bytes, NoneType]' but got '<class 'bool'>'")
